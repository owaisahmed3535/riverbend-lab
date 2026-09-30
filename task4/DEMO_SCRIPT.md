# Riverbend Boutique — Task 4 Demo Script

## Demo Objective

Demonstrate one implemented mitigation in the isolated Riverbend Boutique lab and verify that the mitigation works without breaking the normal application.

## Recommended Demonstration

The recommended demonstration is the NGINX administrative-path restriction because it provides a clear before/after security result.

## Recording Flow

### 1. Introduce the Lab

Say:

"This is my Riverbend Boutique Task 4 mitigation demonstration. The project is running inside an isolated Kali lab environment. I will demonstrate the NGINX administrative-path restriction and verify that the normal storefront continues to work." 

### 2. Show the Active Configuration

Run:

    sudo nginx -T 2>/dev/null | grep -A3 -B1 "location \\\\^~ /admin"

Say:

"The NGINX configuration contains an explicit rule for the administrative path. Requests matching `/admin` are returned with HTTP 403 Forbidden." 

### 3. Test the Restricted Path

Run:

    curl -i -s http://127.0.0.1/admin

Say:

"The request is rejected by NGINX and returns HTTP 403 Forbidden. This demonstrates that the restricted administrative path cannot be accessed directly through the web server." 

### 4. Verify the Normal Application

Run:

    curl -s http://127.0.0.1/ | grep -E "Riverbend Boutique|Handmade Bracelet|Wool Scarf|Leather Wallet|Silver Earrings|Canvas Tote Bag"

Say:

"The normal storefront still responds successfully and the expected Riverbend Boutique products are displayed. Therefore, the mitigation does not break normal application access." 

### 5. Show the Configuration Test

Run:

    sudo nginx -t

Say:

"Finally, I validate the NGINX configuration syntax. The configuration test reports that the syntax is successful." 

### 6. Close the Demo

Say:

"This completes the mitigation demonstration. The administrative path restriction was applied at the NGINX layer, verified with an HTTP 403 response, and the normal application was regression-tested successfully." 

## Expected Duration

Approximately 2 to 3 minutes.

## Important Note

Do not demonstrate a live SQL injection against the current application. The current PHP application uses a fixed SQL query and does not expose a user-controlled SQL injection parameter. SQL injection prevention is documented as a secure-development requirement for future dynamic queries.
