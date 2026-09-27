# Riverbend Boutique - STRIDE Threat Model

## 1. Scope

This threat model is based on the Riverbend Boutique lab architecture and the log analysis results from Task 2.

Components analysed:

1. Client
2. NGINX Web Server
3. PHP Application
4. MariaDB Database
5. External Services

Risk score = Likelihood × Impact, using a 1-5 scale.

---

## 2. STRIDE Threat Table

| Component | STRIDE Category | Threat | Likelihood | Impact | Score |
|---|---|---|---:|---:|---:|
| Client | Spoofing | Attacker impersonates a legitimate client or user | 3 | 4 | 12 |
| Client | Tampering | Malicious client modifies request parameters | 4 | 3 | 12 |
| Client | Repudiation | User denies sending a malicious request | 2 | 3 | 6 |
| Client | Information Disclosure | Sensitive information is exposed through client responses | 3 | 3 | 9 |
| Client | Denial of Service | Client sends excessive requests to consume resources | 3 | 4 | 12 |
| Client | Elevation of Privilege | Client attempts to access administrative functionality | 3 | 5 | 15 |
| NGINX Web Server | Spoofing | Attacker spoofs a trusted request source | 3 | 4 | 12 |
| NGINX Web Server | Tampering | Malicious HTTP parameters or paths are submitted | 4 | 4 | 16 |
| NGINX Web Server | Repudiation | Request activity is disputed or insufficiently logged | 2 | 3 | 6 |
| NGINX Web Server | Information Disclosure | Error or configuration information is exposed | 3 | 4 | 12 |
| NGINX Web Server | Denial of Service | Excessive HTTP requests exhaust web-server resources | 4 | 4 | 16 |
| NGINX Web Server | Elevation of Privilege | Attacker attempts to reach restricted administrative paths | 3 | 5 | 15 |
| PHP Application | Spoofing | Attacker impersonates an application user | 3 | 4 | 12 |
| PHP Application | Tampering | SQL injection-like input modifies application behaviour | 4 | 5 | 20 |
| PHP Application | Repudiation | Application actions cannot be linked to a verified user | 2 | 3 | 6 |
| PHP Application | Information Disclosure | Application exposes sensitive data through responses | 3 | 5 | 15 |
| PHP Application | Denial of Service | Malicious requests consume PHP-FPM resources | 3 | 4 | 12 |
| PHP Application | Elevation of Privilege | Attacker attempts to access administrative functionality | 3 | 5 | 15 |
| MariaDB Database | Spoofing | Unauthorized actor attempts to authenticate as a database user | 3 | 5 | 15 |
| MariaDB Database | Tampering | Unauthorized SQL modifies stored product data | 3 | 5 | 15 |
| MariaDB Database | Repudiation | Database activity cannot be attributed to a specific actor | 2 | 4 | 8 |
| MariaDB Database | Information Disclosure | Unauthorized database queries expose stored information | 3 | 5 | 15 |
| MariaDB Database | Denial of Service | Excessive database queries consume database resources | 3 | 5 | 15 |
| MariaDB Database | Elevation of Privilege | Database user gains unauthorized administrative privileges | 2 | 5 | 10 |
| External Services | Spoofing | Attacker impersonates an external service | 2 | 5 | 10 |
| External Services | Tampering | Data exchanged with an external service is modified | 3 | 5 | 15 |
| External Services | Repudiation | External transaction or request cannot be reliably traced | 2 | 4 | 8 |
| External Services | Information Disclosure | Sensitive application data is exposed to an external service | 3 | 5 | 15 |
| External Services | Denial of Service | External service becomes unavailable | 3 | 4 | 12 |
| External Services | Elevation of Privilege | Compromised integration credentials provide unauthorized access | 2 | 5 | 10 |

---

## 3. Observed Log Findings

The Task 2 log analysis identified the following suspicious behaviours:

### SQL Injection-like Request

Timestamp:

`23/Sep/2026 10:10:07 -0400`

Evidence:

```text
127.0.0.1 - - [23/Sep/2026:10:10:07 -0400] "GET /?id=%27%20OR%20%271%27%3D%271 HTTP/1.1" 200 1614 "-" "curl/8.21.0"




## Mitigation and Recommended Controls

### Client
- Use strong authentication and session management.
- Validate user input before sending requests to the application.
- Restrict access to administrative functionality.
- Protect sensitive information from being displayed to unauthorized users.

### NGINX Web Server
- Apply secure NGINX configuration and restrict unnecessary paths.
- Use request filtering and rate limiting to reduce malicious or excessive requests.
- Restrict access to administrative endpoints.
- Maintain sufficient access and error logging for investigation.

### PHP Application
- Use parameterized queries or prepared statements to prevent SQL injection.
- Validate and sanitize application input.
- Enforce authorization checks for administrative functions.
- Avoid exposing sensitive application or system information in responses.
- Apply secure session and authentication controls.

### MariaDB Database
- Apply least-privilege permissions to database accounts.
- Restrict database access to the application and trusted administrative sources.
- Use strong database authentication credentials.
- Monitor database activity and maintain appropriate audit logs.
- Protect sensitive stored information from unauthorized disclosure.

### External Services
- Use authenticated and encrypted connections for external integrations.
- Validate data received from external services before processing it.
- Store integration credentials securely.
- Apply least privilege to service accounts and API credentials.
- Monitor failed or unexpected external requests.
