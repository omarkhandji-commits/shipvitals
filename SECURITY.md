# Security

ShipVitals is a local audit tool. It should not send project files to a remote service unless the user explicitly chooses to do so through another tool.

Security baseline:

- scan for common secret patterns;
- flag risky environment files;
- mark authentication, authorization, and privacy checks as `NOT VERIFIED` if they were not tested;
- recommend specialist review for payment, healthcare, legal, financial, enterprise, or high-risk data flows.

To report a vulnerability in ShipVitals itself, [open a private security advisory](https://github.com/omarkhandji-commits/shipvitals/security/advisories/new). Do not include secrets or exploit details in a public issue.
