# Error playbook

ShipVitals should keep moving without pretending that failed checks passed.

| Situation | Response |
|---|---|
| Node is missing | Mark JS build/test as `NOT VERIFIED`, suggest installing Node or using nvm. |
| Python is missing | Mark Python checks as `NOT VERIFIED`, suggest pyenv, uv, or system Python. |
| Dependencies are missing | Do not install without permission. Record the install command needed. |
| Command times out | Record timeout, lower evidence level, provide retry command. |
| Permission denied | Record path and command, suggest chmod only when safe. |
| No product promise | Run interview wizard before scoring. |
| No tests exist | Do not fail automatically, but cap verdict at `ALMOST READY` unless other proof exists. |
