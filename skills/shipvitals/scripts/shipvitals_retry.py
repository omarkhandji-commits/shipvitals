#!/usr/bin/env python3
import argparse, subprocess, sys
ap=argparse.ArgumentParser()
ap.add_argument('command', nargs='+')
ap.add_argument('--timeout', type=int, default=180)
args=ap.parse_args()
cmd=' '.join(args.command)
r=subprocess.run(cmd, shell=True, text=True, timeout=args.timeout)
sys.exit(r.returncode)
