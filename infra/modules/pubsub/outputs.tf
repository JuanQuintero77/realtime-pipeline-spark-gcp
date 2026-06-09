output "topic_name" {
  value = google_pubsub_topic.main.name
}

output "subscription_name" {
  value = google_pubsub_subscription.main.name
}