#!/usr/bin/env python3
import sys
from pathlib import Path
print('PDF export is optional. Generate HTML first, then print to PDF from a browser or install WeasyPrint/Playwright in your environment.')
if len(sys.argv)>1:
    p=Path(sys.argv[1]); print(f'Input: {p}')
