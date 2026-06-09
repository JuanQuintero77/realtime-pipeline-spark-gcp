variable "project_id" {
  type = string
}

variable "location" {
  type = string
}

variable "repository_id" {
  type    = string
  default = "ecommerce"
}

variable "service_account_email" {
  type        = string
  description = "Service account that will push images (CI/CD) and pull images (Cloud Run)"
}
