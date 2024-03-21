# cp-ex

## Architecture
 - Two python based services, dockerized
 - Terraform for localstack
 - Terraform for ECR and ECS defintions

## Pipeline
 - Terraform application of localstack
 - Terraform application of ECR/ECS
 - Jenkins pipeline that can be configured with webhook
 - The pipeline is initiated and pushes the intial docker image to the ECR, which the ECS waits for
 - Jenkins needs the docker plugins installed