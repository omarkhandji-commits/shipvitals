#!/usr/bin/env python3
import sys
from pathlib import Path
from shipvitals_config import load_config, merge_config, save_config
project=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
cfg=merge_config(load_config(project))
cfg['version']=1
path=save_config(project,cfg)
print(f'Migrated {path}')
