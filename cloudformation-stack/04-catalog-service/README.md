# Stack 04: Catalog service (read path)

The container that answers "list events" requests, running privately inside the VPC.

## What this stack creates

| Resource | Purpose |
|---|---|
| ECR repository | Stores the container image built from `src/catalog-service`. |
| Internal Application Load Balancer | Receives traffic from API Gateway through a VPC link and spreads it across tasks. |
| ECS cluster, task definition and service | Runs 2 Fargate tasks across 2 Availability Zones. No servers to manage. |
| IAM task role | Read-only access to the DynamoDB table. |
| Security groups | The ALB accepts traffic from inside the VPC only. The tasks accept traffic from the ALB only. |
| CloudWatch log group | Container logs, kept for 14 days. |

**Diagram steps: 7 (events), 8 (route), 9 (private, read data).**

**Depends on:** Stacks 01 and 02.

**Outputs:** Exports the listener ARN and the ALB security group ID. Outputs the ECR repository URI.

Push the image to ECR after this stack exists. Parameter: `ImageTag` (default `latest`).

Template: [`template.yaml`](template.yaml)
