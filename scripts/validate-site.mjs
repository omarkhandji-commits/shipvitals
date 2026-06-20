import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..', 'website');
const publicPages = ['index.html', 'install/index.html', 'benchmarks/index.html', 'methodology/index.html', 'compare/index.html'];
const expectedBase = 'https://omarkhandji-commits.github.io/shipvitals/';

function resolveInternal(href, sourceFile) {
  const clean = href.split('#')[0].split('?')[0];
  if (!clean || clean.startsWith('http') || clean.startsWith('mailto:')) return null;
  const absoluteFromRoot = clean.startsWith('/shipvitals/');
  const relative = absoluteFromRoot ? clean.slice('/shipvitals/'.length) : clean;
  const candidate = path.resolve(absoluteFromRoot ? root : path.dirname(sourceFile), relative);
  return relative.endsWith('/') ? path.join(candidate, 'index.html') : candidate;
}

for (const relative of publicPages) {
  const file = path.join(root, relative);
  const html = fs.readFileSync(file, 'utf8');
  assert.match(html, /<html lang="en">/, `${relative}: missing language`);
  assert.match(html, /<title>[^<]{20,}[^<]*<\/title>/, `${relative}: weak title`);
  assert.match(html, /<meta name="description" content="[^\"]{80,}"/, `${relative}: weak description`);
  assert.match(html, /<link rel="canonical" href="https:\/\/omarkhandji-commits\.github\.io\/shipvitals\//, `${relative}: missing canonical`);
  for (const [, href] of html.matchAll(/href="([^"]+)"/g)) {
    const target = resolveInternal(href, file);
    if (target) assert.ok(fs.existsSync(target), `${relative}: broken link ${href}`);
  }
}

const homepage = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const jsonLd = homepage.match(/<script type="application\/ld\+json">(.+?)<\/script>/s);
assert.ok(jsonLd, 'homepage: missing JSON-LD');
assert.equal(JSON.parse(jsonLd[1])['@type'], 'SoftwareApplication');

const sitemap = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
for (const relative of ['', 'install/', 'benchmarks/', 'methodology/', 'compare/']) {
  assert.ok(sitemap.includes(`<loc>${expectedBase}${relative}</loc>`), `sitemap: missing ${relative || 'home'}`);
}
const robots = fs.readFileSync(path.join(root, 'robots.txt'), 'utf8');
assert.ok(robots.includes(`${expectedBase}sitemap.xml`), 'robots: sitemap URL mismatch');
assert.ok(fs.existsSync(path.join(root, 'assets', 'social-preview.png')), 'missing social preview');
process.stdout.write(`site validation passed: ${publicPages.length} public pages\n`);
