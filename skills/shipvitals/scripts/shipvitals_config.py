#!/usr/bin/env python3
import json
from pathlib import Path

DEFAULT_CONFIG = {
    'version': 1,
    'project': {'name': '', 'type': '', 'audience': '', 'destination': '', 'promise': '', 'critical_flows': []},
    'commands': {},
    'evidence': {'runtime': [], 'visual': [], 'ci': [], 'independent_review': []},
    'exclude': ['node_modules', 'dist', 'build', '.next', '.git'],
    'branding': {}
}

def config_path(project):
    return Path(project) / '.shipvitals-config.json'

def load_config(project):
    path = config_path(project)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save_config(project, config):
    path = config_path(project)
    path.write_text(json.dumps(config, indent=2) + '\n')
    return path

def merge_config(config):
    out = json.loads(json.dumps(DEFAULT_CONFIG))
    if config:
        for k, v in config.items():
            if isinstance(v, dict) and isinstance(out.get(k), dict):
                out[k].update(v)
            else:
                out[k] = v
    return out

def has_product_promise(config):
    if not config:
        return False
    project = config.get('project', {})
    return bool(project.get('promise') and project.get('critical_flows'))
