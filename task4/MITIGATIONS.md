# Riverbend Boutique — Task 4 Mitigation Plan

## Purpose

This document provides concrete mitigations for the five highest-scoring risks identified in the Riverbend Boutique STRIDE threat model.

Risk Score = Likelihood × Impact

The top five risks are taken directly from task3/risk-ranking.csv.

All implementation work was performed inside the isolated Riverbend Boutique lab VM. No external systems were targeted.

## Top 5 Risks

| Rank | Risk | Likelihood | Impact | Score |
|---|---|---:|---:|---:|
| 1 | SQL injection-like input modifies application behaviour | 4 | 5 | 20 |
| 2 | Malicious HTTP parameters or paths are submitted | 4 | 4 | 16 |
| 3 | Excessive HTTP requests exhaust web-server resources | 4 | 4 | 16 |
| 4 | Client attempts to access administrative functionality | 3 | 5 | 15 |
| 5 | Attacker attempts to reach restricted administrative paths | 3 | 5 | 15 |

---

# 1. SQL Injection-Like Input Modifies Application Behaviour

**Risk score:** 20
**Likelihood:** 4
**Impact:** 5
**STRIDE category:** Tampering

## Risk

If future application functionality accepts user-controlled values and directly concatenates those values into SQL queries, an attacker could manipulate the query and modify application behaviour or access unauthorised database information.

## Current Lab State

The current `app/index.php` uses a fixed SQL query:

    SELECT name, description, price, stock FROM products ORDER BY id

There is currently no user-controlled SQL parameter in this query. Therefore, this lab does not claim to have demonstrated a live SQL injection attack.

## Mitigation

Use parameterized queries / prepared statements for all future SQL queries that contain user-controlled input.

Additional controls:

- Validate and constrain input according to the expected data type and format.
- Avoid constructing SQL statements through string concatenation.
- Use a dedicated database account with only the permissions required by the application.
- Do not grant administrative database privileges to the web application account.

## Implemented Control

The database account `shopuser` was changed from full database privileges to SELECT-only access on the Riverbend database.

This applies the principle of least privilege to the current read-only product display application.

## Required Code Change for Future Dynamic Queries

Use prepared statements, for example:

    $stmt = $conn->prepare("SELECT name, description, price, stock FROM products WHERE id = ?");
    $stmt->bind_param("i", $productId);
    $stmt->execute();

The exact query should be adapted to future application functionality.

## Expected Impact

Prepared statements prevent SQL syntax supplied through input from being interpreted as part of the SQL command.

The least-privilege database account also limits the potential impact if the application layer is compromised.

## Verification

Database privileges were checked after the change using SHOW GRANTS. The resulting application grant is SELECT only.

The storefront was then tested and continued displaying all five products successfully.

## Limitation

Prepared statements are a code-level control for SQL injection. They are not a replacement for authentication, authorisation, logging, or database access controls.

---

# 2. Malicious HTTP Parameters or Paths Are Submitted

**Risk score:** 16
**Likelihood:** 4
**Impact:** 4
**STRIDE category:** Tampering

## Risk

Attackers may submit unexpected URL paths, parameters, or requests in an attempt to access files, application functionality, or resources that should not be publicly available.

## Mitigation

NGINX uses controlled request routing:

    location / {
        try_files $uri $uri/ =404;
    }

This causes unknown resources to return HTTP 404 rather than being passed to arbitrary application functionality.

The lab also contains an explicit restriction for the administrative path:

    location ^~ /admin {
        return 403;
    }

## Required Configuration Changes

Keep the controlled routing configuration and explicitly restrict sensitive paths.

Future deployments should also review source-control directories, backup files, configuration files, and other sensitive resources under the web root.

## Expected Impact

Unexpected paths are rejected instead of being served by the application, reducing unnecessary exposure of files and endpoints.

## Verification

The active NGINX configuration was inspected and the expected routing and administrative restrictions were confirmed.

The application continued to load normally after the controls were applied.

---

# 3. Excessive HTTP Requests Exhaust Web-Server Resources

**Risk score:** 16
**Likelihood:** 4
**Impact:** 4
**STRIDE category:** Denial of Service

## Risk

A client sending a large number of requests in a short period can consume web-server and application resources.

## Mitigation

NGINX request-rate limiting was implemented.

Inside the NGINX `http` context:

    limit_req_zone $binary_remote_addr zone=riverbend_limit:10m rate=5r/s;

The web-server location uses:

    limit_req zone=riverbend_limit burst=10 nodelay;

## Configuration Explanation

- `5r/s` establishes a sustained request rate of five requests per second per client IP.
- `burst=10` allows a limited temporary burst.
- `nodelay` prevents accepted burst requests from being artificially delayed.
- Requests exceeding the configured limit are rejected by NGINX.

## Expected Impact

The control reduces the ability of a single client to generate sustained high request volume against the application and reduces unnecessary load reaching PHP-FPM and the database.

## Verification

A 30-request rapid test was performed in the lab.

Observed result:

    12 requests returned HTTP 200
    18 requests returned HTTP 503

NGINX error logs also recorded rate-limit events containing `limiting requests`.

Evidence:

- `task4/evidence/riverbend-rate-limit-test.txt`
- `task4/evidence/riverbend-rate-limit-nginx-log.txt`

## Limitation

This is an application/web-server rate-limiting control, not complete DDoS protection.

The `5r/s` threshold with a burst of `10` is a lab configuration and should be tuned using legitimate traffic requirements in a production environment.

---

# 4. Client Attempts to Access Administrative Functionality

**Risk score:** 15
**Likelihood:** 3
**Impact:** 5
**STRIDE category:** Elevation of Privilege

## Risk

A client may attempt to access administrative functionality without appropriate authorisation.

## Current Lab State

The current Riverbend application does not contain a functional administrative interface.

Therefore, the mitigation in this lab is a defensive restriction of the expected `/admin` path rather than a claim that a complete admin authentication system has been implemented.

## Mitigation

Future administrative functionality should use:

- Authentication
- Role-based authorisation
- Server-side access-control checks
- Least privilege
- Session protection
- Audit logging for privileged actions

As defence in depth, the current lab explicitly blocks `/admin` at NGINX.

## Implemented Configuration

    location ^~ /admin {
        return 403;
    }

## Expected Impact

Unauthorised clients cannot reach the expected administrative path through the web server.

In a future production implementation, authenticated users should additionally be checked for an appropriate administrator role at the application layer.

## Verification

The `/admin` request was verified to return HTTP 403 Forbidden.

The normal storefront continued to return the expected page and products.

Evidence:

- `task4/evidence/riverbend-admin-mitigation.txt`

## Limitation

Blocking `/admin` at NGINX is not equivalent to implementing application-level authentication and authorisation.

---

# 5. Attacker Attempts to Reach Restricted Administrative Paths

**Risk score:** 15
**Likelihood:** 3
**Impact:** 5
**STRIDE category:** Elevation of Privilege

## Risk

An attacker may directly request known or guessed administrative URLs.

Relying only on the absence of a visible link is insufficient because an attacker can request a path directly.

## Mitigation

The NGINX configuration explicitly denies access to the administrative path:

    location ^~ /admin {
        return 403;
    }

## Expected Impact

Direct requests to `/admin` are rejected by NGINX before reaching the PHP application.

This provides an additional server-layer access-control boundary.

## Verification

The mitigation was verified with:

    curl -i -s http://127.0.0.1/admin

The response was HTTP 403 Forbidden.

The normal application continued to respond successfully.

Evidence:

- `task4/evidence/riverbend-admin-mitigation.txt`

## Limitation

This control only protects the configured administrative path.

Any future administrative endpoints must be reviewed individually and protected with application-level authentication and authorisation.

---

# Additional Security Controls

## Security Headers

The NGINX server was configured with additional HTTP security headers:

    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

### Expected Impact

- `X-Content-Type-Options` reduces MIME-type sniffing.
- `X-Frame-Options` restricts framing of the application to the same origin.
- `Referrer-Policy` limits unnecessary referrer information.
- `Permissions-Policy` disables unused browser capabilities in this lab.

### Verification

The response headers were checked using:

    curl -I http://127.0.0.1/

The configured security headers were present in the HTTP response.

## Configuration Validation

NGINX configuration changes were validated with:

    sudo nginx -t

The active configuration passed the NGINX syntax test before reload.

A negative control was also performed using an intentionally invalid NGINX directive. The configuration test correctly failed with an `unknown directive` error.

This confirms that configuration validation can detect invalid syntax before deployment.

## Overall Expected Impact

The implemented controls reduce several identified attack opportunities by restricting administrative paths, limiting excessive HTTP requests, reducing unnecessary browser capabilities, and applying database least privilege.

The SQL injection risk is addressed as a secure-development requirement through prepared statements and parameterized queries for any future user-controlled database input. The current Riverbend application uses a fixed SQL query and does not expose a live user-controlled SQL injection parameter.

## Lab Limitations

- The environment is an isolated beginner lab and is not a production deployment.
- Rate-limit values require tuning against legitimate production traffic.
- NGINX path blocking does not replace application-level authentication and authorisation.
- The current application has no functional administrative interface.
- The current application does not contain a live user-controlled SQL injection parameter.
- Rate limiting is not a substitute for dedicated DDoS protection.
- Production deployments would require additional monitoring, centralised logging, secrets management, TLS, patch management, and security testing.
