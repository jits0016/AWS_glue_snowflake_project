provider "aws" {
  region = "ap-south-1" # Change to your desired AWS region
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "tmdb_api_lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}
data "archive_file" "zip_package" {
  type        = "zip"
  source_dir  = "${path.module}/../python/"  # Directory containing hello.py and other code
  output_path = "${path.module}/../f_pak/deployproject2final.zip"     # Output ZIP file path
}

resource "aws_lambda_function" "example_lambda" {
  function_name = "tmdb_lambda_function"
  handler      = "project_2_final.handler" # Replace with your Python file and handler
  runtime      = "python3.9"               # Python runtime version

  role = aws_iam_role.lambda_execution_role.arn

  # Specify the deployment package (ZIP file)
  filename = "${path.module}/../f_pak/deployproject2final.zip"
}

