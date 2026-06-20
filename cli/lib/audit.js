const { spawnSync } = require('node:child_process');
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
  const loaded = JSON.parse(fs.readFileSync(configPath, 'utf8'));
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
          if (priorityFindings.length < 300) priorityFindings.push(finding);
        } else if (findings.length < 300) {
          findings.push(finding);
        }
      }
    }
  }
  return [...priorityFindings, ...findings];
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

function validateEvidence(root, values) {
  const valid = [];
  const rejected = [];
  for (const value of asList(values)) {
    let accepted = false;
    try {
      const url = new URL(value);
      accepted = ['http:', 'https:'].includes(url.protocol) && Boolean(url.hostname);
    } catch {
      const candidate = path.isAbsolute(value) ? value : path.resolve(root, value);
      if (fs.existsSync(candidate)) {
        const stat = fs.statSync(candidate);
        accepted = stat.isFile() ? stat.size > 0 : stat.isDirectory() && fs.readdirSync(candidate).length > 0;
      }
    }
    (accepted ? valid : rejected).push(value);
  }
  return { valid, rejected };
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

function audit(options) {
  const root = path.resolve(options.project || '.');
  const { config, exists: configExists } = loadConfig(root);
  let commands = Object.values(config.commands || {});
  if (!commands.length) commands = detectCommands(root);
  if (options.mode !== 'deep') commands = commands.slice(0, 4);
  const results = commands.map(command => runCommand(command, root, options.timeout || 120, options.verbose));
  const secrets = scan(root, SECRET_PATTERNS, config.exclude, item => !isNonBlockingSecret(item.file));
  const fake = scan(root, FAKE_PATTERNS, config.exclude, item => isCoreFake(item.file));
  const failed = results.filter(result => result.exit_code !== 0);
  const suppliedProof = {
    runtime: [...asList(config.evidence?.runtime), ...asList(options.runtimeProof)],
    visual: [...asList(config.evidence?.visual), ...asList(options.visualProof)],
    ci: [...asList(config.evidence?.ci), ...asList(options.ciProof)],
    independent_review: [...asList(config.evidence?.independent_review), ...asList(options.independentReview)],
  };
  const checkedProof = Object.fromEntries(Object.entries(suppliedProof).map(([key, values]) => [key, validateEvidence(root, values)]));
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
  const demoOnly = blockingFake.some(item => ['demo only', 'mock data'].some(signal => item.pattern.toLowerCase().includes(signal)));
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
    blocking_fake_completion_candidates: blockingFake.slice(0, 80), proof, rejected_proof: rejectedProof, evidence_levels: evidenceLevels,
    score, score_caps: caps, p0, p1, verdict, not_verified: notVerified,
  };
  return writeReport(root, report, options.ci);
}

module.exports = { VERSION, DEFAULT_CONFIG, audit };
