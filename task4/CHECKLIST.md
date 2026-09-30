# Riverbend Boutique — Task 4 Deployment Checklist

## Purpose

This checklist records the mitigation, verification, documentation, and handover tasks completed for Task 4.

## Lab and Scope

- [x] Confirm work was performed in the isolated Riverbend lab environment.
- [x] Confirm no external systems were targeted.
- [x] Review the Task 3 STRIDE threat model and risk-ranking.csv.
- [x] Identify the top five risks using the existing risk ranking.

## Risk Mitigations

- [x] Risk 1 — Document SQL injection prevention using prepared statements and parameterized queries.
- [x] Risk 1 — Apply least privilege to the application database account.
- [x] Risk 2 — Review NGINX handling of malicious HTTP parameters and paths.
- [x] Risk 2 — Confirm unknown paths are rejected by the NGINX configuration.
- [x] Risk 3 — Configure NGINX request rate limiting.
- [x] Risk 3 — Perform rapid-request validation.
- [x] Risk 3 — Confirm rate-limit events appear in NGINX logs.
- [x] Risk 4 — Restrict access to administrative functionality.
- [x] Risk 4 — Document application-level authentication and authorisation requirements for future administration features.
- [x] Risk 5 — Block restricted `/admin` paths at the NGINX layer.
- [x] Risk 5 — Verify `/admin` returns HTTP 403.

## Additional Security Controls

- [x] Add `X-Content-Type-Options` security header.
- [x] Add `X-Frame-Options` security header.
- [x] Add `Referrer-Policy` security header.
- [x] Add `Permissions-Policy` security header.
- [x] Verify security headers with `curl -I`.
- [x] Validate NGINX configuration with `sudo nginx -t`.
- [x] Perform a negative-control NGINX configuration test.

## Evidence

- [x] Save administrative-path mitigation evidence.
- [x] Save rate-limit test evidence.
- [x] Save NGINX rate-limit log evidence.
- [x] Copy evidence files into `task4/evidence/`.
- [x] Verify evidence files exist in the repository.

## Application Regression Testing

- [x] Confirm Riverbend Boutique page loads successfully.
- [x] Confirm the expected product list is displayed.
- [x] Confirm application still works after database least-privilege changes.
- [x] Confirm security headers do not prevent normal application access.

## Demo and Final Handover

- [ ] Record a short mitigation demonstration of no more than 5 minutes.
- [ ] Demonstrate at least one mitigation being applied and verified in the lab.
- [ ] Add the final demo video or demo link to the repository.
- [ ] Update the main README with the Task 4 executive summary and artefact links.
- [ ] Review all Task 4 documentation for clarity and consistency.
- [ ] Review `git status` before final submission.
- [ ] Commit the completed Task 4 artefacts.
- [ ] Push the final repository changes to GitHub.

## Production Deployment Checks

- [ ] Confirm production values for the NGINX rate limit are approved.
- [ ] Confirm all administrative endpoints require application-level authentication and authorisation.
- [ ] Confirm database accounts follow least-privilege principles.
- [ ] Confirm secrets are stored securely and are not exposed in source control.
- [ ] Confirm TLS/HTTPS is enabled for production.
- [ ] Confirm centralised logging and monitoring are available.
- [ ] Confirm backup and rollback procedures are documented.

## Final Status

Task 4 implementation and evidence preparation are substantially complete. The remaining unchecked items require final demo recording, README updates, repository review, and final submission.
