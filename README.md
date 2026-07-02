# GridPulse - Cloud-Native Energy Transition Analytics Pipeline

An end to end cloud data engineering and analytics project tracking global electricity generation, demand, and the renewable energy transition built to mirror the kind of data platform work performed at a regional electric utility.



---

## Why This Project

Electric utilities are in the middle of a major transition: grids are decarbonizing, demand patterns are shifting with electrification, and regulators, investors, and customers all expect clear visibility into where power comes from and how that mix is changing. This project demonstrates the full lifecycle of building a data platform to answer that question from raw ingestion through a modeled data lake to an interactive analytics dashboard using a genuinely production representative AWS architecture.

## Architecture

```
GitHub (OWID energy dataset)
        │
        ▼
  AWS Lambda (extract.py)  ──────────►  S3 raw/ zone
                                              │
                                              ▼
                                    AWS Glue Crawler (schema discovery)
                                              │
                                              ▼
                                AWS Glue Spark ETL job (transform.py)
                                   clean · dedupe · derive YoY metrics
                                              │
                                              ▼
                                      S3 curated/ zone (Parquet, partitioned by year)
                                              │
                                              ▼
                                    AWS Glue Crawler (curated schema)
                                              │
                                              ▼
                                     Amazon Athena (serverless SQL)
                                              │
                                              ▼
                                   Tableau Desktop (dashboard)
```

One AWS service was deliberately chosen per pipeline stage to keep the architecture clean, cost controlled, and easy to explain no overlapping tools doing the same job.

## Tech Stack

| Stage | Tool | Why |
|---|---|---|
| Extraction | AWS Lambda (Python) | Serverless, near zero cost, scheduled/triggered extraction |
| Raw storage | Amazon S3 | Durable landing zone for untouched source data |
| Transformation | AWS Glue (Spark) | Serverless distributed processing, no cluster to manage |
| Cataloging | AWS Glue Data Catalog | Makes curated data queryable without manual schema work |
| Query layer | Amazon Athena | Serverless SQL directly over S3, pay-per-query |
| IAM | AWS IAM | Scoped roles/users per service (see `etl/iam_roles_reference.md`) |
| Visualization | Tableau Desktop | Live connection to Athena via JDBC |

## Data Source

[Our World in Data - Energy Dataset](https://github.com/owid/energy-data) global energy generation, consumption, and renewable share data, 1965 present, sourced from EIA, Ember, and the Energy Institute. Filtered to 2000 present for this analysis.


## What the project answers -

1. How has the electricity generation mix shifted over the past 25 years? - *Generation Mix* stacked area chart
2. Is renewable energy's share of the grid growing, and how fast? - *Renewable Share Trend* line chart
3. How does the U.S. compare globally on renewable adoption? - *Country Comparison* filled map
4. Right now, is the grid mostly fossil, nuclear, or renewable? - *Fuel Category Breakdown* donut chart

## Real World Debugging Encountered

Part of what makes this a representative engineering exercise rather than a scripted tutorial: several genuine AWS account/infrastructure issues were hit and resolved during the build, including `NoSuchBucket`, `SubscriptionRequiredException`, `OptInRequired`, and a missing JDBC driver installation for the Tableau Athena connection.

## Author

Built by Preethi as a self directed portfolio project demonstrating AWS cloud architecture, Python, Apache Spark, SQL, data lake design, and Tableau dashboard development.
