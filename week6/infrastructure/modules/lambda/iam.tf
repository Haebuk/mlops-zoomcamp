resource "aws_iam_role" "iam_lambda" {
  name               = "iam_lambda_stg"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": [
            "lambda.amazonaws.com",
            "kinesis.amazonaws.com"
        ]
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "allow_kinesis_processing" {
  name        = "allow_kinesis_processing_${var.lambda_function_name}"
  path        = "/"
  description = "IAM policy for logging from a lambda function"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "kinesis:ListShards",
                "kinesis:ListStreams",
                "kinesis:*"
            ],
            "Resource": "arn:aws:kinesis:*:*:*",
            "Effect": "Allow"
        },
        {
            "Action": [
                "stream:*"
            ],
            "Resource": "arn:aws:streams:*:*:*",
            "Effect": "Allow"
        } 
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "kinesis_processing" {
  role       = aws_iam_role.iam_lambda.name
  policy_arn = aws_iam_policy.allow_kinesis_processing.arn
}

resource "aws_iam_role_policy" "inline_lambda_policy" {
  name       = "LambdaInlinePolicy"
  role       = aws_iam_role.iam_lambda.name
  depends_on = [aws_iam_role.iam_lambda]
  policy     = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kinesis:PutRecords,
                "kinesis:PutRecord"
            ],
            "Resource": "${var.output_stream_arn}"
        }
    ]
}
EOF
}

resource "aws_lambda_permission" "allow_cloudwatch_to_trigger_lambda_function" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.kinesis_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.source_stream_arn
}

resource "aws_iam_policy" "allow_logging" {
  name        = "allow_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda function"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*",
            "Effect": "Allow"
        }
    ]
    }
    EOF
}

resource "aws_iam_role_policy_attachment" "allow_logging" {
  role       = aws_iam_role.iam_lambda.name
  policy_arn = aws_iam_policy.allow_logging.arn
}

resource "aws_iam_policy" "lambda_s3_role_policy" {
  name        = "lambda_s3_policy_${var.lambda_function_name}"
  description = "IAM policy for s3"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::${var.model_bucket}/*",
                "arn:aws:s3:::${var.model_bucket}"
            ]
        },
        {
            "Action": [
                "autoscaling:Describe*",
                "cloudwatch:*",
                "logs:*",
                "sns:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "iam-policy-attach" {
  role       = aws_iam_role.iam_lambda.name
  policy_arn = aws_iam_policy.lambda_s3_role_policy.arn
}
