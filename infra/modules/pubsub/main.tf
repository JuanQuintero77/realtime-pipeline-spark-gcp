resource "google_pubsub_topic" "main" {
  name    = var.topic_name
  project = var.project_id
}

resource "google_pubsub_topic" "dlq" {
  name    = "${var.topic_name}-dlq"
  project = var.project_id
}

resource "google_pubsub_subscription" "main" {
  name  = var.subscription_name
  topic = google_pubsub_topic.main.id

  ack_deadline_seconds = var.ack_deadline_seconds

  message_retention_duration = var.message_retention_duration

  retain_acked_messages = false

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dlq.id
    max_delivery_attempts = var.dead_letter_max_delivery_attempts
  }

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }
}

resource "google_pubsub_subscription" "dlq_sub" {
  name  = "${var.subscription_name}-dlq"
  topic = google_pubsub_topic.dlq.id

  message_retention_duration = var.message_retention_duration
}