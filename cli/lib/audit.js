const { spawnSync } = require('node:child_process');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const VERSION = '1.0.0-beta.1';
const SKIP_DIRS = new Set([
  '.git', 'node_modules', 'dist', 'build', '.next', '.venv', 'venv',
  '.shipvitals-evidence', '.shipvitals-golden-benchmark', '__pycache__',
  '.pytest_cache', '.mypy_cache', '.ruff_cache',
]);
const SKIP_SUFFIXES = new Set([
  '.pyc', '.pyo', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico',
  '.pdf', '.zip', '.gz', '.tar', '.mp4', '.mov',
]);
const SECRET_PATTERNS = [
  /\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*["'][A-Za-z0-9_./+=-]{12,}["']/gi,
  /sk-[A-Za-z0-9_-]{20,}/g,
  /AIza[0-9A-Za-z_-]{20,}/g,
];
const FAKE_PATTERNS = [
  /\bTODO\b/gi, /\bFIXME\b/gi, /placeholder/gi, /demo only/gi,
  /mock data/gi, /\.skip\(/gi, /catch\s*\([^)]*\)\s*\{\s*\}/gis,
];
const UI_TYPE_KEYWORDS = ['web', 'saas', 'dashboard', 'landing', 'shopify', 'marketplace', 'extension', 'mobile', 'frontend', 'ui', 'app'];
const HIGH_STAKES_KEYWORDS = ['client', 'paid', 'public', 'production', 'marketplace', 'shopify', 'app store', 'security', 'payment', 'auth', 'privacy'];
const NON_BLOCKING_EVIDENCE_PARTS = new Set(['tests', 'test', 'fixtures', 'fixture', 'benchmarks', 'benchmark', 'case-studies', 'examples', '.shipvitals-evidence', '_archive', 'third-party', 'vendor', 'vendors']);
const NON_BLOCKING_SECRET_PARTS = new Set(['docs', 'documentation', 'examples', 'sample', 'samples', '_archive', 'third-party', 'vendor', 'vendors', 'licenses']);
const NON_BLOCKING_SECRET_FILES = new Set(['readme.md', 'readme.mdx', 'license', 'license.md']);
const NON_BLOCKING_FAKE_PARTS = new Set(['docs', 'references', 'templates', 'registry', 'schemas', 'agents', 'marketing']);
const CORE_FAKE_PARTS = new Set(['src', 'app', 'pages', 'lib', 'components', 'server', 'api', 'routes']);
const CORE_SUFFIXES = new Set(['.js', '.jsx', '.ts', '.tsx', '.py', '.php', '.rb', '.go', '.rs', '.java', '.cs']);

const DEFAULT_CONFIG = {
  version: 1,
  project: { name: '', type: '', audience: '', destination: '', promise: '', critical_flows: [] },
  commands: {},
  evidence: { runtime: [], visual: [], ci: [], independent_review: [] },
  exclude: ['node_modules', 'dist', 'build', '.next', '.git'],
  branding: {},
};

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function loadConfig(root) {
  const configPath = path.join(root, '.shipvitals-config.json');
  const config = clone(DEFAULT_CONFIG);
  if (!fs.existsSync(configPath)) return { config, exists: false };
  const loaded = JSON.parse(fs.readFileSync(configPath, 'utf8').replace(/^\uFEFF/, ''));
  for (const [key, value] of Object.entries(loaded)) {
    config[key] = value && typeof value === 'object' && !Array.isArray(value) && config[key]
      ? { ...config[key], ...value }
      : value;
  }
  return { config, exists: true };
}

function hasProductPromise(config) {
  return Boolean(config.project?.promise && config.project?.critical_flows?.length);
}

function walkFiles(root, exclusions) {
  const files = [];
  const excluded = new Set([...SKIP_DIRS, ...(exclusions || [])].map(value => String(value).replaceAll('\\', '/').replace(/^\/+|\/+$/g, '').toLowerCase()));
  function visit(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const absolute = path.join(directory, entry.name);
      const relative = path.relative(root, absolute).replaceAll('\\', '/');
      const lower = relative.toLowerCase();
      if (entry.isDirectory()) {
        if (excluded.has(entry.name.toLowerCase()) || [...excluded].some(item => item.includes('/') && (lower === item || lower.startsWith(`${item}/`)))) continue;
        visit(absolute);
      } else if (entry.isFile()) {
        if (SKIP_SUFFIXES.has(path.extname(entry.name).toLowerCase())) continue;
        if (fs.statSync(absolute).size < 700_000) files.push({ absolute, relative });
      }
    }
  }
  visit(root);
  return files;
}

function scan(root, patterns, exclusions, isPriority) {
  const findings = [];
  const priorityFindings = [];
  const priorityPatterns = new Set();
  let priorityCount = 0;
  for (const file of walkFiles(root, exclusions)) {
    let text;
    try {
      text = fs.readFileSync(file.absolute, 'utf8');
    } catch {
      continue;
    }
    for (const pattern of patterns) {
      pattern.lastIndex = 0;
      for (const match of text.matchAll(pattern)) {
        const finding = {
          file: file.relative,
          line: text.slice(0, match.index).split('\n').length,
          pattern: pattern.source,
        };
        if (isPriority?.(finding)) {
          priorityCount += 1;
          if (priorityFindings.length < 300) priorityFindings.push(finding);
          else if (!priorityPatterns.has(finding.pattern)) priorityFindings.unshift(finding);
          priorityPatterns.add(finding.pattern);
        } else if (findings.length < 300) {
          findings.push(finding);
        }
      }
    }
  }
  return { findings: [...priorityFindings, ...findings], priorityCount, priorityPatterns: [...priorityPatterns] };
}

function detectCommands(root) {
  const commands = [];
  const packagePath = path.join(root, 'package.json');
  if (fs.existsSync(packagePath)) {
    try {
      const scripts = JSON.parse(fs.readFileSync(packagePath, 'utf8')).scripts || {};
      const manager = fs.existsSync(path.join(root, 'pnpm-lock.yaml'))
        ? 'pnpm'
        : fs.existsSync(path.join(root, 'yarn.lock'))
          ? 'yarn'
          : fs.existsSync(path.join(root, 'bun.lockb')) ? 'bun' : 'npm';
      for (const name of ['typecheck', 'lint', 'test', 'build']) {
        if (scripts[name]) commands.push(`${manager} run ${name}`);
      }
    } catch {}
  }
  if (fs.existsSync(path.join(root, 'pyproject.toml')) || fs.existsSync(path.join(root, 'pytest.ini'))) commands.push('python -m pytest');
  if (fs.existsSync(path.join(root, 'manage.py'))) commands.push('python manage.py check --deploy');
  return commands;
}

function runCommand(command, root, timeout, verbose) {
  const started = Date.now();
  const result = spawnSync(command, { cwd: root, shell: true, encoding: 'utf8', timeout: timeout * 1000 });
  const output = {
    cmd: command,
    exit_code: typeof result.status === 'number' ? result.status : null,
    seconds: Number(((Date.now() - started) / 1000).toFixed(2)),
  };
  if (result.stdout) output.stdout = result.stdout.slice(-4000);
  if (result.stderr) output.stderr = result.stderr.slice(-4000);
  if (result.error) output.error = result.error.message;
  if (verbose) process.stderr.write(`${JSON.stringify(output, null, 2)}\n`);
  return output;
}

function asList(value) {
  if (!value) return [];
  return (Array.isArray(value) ? value : [value]).map(String).filter(item => item.trim());
}

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function gitHead(root) {
  const result = spawnSync('git', ['-C', root, 'rev-parse', 'HEAD'], { encoding: 'utf8' });
  return result.status === 0 ? result.stdout.trim().toLowerCase() : '';
}

function gitRepository(root) {
  const result = spawnSync('git', ['-C', root, 'remote', 'get-url', 'origin'], { encoding: 'utf8' });
  if (result.status !== 0) return '';
  const match = result.stdout.trim().match(/github\.com[/:]([^/]+)\/([^/\s]+?)(?:\.git)?$/i);
  return match ? (match[1] + '/' + match[2]).toLowerCase() : '';
}

function inside(root, candidate) {
  const relative = path.relative(path.resolve(root), path.resolve(candidate));
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function validVisualFile(file) {
  const bytes = fs.readFileSync(file);
  const signatures = [
    Buffer.from([0x89, 0x50, 0x4e, 0x47]),
    Buffer.from([0xff, 0xd8, 0xff]),
    Buffer.from('GIF8'),
    Buffer.from('RIFF'),
    Buffer.from('PK\x03\x04'),
  ];
  if (signatures.some(signature => bytes.subarray(0, signature.length).equals(signature))) return true;
  return bytes.length > 12 && bytes.subarray(4, 8).toString('ascii') === 'ftyp';
}

async function githubJson(apiPath) {
  try {
    const response = await fetch('https://api.github.com' + apiPath, {
      headers: {
        Accept: 'application/vnd.github+json',
        'User-Agent': 'shipvitals-' + VERSION,
        ...(process.env.SHIPVITALS_GITHUB_TOKEN ? { Authorization: 'Bearer ' + process.env.SHIPVITALS_GITHUB_TOKEN } : {}),
      },
    });
    return response.ok ? response.json() : null;
  } catch {
    return null;
  }
}

async function verifyCiProvenance(root, manifest) {
  const match = String(manifest.run_url || '').match(/^https:\/\/github\.com\/([^/]+)\/([^/]+)\/actions\/runs\/(\d+)$/);
  if (!match) return 'CI evidence requires a GitHub Actions run URL.';
  const repository = (match[1] + '/' + match[2]).toLowerCase();
  const expectedRepository = gitRepository(root);
  if (expectedRepository && repository !== expectedRepository) return 'CI run belongs to a different repository.';
  const run = await githubJson('/repos/' + match[1] + '/' + match[2] + '/actions/runs/' + match[3]);
  if (!run || String(run.html_url) !== String(manifest.run_url)) return 'GitHub could not verify the CI run.';
  const head = gitHead(root);
  if (!head || String(run.head_sha || '').toLowerCase() !== head || String(manifest.commit || '').toLowerCase() !== head) return 'CI evidence commit does not match the audited HEAD.';
  const currentRun = process.env.GITHUB_ACTIONS === 'true'
    && String(process.env.GITHUB_RUN_ID || '') === match[3]
    && String(process.env.GITHUB_SHA || '').toLowerCase() === head;
  if (run.conclusion !== 'success' && !(currentRun && ['queued', 'in_progress'].includes(run.status))) return 'The verified CI run did not complete successfully.';
  return '';
}

async function verifyIndependentProvenance(root, manifest) {
  const match = String(manifest.review_url || '').match(/^https:\/\/github\.com\/([^/]+)\/([^/]+)\/(?:issues|pull)\/\d+#issuecomment-(\d+)$/);
  if (!match) return 'Independent review requires a GitHub issue or pull-request comment URL.';
  const repository = (match[1] + '/' + match[2]).toLowerCase();
  const expectedRepository = gitRepository(root);
  if (!expectedRepository || repository !== expectedRepository) return 'Independent review must be published on the audited repository.';
  const comment = await githubJson('/repos/' + match[1] + '/' + match[2] + '/issues/comments/' + match[3]);
  if (!comment || String(comment.html_url) !== String(manifest.review_url)) return 'GitHub could not verify the review comment.';
  const reviewer = String(comment.user?.login || '');
  if (!reviewer || reviewer.toLowerCase() !== String(manifest.reviewer || '').toLowerCase() || reviewer.toLowerCase() === match[1].toLowerCase()) return 'Reviewer identity is not independent of the repository owner.';
  if (!new Set(['NONE', 'CONTRIBUTOR', 'FIRST_TIMER', 'FIRST_TIME_CONTRIBUTOR']).has(comment.author_association)) return 'Reviewer is an owner, member, or collaborator.';
  const head = gitHead(root);
  if (!head || String(manifest.reviewed_commit || '').toLowerCase() !== head) return 'Independent review does not cover the audited HEAD.';
  if (!String(comment.body || '').includes('SHIPVITALS-L6 ACCEPT ' + head)) return 'Review comment does not contain the required acceptance statement.';
  const user = await githubJson('/users/' + encodeURIComponent(reviewer));
  if (!user || !user.created_at || Date.now() - Date.parse(user.created_at) < 90 * 24 * 60 * 60 * 1000) return 'Reviewer account must be at least 90 days old.';
  return '';
}

async function validateManifest(root, value, kind) {
  const fail = reason => ({ accepted: false, reason });
  const manifestPath = path.isAbsolute(value) ? value : path.resolve(root, value);
  if (!value.endsWith('.shipvitals-evidence.json')) return fail('Expected a .shipvitals-evidence.json manifest.');
  if (!fs.existsSync(manifestPath) || !fs.statSync(manifestPath).isFile()) return fail('Manifest file not found.');
  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8').replace(/^\uFEFF/, ''));
  } catch {
    return fail('Manifest is not valid JSON.');
  }
  if (manifest.shipvitals_evidence !== 1 || manifest.kind !== kind) return fail('Manifest kind must be ' + kind + '.');
  const observed = Date.parse(manifest.observed_at || '');
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(manifest.observed_at || '') || Number.isNaN(observed)) return fail('observed_at must be a valid UTC timestamp.');
  if (observed > Date.now() + 5 * 60 * 1000 || Date.now() - observed > 30 * 24 * 60 * 60 * 1000) return fail('Evidence timestamp must be within the last 30 days.');
  if (typeof manifest.source !== 'string' || manifest.source.trim().length < 3) return fail('source is required.');
  if (typeof manifest.summary !== 'string' || manifest.summary.trim().length < 20) return fail('summary must contain at least 20 characters.');
  if (!Array.isArray(manifest.artifacts) || !manifest.artifacts.length) return fail('At least one artifact is required.');

  const head = gitHead(root);
  if (['runtime', 'visual'].includes(kind) && head && String(manifest.commit || '').toLowerCase() !== head) return fail('Evidence commit does not match the audited HEAD.');
  const runtimeExtensions = new Set(['.json', '.xml', '.zip', '.har', '.trace', '.mp4', '.mov']);
  for (const artifact of manifest.artifacts) {
    if (!artifact || typeof artifact !== 'object') return fail('Invalid artifact entry.');
    if (artifact.path) {
      const unresolved = path.resolve(path.dirname(manifestPath), String(artifact.path));
      if (!inside(root, unresolved) || !fs.existsSync(unresolved)) return fail('Local artifacts must stay inside the audited project.');
      const artifactPath = fs.realpathSync(unresolved);
      if (!inside(root, artifactPath) || !fs.statSync(artifactPath).isFile() || fs.statSync(artifactPath).size === 0) return fail('Local artifact is missing, empty, or escapes through a symlink.');
      if (!/^[a-f0-9]{64}$/i.test(artifact.sha256 || '') || sha256(artifactPath) !== artifact.sha256.toLowerCase()) return fail('Local artifact SHA-256 mismatch.');
      if (kind === 'visual' && !validVisualFile(artifactPath)) return fail('Visual artifact has no recognized image, video, trace, or archive signature.');
      if (kind === 'runtime') {
        if (!runtimeExtensions.has(path.extname(artifactPath).toLowerCase())) return fail('Runtime evidence must be a structured test, trace, HAR, video, or JSON artifact.');
        if (path.extname(artifactPath).toLowerCase() === '.json') {
          let runtime;
          try { runtime = JSON.parse(fs.readFileSync(artifactPath, 'utf8').replace(/^\uFEFF/, '')); } catch { return fail('Runtime JSON artifact is invalid.'); }
          if (runtime.shipvitals_runtime !== 1 || runtime.exit_code !== 0 || (head && String(runtime.commit || '').toLowerCase() !== head)) return fail('Runtime JSON is not a passing commit-bound execution record.');
        }
      }
    } else if (artifact.url) {
      if (kind !== 'ci') return fail('Remote artifacts are not accepted without local digest verification.');
      if (String(artifact.url) !== String(manifest.run_url)) return fail('CI artifact URL must equal run_url.');
    } else {
      return fail('Each artifact requires path or url.');
    }
  }

  if (kind === 'ci') {
    const reason = await verifyCiProvenance(root, manifest);
    if (reason) return fail(reason);
  }
  if (kind === 'independent_review') {
    if (manifest.decision !== 'accept' || typeof manifest.reviewer !== 'string' || manifest.reviewer.trim().length < 3) return fail('Independent evidence requires an identified reviewer and accept decision.');
    const reason = await verifyIndependentProvenance(root, manifest);
    if (reason) return fail(reason);
  }
  return { accepted: true };
}

async function validateEvidence(root, values, kind) {
  const valid = [];
  const rejected = [];
  const details = [];
  for (const value of asList(values)) {
    const result = await validateManifest(root, value, kind);
    (result.accepted ? valid : rejected).push(value);
    if (!result.accepted) details.push({ value, reason: result.reason });
  }
  return { valid, rejected, details };
}

function pathParts(value) {
  return new Set(String(value).replaceAll('\\', '/').toLowerCase().split('/').filter(Boolean));
}

function intersects(parts, candidates) {
  return [...parts].some(part => candidates.has(part));
}

function isNonBlockingSecret(file) {
  const parts = pathParts(file);
  return intersects(parts, NON_BLOCKING_EVIDENCE_PARTS)
    || intersects(parts, NON_BLOCKING_SECRET_PARTS)
    || NON_BLOCKING_SECRET_FILES.has(path.basename(file).toLowerCase());
}

function isCoreFake(file) {
  const parts = pathParts(file);
  if (intersects(parts, NON_BLOCKING_EVIDENCE_PARTS) || intersects(parts, NON_BLOCKING_FAKE_PARTS)) return false;
  return intersects(parts, CORE_FAKE_PARTS) || CORE_SUFFIXES.has(path.extname(file).toLowerCase());
}

function isUiProject(config) {
  const type = String(config.project?.type || '').toLowerCase();
  return UI_TYPE_KEYWORDS.some(keyword => type.includes(keyword));
}

function isHighStakes(config) {
  const project = config.project || {};
  const text = ['type', 'audience', 'destination', 'promise'].map(key => String(project[key] || '')).join(' ').toLowerCase();
  return HIGH_STAKES_KEYWORDS.some(keyword => text.includes(keyword));
}

function writeReport(root, report, ci) {
  const output = path.join(root, '.shipvitals-evidence');
  fs.mkdirSync(output, { recursive: true });
  const reportText = `${JSON.stringify(report, null, 2)}\n`;
  fs.writeFileSync(path.join(output, 'report.json'), reportText);
  fs.writeFileSync(path.join(output, 'shipvitals-report.json'), reportText);
  const summary = `# ShipVitals Summary\n\nVerdict: **${report.verdict}**\n\n- Score: ${report.score}\n- P0: ${report.p0.length}\n- P1: ${report.p1.length}\n- Commands: ${report.commands_detected.length}\n- Secret candidates: ${report.secret_candidates.length}\n- Fake-completion candidates: ${report.fake_completion_candidates.length}\n- Not verified: ${report.not_verified.length ? report.not_verified.join(', ') : 'none'}\n\nSee \`report.json\`.\n`;
  fs.writeFileSync(path.join(output, 'summary.md'), summary);
  fs.writeFileSync(path.join(output, 'shipvitals-summary.md'), summary);
  return ci ? report : { status: 'ok', verdict: report.verdict, out: output, p0: report.p0.length, p1: report.p1.length };
}

async function audit(options) {
  const root = path.resolve(options.project || '.');
  const { config, exists: configExists } = loadConfig(root);
  let commands = Object.values(config.commands || {});
  if (!commands.length) commands = detectCommands(root);
  if (options.mode !== 'deep') commands = commands.slice(0, 4);
  const results = commands.map(command => runCommand(command, root, options.timeout || 120, options.verbose));
  const secretScan = scan(root, SECRET_PATTERNS, config.exclude, item => !isNonBlockingSecret(item.file));
  const secrets = secretScan.findings;
  const fakeScan = scan(root, FAKE_PATTERNS, config.exclude, item => isCoreFake(item.file));
  const fake = fakeScan.findings;
  const failed = results.filter(result => result.exit_code !== 0);
  const suppliedProof = {
    runtime: [...asList(config.evidence?.runtime), ...asList(options.runtimeProof)],
    visual: [...asList(config.evidence?.visual), ...asList(options.visualProof)],
    ci: [...asList(config.evidence?.ci), ...asList(options.ciProof)],
    independent_review: [...asList(config.evidence?.independent_review), ...asList(options.independentReview)],
  };
  const checkedProof = {};
  for (const [key, values] of Object.entries(suppliedProof)) {
    checkedProof[key] = await validateEvidence(root, values, key);
  }
  const proof = Object.fromEntries(Object.entries(checkedProof).map(([key, value]) => [key, value.valid]));
  const rejectedProof = Object.fromEntries(Object.entries(checkedProof).map(([key, value]) => [key, value.rejected]));
  const evidenceLevels = ['L1_STATIC'];
  if (results.length && results.every(result => result.exit_code !== null)) evidenceLevels.push('L2_DETERMINISTIC');
  if (proof.runtime.length) evidenceLevels.push('L3_RUNTIME');
  if (proof.visual.length) evidenceLevels.push('L4_VISUAL_FLOW');
  if (proof.ci.length) evidenceLevels.push('L5_CI_REPRODUCIBLE');
  if (proof.independent_review.length) evidenceLevels.push('L6_INDEPENDENT');

  const p0 = [];
  const p1 = [];
  const caps = [];
  const cap = (maxScore, reason) => caps.push({ max_score: maxScore, reason });
  if (!hasProductPromise(config)) {
    p0.push('Missing product promise or critical flows.');
    cap(74, 'No product promise or critical flows.');
  }
  const blockingSecrets = secrets.filter(item => !isNonBlockingSecret(item.file));
  const blockingFake = fake.filter(item => isCoreFake(item.file));
  if (blockingSecrets.length) {
    p0.push('Secret candidates found.');
    cap(59, 'Secret candidates found.');
  }
  if (failed.length) {
    p1.push('One or more project commands failed.');
    cap(89, 'One or more deterministic commands failed.');
  }
  if (!results.length) cap(69, 'No deterministic command output.');
  const needsRuntime = Boolean(config.project?.critical_flows?.length);
  const needsVisual = isUiProject(config);
  const needsIndependent = isHighStakes(config);
  const notVerified = [];
  if (needsRuntime && !proof.runtime.length) {
    notVerified.push('runtime proof');
    cap(89, 'Runtime proof missing for critical flows.');
  }
  if (needsVisual && !proof.visual.length) {
    notVerified.push('visual proof');
    cap(74, 'UI project missing visual proof.');
  }
  if (!proof.independent_review.length) {
    notVerified.push('independent review');
    if (needsIndependent) cap(89, 'High-stakes release missing independent review.');
  }
  const demoOnly = fakeScan.priorityPatterns.some(pattern => ['demo only', 'mock data'].some(signal => pattern.toLowerCase().includes(signal)));
  if (demoOnly) cap(69, 'Demo-only or mock-data signal found.');
  const verdict = p0.length
    ? 'NOT READY'
    : demoOnly
      ? 'DEMO ONLY'
      : p1.length || !results.length || (needsRuntime && !proof.runtime.length) || (needsVisual && !proof.visual.length) || (needsIndependent && !proof.independent_review.length)
        ? 'ALMOST READY'
        : 'READY';
  const score = Math.min(100, ...caps.map(item => item.max_score));
  const report = {
    tool: 'ShipVitals', version: VERSION, generated_at: new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
    project: root, mode: options.mode || 'quick', config_exists: configExists,
    product_type: String(config.project?.type || '').toLowerCase(), product_promise_present: hasProductPromise(config),
    commands_detected: commands, command_results: results, secret_candidates: secrets.slice(0, 80),
    blocking_secret_candidates: blockingSecrets.slice(0, 80), fake_completion_candidates: fake.slice(0, 160),
    blocking_fake_completion_candidates: blockingFake.slice(0, 80), proof, rejected_proof: rejectedProof,
    rejected_proof_details: Object.fromEntries(Object.entries(checkedProof).map(([key, value]) => [key, value.details])),
    scan_stats: { secret_priority_count: secretScan.priorityCount, fake_priority_count: fakeScan.priorityCount }, evidence_levels: evidenceLevels,
    score, score_caps: caps, p0, p1, verdict, not_verified: notVerified,
  };
  return writeReport(root, report, options.ci);
}

module.exports = { VERSION, DEFAULT_CONFIG, audit };
