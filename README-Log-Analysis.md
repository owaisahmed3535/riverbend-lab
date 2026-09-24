# Riverbend Boutique - Log Analysis Report

## 1. Objective

This report documents the analysis of locally collected Riverbend Boutique web, application, and database logs for Task 2.

The objective was to identify suspicious request patterns such as SQL injection-like requests, administrative/login endpoint probing, sensitive-file probing, and HTTP error responses.

All testing and log collection were performed inside the isolated Riverbend Boutique lab against `127.0.0.1`.

## 2. Log Sources

The following raw logs were collected under the `logs/` directory:

- `nginx-access.log`
- `nginx-access.log.1`
- `nginx-error.log`
- `nginx-error.log.1`
- `php8.4-fpm.log`
- `mariadb-journal.log`

The analysis was automated using `scripts/analyze_logs.sh`.

## 3. Analysis Method

The analysis script searches NGINX access logs for:

- HTTP 4xx and 5xx responses
- SQL injection-like patterns
- Administrative and login endpoint probing
- Sensitive-file and path-traversal patterns

It also provides an HTTP status-code summary and checks the MariaDB journal for relevant messages.

## 4. Suspicious Event 1 - SQL Injection-like Request

### Timestamp

`23/Sep/2026 10:10:07 -0400`

### Evidence

```text
127.0.0.1 - - [23/Sep/2026:10:10:07 -0400] "GET /?id=%27%20OR%20%271%27%3D%271 HTTP/1.1" 200 1614 "-" "curl/8.21.0"
