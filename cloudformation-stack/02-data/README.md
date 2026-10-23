# Stack 02: Data and secrets

The storage layer and the encryption key.

## What this stack creates

| Resource | Purpose |
|---|---|
| KMS key | Encrypts the table, the e-ticket bucket and the secret. Key rotation is on. |
| DynamoDB table `ticketing-table` | Stores events, seats and bookings. On-demand billing, point-in-time recovery and a TTL attribute for seat holds. |
| S3 bucket for e-tickets | Private, encrypted, versioned. The state machine writes the ticket files here. |
| Secrets Manager secret | A placeholder payment provider key. There is no real value. |
| Systems Manager parameter | Seat hold time in minutes. |

**Diagram steps: 11 (save), 18 (PDF).**

**Depends on:** Stack 01 is not required, but deploy this second.

**Outputs:** Exports the table name and ARN, bucket name and ARN, key ARN and secret ARN.



Template: [`template.yaml`](template.yaml)
