# Stack 03: Edge and identity

What the customer reaches first: the website, the CDN, the firewall and sign-in. Deploy in us-east-1, because CloudFront and WAF use that region.

## What this stack creates

| Resource | Purpose |
|---|---|
| S3 website bucket | Private bucket that holds the static site. Only CloudFront can read it (Origin Access Control). |
| CloudFront distribution | Serves the site over HTTPS from edge locations. Cached reads suit the read-heavy workload. |
| WAF web ACL | AWS common rules plus a rate limit of 2,000 requests per IP. |
| Cognito user pool and app client | Sign up and sign in. Issues the JWT that API Gateway checks. |
| Route 53 record and ACM certificate (optional) | Created only if you pass `DomainName` and `HostedZoneId`. |

**Diagram steps: 1 (DNS), 2 (CDN), 3 (site), 4 (sign in).**

**Depends on:** None.

**Outputs:** Exports the user pool ID and client ID. Outputs the website URL.

Parameters: `DomainName`, `HostedZoneId` (both optional).

Template: [`template.yaml`](template.yaml)
