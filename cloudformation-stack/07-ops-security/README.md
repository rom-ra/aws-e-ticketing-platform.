# Stack 07: Operations, security and cost

Watching, protecting and backing up the system, and keeping the bill under control.

## What this stack creates

| Resource | Purpose |
|---|---|
| CloudTrail with an encrypted S3 bucket | Records every API call. Log file validation is on. |
| GuardDuty | Threat detection. |
| CloudWatch alarm | Fires when anything lands in the dead letter queue and emails you. |
| AWS Backup vault and daily plan | Backs up the DynamoDB table every day and keeps backups for 35 days. |
| Budget | Emails you at 80% of the monthly limit. |
| SNS alert topic | Delivers the alarm email. |

**Diagram: the Security, Monitoring and Reliability boxes, and the "backup" arrow.**

**Depends on:** Stacks 02 and 05.

**Outputs:** None.

Parameters: `AlertEmail`, `MonthlyBudgetUsd` (default 50).

Template: [`template.yaml`](template.yaml)
