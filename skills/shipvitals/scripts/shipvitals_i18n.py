#!/usr/bin/env python3
import json, sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
text=' '.join(x.name for x in p.rglob('*') if x.is_file())[:10000]
lang='fr' if any(w in text.lower() for w in ['accueil','client','devis','facture']) else 'en'
print(json.dumps({'language_guess':lang}, indent=2))
