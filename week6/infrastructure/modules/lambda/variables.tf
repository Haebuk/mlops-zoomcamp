variable "output_stream_name" {
  description = "output_stream_name"
}

variable "output_stream_arn" {
  description = "output_stream_arn"
}

variable "source_stream_name" {
  type        = string
  description = "Source Kinesis Data Streams stream name"
}

variable "source_stream_arn" {
  type        = string
  description = "Source Kinesis Data Streams stream name"
}

variable "model_bucket" {
  description = "s3 model_bucket"
}

variable "image_uri" {
  description = "image_uri"
}

variable "lambda_function_name" {
  description = "lambda_function_name"
}

