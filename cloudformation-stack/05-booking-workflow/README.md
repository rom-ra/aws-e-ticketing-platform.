# Stack 05: Booking workflow (write path)

Everything that happens after the customer presses Book: queue, payment, ticket and email. This template uses SAM, so deploy it with `sam deploy`.

## What this stack creates

| Resource | Purpose |
|---|---|
| Lambda `booking-api` | Receives the booking, saves it in DynamoDB and queues it. |
| SQS queue and dead letter queue | Buffers bookings. After 3 failed tries a message moves to the dead letter queue. |
| Lambda `start-workflow` | Reads the queue and starts the state machine. |
| Step Functions state machine | Validate seats, Charge payment, Issue e-ticket, Publish event. On failure it releases the seat. |
| Lambda `charge-payment` and `payment-webhook` | The first asks the payment provider to charge. The second receives the provider's callback and resumes the workflow. |
| Lambda `cleanup` with a 5-minute schedule | Releases seats that were held but never paid. |
| EventBridge rule, SNS topic, Lambda `send-email`, SES identity | Turn the TicketIssued event into an email to the customer. |

**Diagram steps: 10 to 22, plus the state machine panel.**

**Depends on:** Stack 02.

**Outputs:** Exports the booking and webhook Lambda ARNs and the dead letter queue name.

Parameter: `SenderEmail` (must be verified in SES). Run `sam deploy` from the repository root.

Template: [`template.yaml`](template.yaml)
