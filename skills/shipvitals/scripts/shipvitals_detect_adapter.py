#!/usr/bin/env python3
from pathlib import Path
import json, sys
project=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
adapters=[]
checks={
 'nextjs':['next.config.js','next.config.mjs','app','pages'],
 'shopify':['shopify.app.toml','extensions'],
 'django':['manage.py'],
 'fastapi':['main.py','pyproject.toml'],
 'remix':['remix.config.js','app/root.tsx'],
 'laravel':['artisan'],
 'rails':['Gemfile','config/routes.rb'],
}
for name, markers in checks.items():
    if any((project/m).exists() for m in markers): adapters.append(name)
print(json.dumps({'project':str(project),'adapters':adapters}, indent=2))
