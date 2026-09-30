# Riverbend Boutique — Threat Modelling Lab

## Scope
All work in this repository is performed inside an isolated lab VM (Kali, host-only network).
No external systems are targeted.

## Stack
- NGINX (port 80)
- PHP 8.4-FPM
- MariaDB 11.8 (database: riverbend_shop, user: shopuser)

## Lab Setup Steps
1. NGINX install + PHP-FPM integration
2. MariaDB install + secure-installation
3. riverbend_shop DB + products table with sample data
4. index.php renders products from DB
5. VM snapshot taken (`shop-stack-complete`) and restored once to verify

## Files
- `configs/nginx-default.conf` — NGINX server block
- `configs/mariadb-setup.sql` — DB schema + seed data
- `app/index.php` — shop page

## Network Isolation
Host-only adapter; no NAT/bridged. `ping 8.8.8.8` fails from inside the VM.

## Task 3 — STRIDE Threat Model

The Riverbend Boutique system was analysed using the STRIDE threat-modelling methodology. The model covers the client, NGINX web server, PHP application, MariaDB database, and external services.

### Task 3 Artefacts

- `task3/diagram.svg` — System architecture diagram showing the main components, data flows, and lab/application boundary.
- `task3/THREAT_MODEL.md` — STRIDE threat model with threats covering all six STRIDE categories for each component, including likelihood, impact, and risk score.
- `task3/risk-ranking.csv` — Risk ranking using the formula `Likelihood × Impact`, sorted from highest to lowest score.
- `task3/threat-model.pdf` — PDF export of the STRIDE threat model, architecture, risk ranking, observed findings, and methodology.
- `task3/create_pdf.py` — Python script used to generate the threat-model PDF.

### Observed Log Findings

The threat model also considers the suspicious activity identified during log analysis, including SQL injection-like input, `/admin` probing, `/wp-login.php` probing, and `/etc/passwd` probing.

## Task 4 — Mitigation Plan and Final Handover

### Executive Summary

Task 4 converted the highest-scoring risks from the STRIDE threat model into concrete mitigation and verification steps. The work was performed inside the isolated Riverbend Boutique lab.

The implemented controls include NGINX administrative-path restriction, HTTP request rate limiting, security response headers, and least-privilege database access. The SQL injection risk was documented as a secure-development requirement using prepared statements and parameterized queries for future dynamic database inputs. The current application uses a fixed SQL query and does not expose a live user-controlled SQL injection parameter.

The mitigations were validated without breaking the normal storefront. The `/admin` path returned HTTP 403, rapid requests triggered the configured NGINX rate limit, security headers were present in HTTP responses, and the application continued to display the expected product data after the database privilege reduction.

### Top 5 Risks Addressed

1. SQL injection-like input modifies application behaviour — Score 20
2. Malicious HTTP parameters or paths are submitted — Score 16
3. Excessive HTTP requests exhaust web-server resources — Score 16
4. Client attempts to access administrative functionality — Score 15
5. Attacker attempts to reach restricted administrative paths — Score 15

### Task 4 Artefacts

- `task4/MITIGATIONS.md` — Detailed mitigation plan, configuration changes, expected impact, verification, and limitations.
- `task4/CHECKLIST.md` — Deployment, verification, evidence, and final handover checklist.
- `task4/DEMO_SCRIPT.md` — Short demonstration script for the mitigation video.
- `task4/evidence/riverbend-admin-mitigation.txt` — Administrative-path mitigation validation.
- `task4/evidence/riverbend-rate-limit-test.txt` — Rate-limit validation results.
- `task4/evidence/riverbend-rate-limit-nginx-log.txt` — NGINX rate-limit log evidence.

### Implemented and Verified Controls

- NGINX returns HTTP 403 for the restricted `/admin` path.
- NGINX rate limiting is configured at `5r/s` with a burst of `10` requests.
- Rapid-request testing produced both successful responses and rate-limited HTTP 503 responses.
- NGINX recorded rate-limit events in its error log.
- Security response headers were verified with `curl -I`.
- The application database account was reduced from full database privileges to SELECT-only access.
- The normal storefront was regression-tested after the database privilege change.
- NGINX configuration syntax was validated with `sudo nginx -t`.
- An intentionally invalid NGINX configuration was tested as a negative control and correctly rejected.

### Demo

The final demonstration video should be kept at 5 minutes or less and should show one mitigation being applied or active and then verified in the lab.

After recording, add the video as `task4/demo.mp4` or replace this section with the submitted video link.

### Final Handover

The `task4/` directory contains the mitigation documentation, deployment checklist, demonstration script, and supporting evidence for final review.
