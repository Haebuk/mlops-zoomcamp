resource "aws_lambda_function" "kinesis_lambda" {
  function_name = var.lambda_function_name
  image_uri     = var.image_uri
  package_type  = "Image"
  role          = aws_iam_role.iam_lambda.arn
  tracing_config {
    mode = "Active"
  }
  environment {
    variables = {
      PREDICTIONS_STREAM_NAME = var.output_stream_name
      MODEL_BUCKET            = var.model_bucket
    }
  }
  timeout = 180
}


