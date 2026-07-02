# IAM Roles & Users — Reference

This project uses least-privilege-oriented IAM roles/users, one per service, rather than a single broad-permission identity.

| Identity | Type | Attached Policies | Used By |
|---|---|---|---|
| `gridpulse-lambda-role` | Role | `AWSLambdaBasicExecutionRole`, `AmazonS3FullAccess` | Lambda extraction function |
| `gridpulse-glue-role` | Role | `AWSGlueServiceRole`, `AmazonS3FullAccess` | Glue crawlers + Spark ETL job |
| `tableau-connector` | User (programmatic access only) | `AmazonAthenaFullAccess`, `AmazonS3FullAccess` | Tableau Desktop → Athena connection |

**Note on scope:** `AmazonS3FullAccess` is used here for build simplicity. In a production environment, this would be tightened to a bucket-scoped policy (`s3:GetObject`, `s3:PutObject`, `s3:ListBucket` restricted to `arn:aws:s3:::gridpulse-preethi-ds/*`) rather than account-wide S3 access.

**Why Athena needs S3 write access:** Athena is serverless — every query result is written to the configured S3 staging directory (`s3://gridpulse-preethi-ds/athena-results/`) before being returned to the client (Tableau). Read-only S3 access is not sufficient for the Athena connection to function.
