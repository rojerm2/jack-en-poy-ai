# Security policy

Security fixes target the current 1.1.x release. Earlier releases should be upgraded.

Report a suspected vulnerability through [GitHub private vulnerability reporting](https://github.com/rojerm2/jack-en-poy-ai/security/advisories/new).
Include the affected version, reproduction steps and likely impact. Do not include credentials or
unrelated personal data. Reports are reviewed as maintainer availability permits.

The default deployment is loopback-only and uses anonymous gameplay. Java and Python are not
published as host ports. Public self-hosting requires HTTPS, explicit allowed origins and an
operator-defined data-retention policy. There are no user accounts or authentication endpoints.

Model artifacts use Joblib and must be trusted. Do not load models received from unknown sources.
Training and model replacement are local/container-admin operations, not public HTTP endpoints.
The GitHub Pages demo makes no API requests and stores no gameplay outside the current page.
