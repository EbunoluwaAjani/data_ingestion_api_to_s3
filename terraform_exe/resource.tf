# creating s3 bucket using random provider
resource "random_id" "bucket_suffix" {
  byte_length = 4
}
# weather api s3 bucket
resource "aws_s3_bucket" "weather-api-bucket" {
  bucket = "weather-api-bucket-${random_id.bucket_suffix.hex}"

  tags = merge(local.common_tags, {
    Name = "weather-api"
  })
}
# google sheet s3 bucket
resource "aws_s3_bucket" "google-sheet" {
  bucket = "google-sheet-bucket-${random_id.bucket_suffix.hex}"

  tags = merge(local.common_tags, {
    Name = "google-sheet"
  })
}

# Create IAM users based on a list from a YAML file
resource "aws_iam_user" "users" {
  for_each = toset(local.users_from_yaml[*].username)
  name     = each.value
}

# Generate access keys for each IAM user
resource "aws_iam_access_key" "user_keys" {
  for_each = aws_iam_user.users
  user = each.value.name
}

# Define a custom IAM policy for write access to S3 and SSM
resource "aws_iam_policy" "custom_writeaccess" {
  name        = "AirflowWriteAccess"
  description = "Allows write operations for Airflow"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = ["s3:PutObject", "ssm:GetParameter"],
      Resource = ["arn:aws:s3:::google-sheet-bucket-*/*",
                  "arn:aws:s3:::weather-api-bucket-*/*"
                  ]
    }]
  })
}

# Attach IAM policies to users based on roles defined in YAML
resource "aws_iam_user_policy_attachment" "user_roles" {
  for_each = {
    for user in local.users_from_yaml : user.username => user.roles[0]
  }

  user       = aws_iam_user.users[each.key].name
  policy_arn = lookup(local.role_policy_map, each.value)
}

# Store IAM user access keys securely in AWS SSM Parameter Store
resource "aws_ssm_parameter" "user_keys" {
  for_each = aws_iam_access_key.user_keys

  name = "/airflow/keys/${each.key}"
  type = "SecureString"
  value = jsonencode({
    access_key_id     = each.value.id,
    secret_access_key = each.value.secret
  })
}
