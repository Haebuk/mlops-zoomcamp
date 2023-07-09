variable "aws_region" {
  default     = "ap-northeast-2"
  description = "AWS region to create resources"
}

variable "project_id" {
  default     = "mlops-zoomcamp-kade"
  description = "project_id"
}

variable "source_stream_name" {
  type        = string
  description = "source_stream_name"
}

variable "output_stream_name" {
  type        = string
  description = "output_stream_name"
}

variable "model_bucket" {
  type        = string
  description = "s3 model_bucket"
}

variable "lambda_function_local_path" {
  type        = string
  description = "The path to the lambda function"
}

variable "docker_image_local_path" {
  type        = string
  description = "The path to the docker image"
}

variable "ecr_repo_name" {
  type        = string
  description = "The name of the ECR repository to create"
}

variable "lambda_function_name" {
  type        = string
  description = "lambda_function_name"
}