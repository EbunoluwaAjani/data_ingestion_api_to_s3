locals {
  common_tags = {
    ManagedBy = "Terraform"
    Project   = "Mentorship by Mayor"
  }

  users_from_yaml = yamldecode(file("${path.module}/user-roles.yaml")).users

  role_policy_map = {
    "writeaccess" = aws_iam_policy.custom_writeaccess.arn
    "fullaccess"    = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
  }

}

output "common_tags_debug" {
  value = local.common_tags
}

output "users" {
  value = local.users_from_yaml
}