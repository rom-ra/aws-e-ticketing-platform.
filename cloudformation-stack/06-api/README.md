# Stack 06: API

The single front door for application calls.

## What this stack creates

| Resource | Purpose |
|---|---|
| API Gateway HTTP API | Public HTTPS endpoint. |
| Cognito JWT authorizer | Rejects calls without a valid sign-in token. |
| `GET /events` | Goes through a VPC link to the ALB and Fargate. |
| `POST /bookings` | Calls the `booking-api` Lambda. |
| `POST /payments/webhook` | Called by the payment provider. It has no JWT, because the provider is not a signed-in user. |

**Diagram steps: 5 (API call), 6 (JWT check), 7 and 10.**

**Depends on:** Stacks 01, 03, 04 and 05.

**Outputs:** Outputs the API URL.

Template: [`template.yaml`](template.yaml)
