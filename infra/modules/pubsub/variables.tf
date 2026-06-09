variable "project_id" {
  type = string
}

variable "topic_name" {
  type = string
}

variable "subscription_name" {
  type = string
}

variable "ack_deadline_seconds" {
  type    = number
  default = 20
}

variable "message_retention_duration" {
  type    = string
  default = "604800s" # 7 días
}

variable "dead_letter_max_delivery_attempts" {
  type    = number
  default = 5
}