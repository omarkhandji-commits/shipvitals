#!/usr/bin/env python3
import shutil, sys, json, platform
from pathlib import Path
project=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
tools=['node','npm','pnpm','yarn','bun','python3','pytest','git','npx','docker']
print(json.dumps({
 'project':str(project),
 'platform':platform.platform(),
 'tools':{t:shutil.which(t) for t in tools},
 'config_exists':(project/'.shipvitals-config.json').exists(),
 'package_json':(project/'package.json').exists(),
 'pyproject':(project/'pyproject.toml').exists()
}, indent=2))
