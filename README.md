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
