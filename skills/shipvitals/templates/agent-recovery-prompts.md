# Recovery prompts

- If a command fails because the package manager is missing: explain the missing tool and continue with static checks.
- If dependency install is needed: ask before installing unless the environment is explicitly disposable.
- If a test hangs: stop it, record the timeout, and continue with a lower evidence level.
- If the project has no product promise: run the interview wizard.
