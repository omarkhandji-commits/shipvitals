const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const CLI = path.resolve(__dirname, '..', 'cli', 'bin', 'shipvitals.js');

function fixture(type = 'cli') {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'shipvitals-node-'));
  fs.mkdirSync(path.join(root, 'src'));
  fs.writeFileSync(path.join(root, 'package.json'), JSON.stringify({ scripts: { test: 'node -e "process.exit(0)"' } }));
  fs.writeFileSync(path.join(root, '.shipvitals-config.json'), JSON.stringify({
    project: { name: 'fixture', type, audience: 'developers', destination: 'internal use', promise: 'Run a deterministic fixture.', critical_flows: ['test command'] },
    commands: {}, evidence: {}, exclude: ['node_modules'],
  }));
  fs.writeFileSync(path.join(root, 'src', 'index.js'), 'module.exports = true;\n');
  fs.writeFileSync(path.join(root, 'runtime-proof.txt'), 'fixture command observed\n');
  return root;
}

function run(args) {
  return JSON.parse(execFileSync(process.execPath, [CLI, ...args], { encoding: 'utf8' }));
}

test('npm CLI audits a Node project without invoking Python', () => {
  const root = fixture();
  const result = run(['audit', root, '--runtime-proof', 'runtime-proof.txt']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'READY');
  assert.equal(report.score, 100);
  assert.deepEqual(report.commands_detected, ['npm run test']);
  assert.equal(report.command_results[0].exit_code, 0);
});

test('npm CLI blocks a secret candidate in source', () => {
  const root = fixture();
  fs.writeFileSync(path.join(root, 'src', 'index.js'), 'const apiKey = "sk-abcdefghijklmnopqrstuvwxyz";\n');
  const result = run(['audit', root, '--runtime-proof', 'runtime-proof.txt']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'NOT READY');
  assert.equal(report.score, 59);
  assert.equal(report.p0.length, 1);
});

test('npm CLI requires visual proof for UI projects', () => {
  const root = fixture('saas web app');
  const result = run(['audit', root, '--runtime-proof', 'runtime-proof.txt']);
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
  const result = run(['audit', root, '--timeout', '0.05', '--runtime-proof', 'runtime-proof.txt']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'ALMOST READY');
  assert.equal(report.p1.length, 1);
  assert.equal(report.command_results[0].exit_code, null);
  assert.ok(!report.evidence_levels.includes('L2_DETERMINISTIC'));
});

test('npm CLI retains core blockers after low-priority scan saturation', () => {
  const root = fixture();
  fs.mkdirSync(path.join(root, 'docs'));
  fs.writeFileSync(path.join(root, 'docs', 'notes.md'), 'TODO\n'.repeat(350));
  fs.writeFileSync(path.join(root, 'src', 'index.js'), 'module.exports = "mock data";\n');
  const result = run(['audit', root, '--runtime-proof', 'runtime-proof.txt']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'DEMO ONLY');
  assert.ok(report.blocking_fake_completion_candidates.some(item => item.file.endsWith('src\\index.js') || item.file.endsWith('src/index.js')));
});

test('npm CLI rejects free-form proof strings', () => {
  const root = fixture();
  const configPath = path.join(root, '.shipvitals-config.json');
  const config = JSON.parse(fs.readFileSync(configPath));
  config.project.destination = 'public release';
  fs.writeFileSync(configPath, JSON.stringify(config));
  const result = run(['audit', root, '--runtime-proof', 'x', '--ci-proof', 'x', '--independent-review', 'x']);
  const report = JSON.parse(fs.readFileSync(path.join(root, '.shipvitals-evidence', 'report.json')));
  assert.equal(result.verdict, 'ALMOST READY');
  assert.deepEqual(report.rejected_proof.runtime, ['x']);
  assert.ok(!report.evidence_levels.includes('L3_RUNTIME'));
  assert.ok(!report.evidence_levels.includes('L5_CI_REPRODUCIBLE'));
  assert.ok(!report.evidence_levels.includes('L6_INDEPENDENT'));
});
