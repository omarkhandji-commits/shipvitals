#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from shipvitals_config import DEFAULT_CONFIG, save_config

QUESTIONS = [
    ('type', 'Project type'),
    ('audience', 'Target user/client'),
    ('destination', 'Next destination: public launch, client delivery, marketplace, internal use, demo'),
    ('promise', 'One-sentence product promise'),
    ('critical_flows', 'Critical flows, comma-separated'),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('project', nargs='?', default='.')
    ap.add_argument('--write-config', action='store_true')
    ap.add_argument('--non-interactive', action='store_true')
    args = ap.parse_args()
    project = Path(args.project).resolve()
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    cfg['project']['name'] = project.name
    if args.non_interactive:
        cfg['project'].update({'type':'unknown','audience':'unknown','destination':'unknown','promise':'To be defined before release.','critical_flows':[]})
    else:
        for key, label in QUESTIONS:
            value = input(f'{label}: ').strip()
            if key == 'critical_flows':
                cfg['project'][key] = [x.strip() for x in value.split(',') if x.strip()]
            else:
                cfg['project'][key] = value
    if args.write_config:
        path = save_config(project, cfg)
        print(f'Wrote {path}')
    else:
        print(json.dumps(cfg, indent=2))
if __name__ == '__main__': main()
