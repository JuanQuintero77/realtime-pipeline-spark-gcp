variable "project_id" {
  type = string
}

variable "location" {
  type = string
}

variable "job_name" {
  type    = string
  default = "event-generator"
}

variable "container_image" {
  type        = string
  description = "Full image URI from Artifact Registry, e.g. us-central1-docker.pkg.dev/PROJECT/REPO/event-generator:latest"
}

variable "service_account_email" {
  type = string
}

variable "topic_name" {
  type    = string
  default = "events"
}

variable "batch_size" {
  type    = number
  default = 50
}

variable "sleep_time" {
  type    = number
  default = 10
}

variable "max_runtime_seconds" {
  type    = number
  default = 300
}
