const assert = require('node:assert/strict');
const { execFileSync, spawnSync } = require('node:child_process');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const CLI = path.resolve(__dirname, '..', 'cli', 'bin', 'shipvitals.js');

function evidence(root, kind, artifactName) {
  const artifact = path.join(root, artifactName);
  const manifestName = kind + '.shipvitals-evidence.json';
  fs.writeFileSync(path.join(root, manifestName), JSON.stringify({
    shipvitals_evidence: 1,
    kind,
    observed_at: '2026-06-22T12:00:00Z',
    source: 'node-test',
    summary: 'Deterministic fixture evidence observed by the Node integration test.',
    artifacts: [{
      path: artifactName,
      sha256: crypto.createHash('sha256').update(fs.readFileSync(artifact)).digest('hex'),
    }],
  }));
  return manifestName;
}

function fixture(type = 'cli') {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'shipvitals-node-'));
  fs.mkdirSync(path.join(root, 'src'));
  fs.writeFileSync(path.join(root, 'package.json'), JSON.stringify({ scripts: { test: 'node -e "process.exit(0)"' } }));
  fs.writeFileSync(path.join(root, '.shipvitals-config.json'), JSON.stringify({
    project: { name: 'fixture', type, audience: 'developers', destination: 'internal use', promise: 'Run a deterministic fixture.', critical_flows: ['test command'] },
    commands: {}, evidence: {}, exclude: ['node_modules'],
  }));
  fs.writeFileSync(path.join(root, 'src', 'index.js'), 'module.exports = true;\n');
  fs.writeFileSync(path.join(root, 'runtime-proof.json'), JSON.stringify({ shipvitals_runtime: 1, exit_code: 0, observations: ['fixture command observed'] }));
  evidence(root, 'runtime', 'runtime-proof.json');
  return root;
}

function run(args) {
  return JSON.parse(execFileSync(process.execPath, [CLI, ...args, '--no-fail'], { encoding: 'utf8' }));
}

test('npm CLI audits a Node project without invoking Python', () => {
  const root = fixture();
  const result = run(['audit', root, '--runtime-proof', 'runtime.shipvitals-evidence.json']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'READY');
  assert.equal(report.score, 100);
  assert.deepEqual(report.commands_detected, ['npm run test']);
  assert.equal(report.command_results[0].exit_code, 0);
});

test('npm CLI blocks a secret candidate in source', () => {
  const root = fixture();
  fs.writeFileSync(path.join(root, 'src', 'index.js'), 'const apiKey = "sk-abcdefghijklmnopqrstuvwxyz";\n');
  const result = run(['audit', root, '--runtime-proof', 'runtime.shipvitals-evidence.json']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'NOT READY');
  assert.equal(report.score, 59);
  assert.equal(report.p0.length, 1);
});

test('npm CLI requires visual proof for UI projects', () => {
  const root = fixture('saas web app');
  const result = run(['audit', root, '--runtime-proof', 'runtime.shipvitals-evidence.json']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'ALMOST READY');
  assert.equal(report.score, 74);
  assert.ok(report.not_verified.includes('visual proof'));
});

test('npm CLI writes a non-interactive config', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'shipvitals-init-'));
  execFileSync(process.execPath, [CLI, 'init', root, '--non-interactive']);
  const config = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-config.json')));
  assert.equal(config.project.name, path.basename(root));
  assert.equal(config.version, 1);
});

test('npm CLI treats a command timeout as a failed deterministic check', () => {
  const root = fixture();
  const configPath = path.join(root, '.shipvitals-config.json');
  const config = JSON.parse(fs.readFileSync(configPath));
  config.commands = { timeout: 'node -e "setTimeout(() => {}, 1000)"' };
  fs.writeFileSync(configPath, JSON.stringify(config));
  const result = run(['audit', root, '--timeout', '0.05', '--runtime-proof', 'runtime.shipvitals-evidence.json']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'ALMOST READY');
  assert.equal(report.p1.length, 1);
  assert.equal(report.command_results[0].exit_code, null);
  assert.ok(!report.evidence_levels.includes('L2_DETERMINISTIC'));
});

test('npm CLI retains a distinct core blocker after 300 core findings', () => {
  const root = fixture();
  fs.writeFileSync(path.join(root, 'src', 'a-noise.js'), '// TODO\n'.repeat(350));
  fs.writeFileSync(path.join(root, 'src', 'z-blocker.js'), 'module.exports = "mock data";\n');
  const result = run(['audit', root, '--runtime-proof', 'runtime.shipvitals-evidence.json']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'DEMO ONLY');
  assert.ok(report.scan_stats.fake_priority_count > 300);
  assert.ok(report.blocking_fake_completion_candidates.some(item => item.file.replaceAll('\\', '/') === 'src/z-blocker.js'));
});

test('npm CLI rejects existing arbitrary files as every proof level', () => {
  const root = fixture();
  const configPath = path.join(root, '.shipvitals-config.json');
  const config = JSON.parse(fs.readFileSync(configPath));
  config.project.destination = 'public release';
  fs.writeFileSync(configPath, JSON.stringify(config));
  const result = run(['audit', root, '--runtime-proof', 'package.json', '--visual-proof', 'package.json', '--ci-proof', 'package.json', '--independent-review', 'package.json']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'ALMOST READY');
  assert.deepEqual(report.rejected_proof.runtime, ['package.json']);
  for (const level of ['L3_RUNTIME', 'L4_VISUAL_FLOW', 'L5_CI_REPRODUCIBLE', 'L6_INDEPENDENT']) assert.ok(!report.evidence_levels.includes(level));
});

test('npm CLI exits nonzero when the verdict blocks release', () => {
  const root = fixture();
  fs.writeFileSync(path.join(root, 'src', 'index.js'), 'const token = "sk-abcdefghijklmnopqrstuvwxyz";\n');
  const result = spawnSync(process.execPath, [CLI, 'audit', root, '--runtime-proof', 'runtime.shipvitals-evidence.json'], { encoding: 'utf8' });
  assert.equal(result.status, 1);
  assert.equal(JSON.parse(result.stdout).verdict, 'NOT READY');
});
test('npm CLI rejects forged remote evidence and fake visual bytes', () => {
  const root = fixture('saas web app');
  fs.writeFileSync(path.join(root, 'fake.png'), 'not an image');
  evidence(root, 'visual', 'fake.png');
  fs.writeFileSync(path.join(root, 'remote.shipvitals-evidence.json'), JSON.stringify({
    shipvitals_evidence: 1,
    kind: 'runtime',
    observed_at: '2026-06-22T12:00:00Z',
    source: 'attacker',
    summary: 'A remote URL with a declared but unverified digest.',
    artifacts: [{ url: 'https://example.com/fake.zip', sha256: 'a'.repeat(64) }],
  }));
  const result = run([
    'audit', root,
    '--runtime-proof', 'remote.shipvitals-evidence.json',
    '--visual-proof', 'visual.shipvitals-evidence.json',
  ]);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'ALMOST READY');
  assert.ok(!report.evidence_levels.includes('L3_RUNTIME'));
  assert.ok(!report.evidence_levels.includes('L4_VISUAL_FLOW'));
  assert.match(report.rejected_proof_details.runtime[0].reason, /Remote artifacts are not accepted/);
  assert.match(report.rejected_proof_details.visual[0].reason, /recognized/);
});

test('npm CLI handles BOM config and rejects impossible timestamps', () => {
  const root = fixture();
  const configPath = path.join(root, '.shipvitals-config.json');
  fs.writeFileSync(configPath, '\ufeff' + fs.readFileSync(configPath, 'utf8'));
  const manifestPath = path.join(root, 'runtime.shipvitals-evidence.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath));
  manifest.observed_at = '2026-99-99T99:99:99Z';
  fs.writeFileSync(manifestPath, JSON.stringify(manifest));
  const result = run(['audit', root, '--runtime-proof', 'runtime.shipvitals-evidence.json']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'ALMOST READY');
  assert.ok(!report.evidence_levels.includes('L3_RUNTIME'));
  assert.match(report.rejected_proof_details.runtime[0].reason, /valid UTC timestamp/);
});
