#!/usr/bin/env python3
"""ShipVitals release gate runner.

This runner is conservative: it records what it can prove and labels missing proof as NOT VERIFIED.
"""
import argparse, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
from urllib.parse import urlparse
try:
    from shipvitals_config import load_config, merge_config, has_product_promise
except Exception:
    sys.path.append(str(Path(__file__).resolve().parent))
    from shipvitals_config import load_config, merge_config, has_product_promise

SKIP_DIRS_DEFAULT={'.git','node_modules','dist','build','.next','.venv','venv','.shipvitals-evidence','.shipvitals-golden-benchmark','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache'}
SKIP_SUFFIXES={'.pyc','.pyo','.png','.jpg','.jpeg','.gif','.webp','.ico','.pdf','.zip','.gz','.tar','.mp4','.mov'}
SECRET_PATTERNS=[r'(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*["\'][A-Za-z0-9_./+=-]{12,}["\']', r'sk-[A-Za-z0-9_-]{20,}', r'AIza[0-9A-Za-z\-_]{20,}']
FAKE_PATTERNS=[r'\bTODO\b',r'\bFIXME\b',r'placeholder',r'demo only',r'mock data',r'\.skip\(',r'catch\s*\([^)]*\)\s*\{\s*\}']
UI_TYPE_KEYWORDS=('web','saas','dashboard','landing','shopify','marketplace','extension','mobile','frontend','ui','app')
HIGH_STAKES_KEYWORDS=('client','paid','public','production','marketplace','shopify','app store','security','payment','auth','privacy')
NON_BLOCKING_EVIDENCE_PARTS={'tests','test','fixtures','fixture','benchmarks','benchmark','case-studies','examples','.shipvitals-evidence','_archive','third-party','vendor','vendors'}
NON_BLOCKING_SECRET_PARTS={'docs','documentation','examples','sample','samples','_archive','third-party','vendor','vendors','licenses'}
NON_BLOCKING_SECRET_FILES={'readme.md','readme.mdx','license','license.md'}
NON_BLOCKING_FAKE_PARTS={'docs','references','templates','registry','schemas','agents','marketing'}
CORE_FAKE_PARTS={'src','app','pages','lib','components','server','api','routes'}

def iter_files(root, exclude):
    skip=set(SKIP_DIRS_DEFAULT)|set(exclude or [])
    for p in root.rglob('*'):
        rel=str(p.relative_to(root)).replace('\\','/').lower()
        skip_paths={str(x).replace('\\','/').strip('/').lower() for x in skip}
        if any(part in skip for part in p.parts): continue
        if any(rel == x or rel.startswith(x.rstrip('/') + '/') for x in skip_paths if '/' in x): continue
        if p.suffix.lower() in SKIP_SUFFIXES: continue
        if p.is_file() and p.stat().st_size < 700_000: yield p

def run(cmd, root, timeout, verbose=False):
    started=time.time()
    try:
        r=subprocess.run(cmd, cwd=root, shell=True, text=True, capture_output=True, timeout=timeout)
        out={'cmd':cmd,'exit_code':r.returncode,'seconds':round(time.time()-started,2),'stdout':r.stdout[-4000:],'stderr':r.stderr[-4000:]}
    except Exception as e:
        out={'cmd':cmd,'exit_code':None,'seconds':round(time.time()-started,2),'error':str(e)}
    if verbose: print(json.dumps(out, indent=2))
    return out

def detect_commands(root):
    commands=[]
    pkg=root/'package.json'
    if pkg.exists():
        try:
            scripts=json.loads(pkg.read_text()).get('scripts',{})
            pm='npm'
            if (root/'pnpm-lock.yaml').exists(): pm='pnpm'
            elif (root/'yarn.lock').exists(): pm='yarn'
            elif (root/'bun.lockb').exists(): pm='bun'
            for name in ['typecheck','lint','test','build']:
                if name in scripts: commands.append(f'{pm} run {name}')
        except Exception: pass
    if (root/'pyproject.toml').exists() or (root/'pytest.ini').exists(): commands.append('python -m pytest')
    if (root/'manage.py').exists(): commands.append('python manage.py check --deploy')
    return commands

def as_list(value):
    if not value: return []
    if isinstance(value, list): return [str(x) for x in value if str(x).strip()]
    return [str(value)]

def project_type(config):
    return str(config.get('project', {}).get('type', '')).lower()

def is_ui_project(config):
    ptype=project_type(config)
    return any(k in ptype for k in UI_TYPE_KEYWORDS)

def is_high_stakes(config):
    project=config.get('project', {})
    text=' '.join(str(project.get(k, '')) for k in ('type','audience','destination','promise')).lower()
    return any(k in text for k in HIGH_STAKES_KEYWORDS)

def evidence_values(config, key, cli_values):
    configured=config.get('evidence', {}).get(key, [])
    return as_list(configured)+as_list(cli_values)

def cap_score(caps, score, reason):
    caps.append({'max_score':score,'reason':reason})

def path_parts(value):
    return {part.lower() for part in Path(value).parts}

def is_non_blocking_evidence_path(value):
    parts=path_parts(value)
    return bool(parts & NON_BLOCKING_EVIDENCE_PARTS)

def is_non_blocking_secret_path(value):
    parts=path_parts(value)
    name=Path(value).name.lower()
    return bool(parts & (NON_BLOCKING_EVIDENCE_PARTS | NON_BLOCKING_SECRET_PARTS)) or name in NON_BLOCKING_SECRET_FILES

def is_core_fake_path(value):
    parts=path_parts(value)
    if parts & (NON_BLOCKING_EVIDENCE_PARTS | NON_BLOCKING_FAKE_PARTS):
        return False
    suffix=Path(value).suffix.lower()
    return bool(parts & CORE_FAKE_PARTS) or suffix in {'.js','.jsx','.ts','.tsx','.py','.php','.rb','.go','.rs','.java','.cs'}

def scan(root, patterns, exclude, is_priority=None):
    findings=[]; priority_findings=[]; priority_patterns=set(); priority_count=0
    for p in iter_files(root, exclude):
        txt=p.read_text(errors='ignore')
        for pat in patterns:
            for m in re.finditer(pat, txt, re.I|re.S):
                finding={'file':str(p.relative_to(root)),'line':txt[:m.start()].count('\n')+1,'pattern':pat}
                if is_priority and is_priority(finding):
                    priority_count += 1
                    if len(priority_findings) < 300: priority_findings.append(finding)
                    elif pat not in priority_patterns: priority_findings.insert(0, finding)
                    priority_patterns.add(pat)
                elif len(findings) < 300: findings.append(finding)
    return {'findings':priority_findings + findings,'priority_count':priority_count,'priority_patterns':list(priority_patterns)}

def git_head(root):
    result=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'], text=True, capture_output=True)
    return result.stdout.strip().lower() if result.returncode == 0 else ''

def inside(root, candidate):
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False

def validate_manifest(root, value, kind):
    def fail(reason): return False, reason
    manifest_path=Path(value).expanduser()
    if not manifest_path.is_absolute(): manifest_path=root/manifest_path
    if not str(value).endswith('.shipvitals-evidence.json'): return fail('Expected a .shipvitals-evidence.json manifest.')
    if not manifest_path.is_file(): return fail('Manifest file not found.')
    try: manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    except Exception: return fail('Manifest is not valid JSON.')
    if manifest.get('shipvitals_evidence') != 1 or manifest.get('kind') != kind: return fail(f'Manifest kind must be {kind}.')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', str(manifest.get('observed_at',''))): return fail('observed_at must be a UTC timestamp.')
    if len(str(manifest.get('source','')).strip()) < 3: return fail('source is required.')
    if len(str(manifest.get('summary','')).strip()) < 20: return fail('summary must contain at least 20 characters.')
    artifacts=manifest.get('artifacts')
    if not isinstance(artifacts,list) or not artifacts: return fail('At least one artifact is required.')
    visual_ext={'.png','.jpg','.jpeg','.gif','.webp','.mp4','.mov','.zip','.har','.trace'}
    for artifact in artifacts:
        if not isinstance(artifact,dict): return fail('Invalid artifact entry.')
        if artifact.get('path'):
            artifact_path=(manifest_path.parent/str(artifact['path'])).resolve()
            if not inside(root, artifact_path): return fail('Local artifacts must stay inside the audited project.')
            if not artifact_path.is_file() or artifact_path.stat().st_size == 0: return fail('Local artifact is missing or empty.')
            digest=hashlib.sha256(artifact_path.read_bytes()).hexdigest()
            if not re.fullmatch(r'[a-fA-F0-9]{64}',str(artifact.get('sha256',''))) or digest != str(artifact['sha256']).lower(): return fail('Local artifact SHA-256 mismatch.')
            if kind == 'visual' and artifact_path.suffix.lower() not in visual_ext: return fail('Visual evidence must reference an image, video, trace, HAR, or archive.')
        elif artifact.get('url'):
            parsed=urlparse(str(artifact['url']))
            if parsed.scheme != 'https' or not parsed.netloc: return fail('Artifact URLs must use HTTPS.')
            if kind != 'ci' and not re.fullmatch(r'[a-fA-F0-9]{64}',str(artifact.get('sha256',''))): return fail('Remote non-CI artifacts require a SHA-256.')
        else: return fail('Each artifact requires path or url.')
    head=git_head(root)
    if kind == 'ci':
        if not re.fullmatch(r'https://github\.com/[^/]+/[^/]+/actions/runs/\d+',str(manifest.get('run_url',''))): return fail('CI evidence requires a GitHub Actions run URL.')
        if not head or str(manifest.get('commit','')).lower() != head: return fail('CI evidence commit does not match the audited HEAD.')
    if kind == 'independent_review':
        if manifest.get('decision') != 'accept' or len(str(manifest.get('reviewer','')).strip()) < 3: return fail('Independent evidence requires an identified reviewer and accept decision.')
        if not head or str(manifest.get('reviewed_commit','')).lower() != head: return fail('Independent review does not cover the audited HEAD.')
    return True, ''

def validate_evidence(root, values, kind):
    valid=[]; rejected=[]; details=[]
    for value in as_list(values):
        accepted,reason=validate_manifest(root,value,kind)
        (valid if accepted else rejected).append(value)
        if not accepted: details.append({'value':value,'reason':reason})
    return {'valid':valid,'rejected':rejected,'details':details}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('project', nargs='?', default='.')
    ap.add_argument('--ci', action='store_true')
    ap.add_argument('--no-fail', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--mode', choices=['quick','deep'], default='quick')
    ap.add_argument('--timeout', type=int, default=120)
    ap.add_argument('--runtime-proof', action='append', default=[], help='Existing runtime artifact path or HTTPS URL.')
    ap.add_argument('--visual-proof', action='append', default=[], help='Existing screenshot, video, trace path, or HTTPS URL.')
    ap.add_argument('--ci-proof', action='append', default=[], help='CI/hook artifact, run URL, or reproducibility proof.')
    ap.add_argument('--independent-review', action='append', default=[], help='Second-auditor proof or review artifact.')
    args=ap.parse_args()
    root=Path(args.project).resolve(); out=root/'.shipvitals-evidence'; out.mkdir(exist_ok=True)
    config=merge_config(load_config(root))
    config_exists=(root/'.shipvitals-config.json').exists()
    commands=list(config.get('commands',{}).values()) or detect_commands(root)
    if args.mode=='quick': commands=commands[:4]
    results=[run(c, root, args.timeout, args.verbose) for c in commands]
    secret_scan=scan(root, SECRET_PATTERNS, config.get('exclude'), lambda item: not is_non_blocking_secret_path(item['file']))
    secrets=secret_scan['findings']
    fake_scan=scan(root, FAKE_PATTERNS, config.get('exclude'), lambda item: is_core_fake_path(item['file']))
    fake=fake_scan['findings']
    failed=[r for r in results if r.get('exit_code') != 0]
    checked_proof={
        'runtime':validate_evidence(root, evidence_values(config, 'runtime', args.runtime_proof), 'runtime'),
        'visual':validate_evidence(root, evidence_values(config, 'visual', args.visual_proof), 'visual'),
        'ci':validate_evidence(root, evidence_values(config, 'ci', args.ci_proof), 'ci'),
        'independent_review':validate_evidence(root, evidence_values(config, 'independent_review', args.independent_review), 'independent_review'),
    }
    runtime_proof=checked_proof['runtime']['valid']; visual_proof=checked_proof['visual']['valid']
    ci_proof=checked_proof['ci']['valid']; independent_review=checked_proof['independent_review']['valid']
    evidence=['L1_STATIC']
    if results and all(r.get('exit_code') is not None for r in results): evidence.append('L2_DETERMINISTIC')
    if runtime_proof: evidence.append('L3_RUNTIME')
    if visual_proof: evidence.append('L4_VISUAL_FLOW')
    if ci_proof: evidence.append('L5_CI_REPRODUCIBLE')
    if independent_review: evidence.append('L6_INDEPENDENT')
    p0=[]; p1=[]
    caps=[]
    if not has_product_promise(config):
        p0.append('Missing product promise or critical flows.')
        cap_score(caps, 74, 'No product promise or critical flows.')
    blocking_secrets=[s for s in secrets if not is_non_blocking_secret_path(s['file'])]
    blocking_fake=[f for f in fake if is_core_fake_path(f['file'])]
    if blocking_secrets:
        p0.append('Secret candidates found.')
        cap_score(caps, 59, 'Secret candidates found.')
    if failed:
        p1.append('One or more project commands failed.')
        cap_score(caps, 89, 'One or more deterministic commands failed.')
    if not results:
        cap_score(caps, 69, 'No deterministic command output.')
    needs_runtime=bool(config.get('project', {}).get('critical_flows'))
    needs_visual=is_ui_project(config)
    not_verified=[]
    if needs_runtime and not runtime_proof:
        not_verified.append('runtime proof')
        cap_score(caps, 89, 'Runtime proof missing for critical flows.')
    if needs_visual and not visual_proof:
        not_verified.append('visual proof')
        cap_score(caps, 74, 'UI project missing visual proof.')
    needs_independent=is_high_stakes(config)
    if not independent_review:
        not_verified.append('independent review')
        if needs_independent:
            cap_score(caps, 89, 'High-stakes release missing independent review.')
    demo_only=any('demo only' in pat.lower() or 'mock data' in pat.lower() for pat in fake_scan['priority_patterns'])
    if demo_only:
        cap_score(caps, 69, 'Demo-only or mock-data signal found.')
    if p0:
        verdict='NOT READY'
    elif demo_only:
        verdict='DEMO ONLY'
    elif p1 or not results or (needs_runtime and not runtime_proof) or (needs_visual and not visual_proof) or (needs_independent and not independent_review): verdict='ALMOST READY'
    else: verdict='READY'
    score=min([100]+[c['max_score'] for c in caps])
    report={'tool':'ShipVitals','version':'1.0.0-beta.1','generated_at':time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),'project':str(root),'mode':args.mode,'config_exists':config_exists,'product_type':project_type(config),'product_promise_present':has_product_promise(config),'commands_detected':commands,'command_results':results,'secret_candidates':secrets[:80],'blocking_secret_candidates':blocking_secrets[:80],'fake_completion_candidates':fake[:160],'blocking_fake_completion_candidates':blocking_fake[:80],'proof':{'runtime':runtime_proof,'visual':visual_proof,'ci':ci_proof,'independent_review':independent_review},'rejected_proof':{key:value['rejected'] for key,value in checked_proof.items()},'rejected_proof_details':{key:value['details'] for key,value in checked_proof.items()},'scan_stats':{'secret_priority_count':secret_scan['priority_count'],'fake_priority_count':fake_scan['priority_count']},'evidence_levels':evidence,'score':score,'score_caps':caps,'p0':p0,'p1':p1,'verdict':verdict,'not_verified':not_verified}
    report_text=json.dumps(report, indent=2)
    (out/'report.json').write_text(report_text, encoding='utf-8')
    (out/'shipvitals-report.json').write_text(report_text, encoding='utf-8')
    summary=f"# ShipVitals Summary\n\nVerdict: **{verdict}**\n\n- Score: {score}\n- P0: {len(p0)}\n- P1: {len(p1)}\n- Commands: {len(commands)}\n- Secret candidates: {len(secrets)}\n- Fake-completion candidates: {len(fake)}\n- Not verified: {', '.join(not_verified) if not_verified else 'none'}\n\nSee `report.json`.\n"
    (out/'summary.md').write_text(summary, encoding='utf-8')
    (out/'shipvitals-summary.md').write_text(summary, encoding='utf-8')
    print(json.dumps(report if args.ci else {'status':'ok','verdict':verdict,'out':str(out),'p0':len(p0),'p1':len(p1)}, indent=2))
    if not args.no_fail and verdict != 'READY': raise SystemExit(1)
if __name__=='__main__': main()
