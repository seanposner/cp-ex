provider "aws" {
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    ecs                = "http://localhost:4566"
    ec2                = "http://localhost:4566"
    iam                = "http://localhost:4566"
    ecr                = "http://localhost:4566"
    logs               = "http://localhost:4566"
  }
}

resource "aws_ecs_cluster" "cluster" {
  name = "cluster"
}

resource "aws_ecr_repository" "elb" {
  name                 = "elb"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository" "sqs" {
  name                 = "sqs"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecs_task_definition" "elb_task" {
  family                   = "elb-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "elb"
      image     = "${aws_ecr_repository.elb.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 5000
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "sqs_task" {
  family                   = "sqs-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "sqs"
      image     = "${aws_ecr_repository.sqs.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 5001
        }
      ]
    }
  ])
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Effect = "Allow"
        Sid    = ""
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_service" "elb_service" {
  name            = "elb-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.elb_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
}

resource "aws_ecs_service" "sqs_service" {
  name            = "sqs-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.sqs_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
}
