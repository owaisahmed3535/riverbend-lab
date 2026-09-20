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
