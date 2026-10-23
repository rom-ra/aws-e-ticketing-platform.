# Stack 01: Network

The private network everything else runs in. There is no internet gateway and no NAT, so nothing inside is reachable from the internet.

## What this stack creates

| Resource | Purpose |
|---|---|
| VPC (10.0.0.0/16) | The isolated network. |
| 2 private subnets | One per Availability Zone, for high availability. |
| Gateway endpoints: DynamoDB and S3 | Free private paths. The DynamoDB endpoint is the "9b read data" arrow in the diagram. |
| Interface endpoints: ECR (api, dkr), CloudWatch Logs, Secrets Manager | Let Fargate pull its image, write logs and read secrets without internet access. |
| Security group for the endpoints | Allows HTTPS from inside the VPC only. |

**Diagram steps: 9 (private access).**

**Depends on:** None. Deploy this stack first.

**Outputs:** Exports the VPC ID, CIDR and both subnet IDs.

Template: [`template.yaml`](template.yaml)
