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
  name         = "localstack/localstack"
}

resource "docker_container" "localstack_container" {
  image = docker_image.localstack.latest
  name  = "localstack_container"
  ports {
    internal = 4566
    external = 4566
  }
  env = [
    "SERVICES=s3,sqs,ecs",
    "DEBUG=1",
    "DATA_DIR=/tmp/localstack/data"
  ]
}
