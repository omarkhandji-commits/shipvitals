#!/usr/bin/env python3
import json, sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
files={x.name for x in p.iterdir()} if p.exists() else set()
stack=[]; managers=[]
if 'package.json' in files: stack.append('javascript/typescript')
if 'next.config.js' in files or 'next.config.mjs' in files: stack.append('nextjs')
if 'shopify.app.toml' in files: stack.append('shopify')
if 'pyproject.toml' in files: stack.append('python')
if 'manage.py' in files: stack.append('django')
if 'pnpm-lock.yaml' in files: managers.append('pnpm')
if 'yarn.lock' in files: managers.append('yarn')
if 'bun.lockb' in files: managers.append('bun')
if 'package-lock.json' in files: managers.append('npm')
if 'poetry.lock' in files: managers.append('poetry')
if 'Pipfile' in files: managers.append('pipenv')
monorepo=any((p/x).exists() for x in ['pnpm-workspace.yaml','turbo.json','lerna.json','nx.json'])
print(json.dumps({'project':str(p),'stack':stack,'package_managers':managers,'monorepo':monorepo}, indent=2))
