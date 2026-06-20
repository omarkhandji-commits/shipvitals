#!/usr/bin/env python3
from pathlib import Path
import sys
out=Path(sys.argv[1] if len(sys.argv)>1 else 'tests/shipvitals.visual.spec.ts')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text("""
import { test, expect } from '@playwright/test';

const BASE = process.env.PV_BASE_URL || 'http://localhost:3000';
const paths = (process.env.PV_PATHS || '/').split(',');

for (const path of paths) {
 test(`ShipVitals visual gate ${path}`, async ({ page }) => {
 const errors: string[] = [];
 page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
 page.on('pageerror', err => errors.push(err.message));
 await page.setViewportSize({ width: 1440, height: 1000 });
 await page.goto(BASE + path, { waitUntil: 'networkidle' });
 await page.screenshot({ path: `shipvitals-desktop-${path.replace(/[^a-z0-9]/gi,'_')}.png`, fullPage: true });
 await page.setViewportSize({ width: 390, height: 844 });
 await page.goto(BASE + path, { waitUntil: 'networkidle' });
 await page.screenshot({ path: `shipvitals-mobile-${path.replace(/[^a-z0-9]/gi,'_')}.png`, fullPage: true });
 expect(errors, 'console/page errors').toEqual([]);
 });
}
""")
print(f'Generated {out}')
