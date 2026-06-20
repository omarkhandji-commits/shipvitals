#!/usr/bin/env node
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const readline = require('node:readline/promises');
const { audit, DEFAULT_CONFIG, VERSION } = require('../lib/audit');

const HELP = `ShipVitals ${VERSION}

Usage:
  shipvitals audit [project] [--ci] [--mode quick|deep]
  shipvitals init [project] [--non-interactive]
  shipvitals diagnostics [project]

Audit proof flags:
  --runtime-proof "note, URL, path, or artifact"
  --visual-proof "screenshot, video, trace, or responsive proof"
  --ci-proof "CI run URL, hook output, or reproducibility artifact"
  --independent-review "second-auditor report or reviewer signoff"
`;

function parse(argv) {
  const options = {
    command: argv[0] || 'audit', project: '.', mode: 'quick', timeout: 120,
    runtimeProof: [], visualProof: [], ciProof: [], independentReview: [],
  };
  const valueFlags = new Map([
    ['--mode', 'mode'], ['--timeout', 'timeout'], ['--runtime-proof', 'runtimeProof'],
    ['--visual-proof', 'visualProof'], ['--ci-proof', 'ciProof'], ['--independent-review', 'independentReview'],
  ]);
  let projectSet = false;
  for (let index = 1; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--ci') options.ci = true;
    else if (arg === '--verbose') options.verbose = true;
    else if (arg === '--non-interactive') options.nonInteractive = true;
    else if (valueFlags.has(arg)) {
      const key = valueFlags.get(arg);
      const value = argv[index + 1];
      if (value === undefined) throw new Error(`${arg} requires a value`);
      index += 1;
      if (Array.isArray(options[key])) options[key].push(value);
      else options[key] = key === 'timeout' ? Number(value) : value;
    } else if (!arg.startsWith('-') && !projectSet) {
      options.project = arg;
      projectSet = true;
    }
    else if (!arg.startsWith('-')) throw new Error(`Unexpected positional argument: ${arg}`);
    else throw new Error(`Unknown option: ${arg}`);
  }
  if (!['quick', 'deep'].includes(options.mode)) throw new Error('--mode must be quick or deep');
  if (!Number.isFinite(options.timeout) || options.timeout <= 0) throw new Error('--timeout must be a positive number');
  return options;
}

async function init(options) {
  const project = path.resolve(options.project);
  const config = JSON.parse(JSON.stringify(DEFAULT_CONFIG));
  config.project.name = path.basename(project);
  if (options.nonInteractive) {
    Object.assign(config.project, { type: 'unknown', audience: 'unknown', destination: 'unknown', promise: 'To be defined before release.', critical_flows: [] });
  } else {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    config.project.type = (await rl.question('Project type: ')).trim();
    config.project.audience = (await rl.question('Target user/client: ')).trim();
    config.project.destination = (await rl.question('Next destination: ')).trim();
    config.project.promise = (await rl.question('One-sentence product promise: ')).trim();
    config.project.critical_flows = (await rl.question('Critical flows, comma-separated: ')).split(',').map(value => value.trim()).filter(Boolean);
    rl.close();
  }
  const output = path.join(project, '.shipvitals-config.json');
  fs.writeFileSync(output, `${JSON.stringify(config, null, 2)}\n`);
  process.stdout.write(`Wrote ${output}\n`);
}

function diagnostics(options) {
  const command = process.platform === 'win32' ? 'where' : 'which';
  const available = name => spawnSync(command, [name], { encoding: 'utf8' }).status === 0;
  process.stdout.write(`${JSON.stringify({
    project: path.resolve(options.project), platform: process.platform, node: process.version,
    tools: { npm: available('npm'), git: available('git'), python: available('python') || available('python3') },
  }, null, 2)}\n`);
}

async function main() {
  const argv = process.argv.slice(2);
  if (['help', '--help', '-h'].includes(argv[0])) {
    process.stdout.write(HELP);
    return;
  }
  const options = parse(argv);
  if (options.command === 'audit') process.stdout.write(`${JSON.stringify(audit(options), null, 2)}\n`);
  else if (['init', 'interview'].includes(options.command)) await init(options);
  else if (options.command === 'diagnostics') diagnostics(options);
  else throw new Error(`Unknown command: ${options.command}\n\n${HELP}`);
}

main().catch(error => {
  process.stderr.write(`ShipVitals: ${error.message}\n`);
  process.exitCode = 1;
});
