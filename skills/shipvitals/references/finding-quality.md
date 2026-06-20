# Finding Quality Standard

Every finding must be actionable.

Required fields:

- severity: P0/P1/P2/P3;
- area: code, UI, mobile, security, product, docs, launch, client delivery, marketplace;
- location: file path, URL, screenshot, command, or flow;
- evidence: observed proof or command output;
- why it matters: user/client/business risk;
- smallest fix: the minimum correction required;
- owner/tool: developer, designer, Claude Code, Codex, security reviewer, Playwright, etc.;
- retest command: exact command or manual retest step.

Bad: "Improve UI." 
Good: "P1 mobile: `/pricing` CTA wraps below the fold at 390px width, screenshot `mobile-pricing.png`; users cannot see checkout CTA. Fix button layout and retest with Playwright mobile viewport."
