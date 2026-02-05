# Security Policy

## Reporting
If you discover a security issue, please open a private report with details and reproduction steps.

## Scope
KRUTI is a template-style repo. If you add networked tools (HTTP, filesystem writes, shell exec),
treat them as privileged and gate them behind allowlists, timeouts, and sanitization.
