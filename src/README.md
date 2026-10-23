# Source code

| Folder | Diagram steps | What it does | Talks to |
|---|---|---|---|
| `catalog-service/` | 7-9 | Container behind the ALB. `GET /events`, `GET /events/{id}/seats`, `GET /health` | DynamoDB (read) |
| `lambdas/booking-api/` | 10-12 | Holds the seat (a condition blocks double booking), then queues the booking | DynamoDB, SQS |
| `lambdas/start-workflow/` | 13-14 | Reads the queue and starts the state machine | Step Functions |
| `lambdas/charge-payment/` | 15 | State 2: stores the task token and asks the provider to charge (logged only) | DynamoDB |
| `lambdas/payment-webhook/` | 16-17 | Marks the seat BOOKED or fails the task, then resumes the workflow | DynamoDB, Step Functions |
| `lambdas/cleanup/` | timer | Frees seats held longer than the hold time | DynamoDB |
| `lambdas/send-email/` | 20-21 | Sends the e-ticket email | SES |
| `seed/seed_events.py` | - | Loads sample events and seats | DynamoDB |

## Data model

One DynamoDB table. `pk` is the event ID. `sk` is `META` for the event details, or the seat ID (for example `A1`) for a seat.
A seat has a `status` of `FREE`, `HELD` or `BOOKED`.
