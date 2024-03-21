# SetupDocker provider
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.13"
    }
  }
}

provider "docker" {}

# Initiate LocalStack container
resource "docker_image" "localstack" {
  name         = "localstack/localstack-pro"
}

resource "docker_container" "localstack_container" {
  image = docker_image.localstack.latest
  name  = "localstack_container"
  ports {
    internal = 4566
    external = 4566
  }
  env = [
    "SERVICES=s3,sqs,ecs,ecr,iam,ec2",
    "DEBUG=1",
    "DATA_DIR=/tmp/localstack/data",
    "ACTIVATE_PRO=1",
    "LOCALSTACK_AUTH_TOKEN='ls-POteMEvE-qIQI-bimO-9332-5110wUkA2dc4'"
  ]
}
