# MLFlow

MLFlow provides experiment tracking process by logging metrics, metadata and models for each training. It logs model checkpoints, artifacts and models from MLFlow Model Registry to an S3 bucket, while metrics, training parameters and other metadata are being logged to a PostgreSQL database.

It should be deployed on ECS + EC2 with corresponding IAM roles and access to RDS (PostgreSQL) and S3. 

Environment variables:
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- MLFLOW_BACKEND_STORE_URI (PostgreSQL URI)
- MLFLOW_DEFAULT_ARTIFACT_ROOT (S3 bucket URI)