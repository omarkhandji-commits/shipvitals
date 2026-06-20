import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const workspace = fs.mkdtempSync(path.join(os.tmpdir(), 'shipvitals-package-'));
const project = path.join(workspace, 'fixture');
fs.mkdirSync(project);

const run = (command, args, cwd) => {
  const isWindows = process.platform === 'win32';
  const npmEntry = isWindows
    ? path.join(path.dirname(process.execPath), 'node_modules', 'npm', 'bin', command === 'npx' ? 'npx-cli.js' : 'npm-cli.js')
    : null;
  const executable = npmEntry && fs.existsSync(npmEntry) ? process.execPath : command;
  const commandArgs = npmEntry && fs.existsSync(npmEntry) ? [npmEntry, ...args] : args;
  const result = spawnSync(executable, commandArgs, { cwd, encoding: 'utf8', timeout: 120_000 });
  if (result.status !== 0) {
    throw new Error(`${command} ${args.join(' ')} failed\n${result.error?.message || ''}\n${result.stdout || ''}\n${result.stderr || ''}`);
  }
  return result.stdout;
};

const packed = JSON.parse(run('npm', ['pack', '--json', '--pack-destination', workspace], root));
const tarball = path.join(workspace, packed[0].filename);
fs.writeFileSync(path.join(project, 'package.json'), JSON.stringify({
  name: 'shipvitals-smoke-fixture',
  private: true,
  scripts: { test: 'node -e "process.exit(0)"' },
}, null, 2));
fs.writeFileSync(path.join(project, '.shipvitals-config.json'), JSON.stringify({
  project: {
    name: 'shipvitals-smoke-fixture',
    type: 'cli',
    audience: 'developers',
    destination: 'internal use',
    promise: 'Prove that the packed npm CLI runs.',
    critical_flows: ['npm test'],
  },
  evidence: {},
  commands: {},
  exclude: ['node_modules'],
}, null, 2));
fs.writeFileSync(path.join(project, 'index.js'), 'module.exports = true;\n');
fs.writeFileSync(path.join(project, 'runtime-proof.txt'), 'packed CLI smoke test\n');

run('npm', ['install', '--ignore-scripts', tarball], project);
run('npx', ['--no-install', 'shipvitals', 'audit', '.', '--runtime-proof', 'runtime-proof.txt'], project);

const report = JSON.parse(fs.readFileSync(path.join(project, '.shipvitals-evidence', 'report.json'), 'utf8'));
assert.equal(report.verdict, 'READY');
assert.equal(report.p0.length, 0);
assert.equal(report.p1.length, 0);
assert.equal(report.command_results[0].exit_code, 0);
process.stdout.write(`npm package smoke passed: ${packed[0].filename}\n`);
