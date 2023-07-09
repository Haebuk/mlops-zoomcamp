variable "ecr_repo_name" {
  type        = string
  description = "The name of the ECR repository to create"
}

variable "ecr_image_tag" {
  type        = string
  description = "ECR repo name"
  default     = "latest"
}

variable "lambda_function_local_path" {
  type        = string
  description = "The path to the lambda function"
}

variable "docker_image_local_path" {
  type        = string
  description = "The path to the docker image"
}

variable "region" {
  type        = string
  default     = "ap-northeast-2"
  description = "AWS region to create resources"
}

variable "account_id" {
  type        = string
  description = "AWS account id"
}
