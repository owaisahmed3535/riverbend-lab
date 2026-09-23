#!/bin/bash

# Riverbend Boutique - Task 2 Log Analysis
# Purpose: Extract suspicious requests and HTTP errors from lab logs.
# All analysis is performed on locally collected lab logs.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$REPO_DIR/logs"

echo "=========================================="
echo " Riverbend Boutique - Log Analysis"
echo "=========================================="
echo

echo "[1] HTTP 4xx/5xx Requests"
echo "------------------------------------------"

grep -hE '" [45][0-9][0-9] [0-9]+' "$LOG_DIR"/nginx-access.log* 2>/dev/null || \
echo "No HTTP 4xx/5xx requests found."

echo
echo "[2] SQL Injection-like Patterns"
echo "------------------------------------------"

grep -hiE 'SELECT|UNION|%27|%22|%3D|OR%20|AND%20|SLEEP|BENCHMARK' \
"$LOG_DIR"/nginx-access.log* 2>/dev/null || \
echo "No SQL injection-like patterns found."

echo
echo "[3] Administrative/Login Endpoint Probing"
echo "------------------------------------------"

grep -hiE '/admin|/login|wp-login|wp-admin' \
"$LOG_DIR"/nginx-access.log* 2>/dev/null || \
echo "No administrative/login probing found."

echo
echo "[4] Sensitive File / Path Traversal Probing"
echo "------------------------------------------"

grep -hiE '/etc/passwd|/etc/shadow|\.\./|%2e%2e|passwd' \
"$LOG_DIR"/nginx-access.log* 2>/dev/null || \
echo "No sensitive-file/path-traversal patterns found."

echo
echo "[5] HTTP Status Code Summary"
echo "------------------------------------------"

grep -hoE '" [0-9]{3} [0-9]+' "$LOG_DIR"/nginx-access.log* 2>/dev/null |
awk '{print $2}' |
sort |
uniq -c |
sort -nr

echo
echo "[6] MariaDB Log Summary"
echo "------------------------------------------"

if [ -s "$LOG_DIR/mariadb-journal.log" ]; then
    grep -hiE 'error|warning|failed|denied|ready for connections' \
    "$LOG_DIR/mariadb-journal.log" | tail -n 20
else
    echo "MariaDB journal log not found or empty."
fi

echo
echo "=========================================="
echo " Analysis complete."
echo "=========================================="
