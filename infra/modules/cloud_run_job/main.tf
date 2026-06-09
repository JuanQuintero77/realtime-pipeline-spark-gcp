resource "google_cloud_run_v2_job" "event_generator" {
  name                = var.job_name
  location            = var.location
  project             = var.project_id
  deletion_protection = false

  template {
    template {
      service_account = var.service_account_email

      # 6 minutes: 5 min runtime + 1 min buffer for startup/shutdown
      timeout = "360s"

      containers {
        # Placeholder on first apply — replaced by CI/CD after docker push
        image = var.container_image

        env {
          name  = "GCP_PROJECT_ID"
          value = var.project_id
        }

        env {
          name  = "PUBSUB_TOPIC"
          value = var.topic_name
        }

        env {
          name  = "BATCH_SIZE"
          value = tostring(var.batch_size)
        }

        env {
          name  = "SLEEP_TIME"
          value = tostring(var.sleep_time)
        }

        env {
          name  = "MAX_RUNTIME_SECONDS"
          value = tostring(var.max_runtime_seconds)
        }

        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
        }
      }
    }
  }

  lifecycle {
    # Image updates are managed by CI/CD (docker push + gcloud run jobs update)
    ignore_changes = [template]
  }
}

resource "google_pubsub_topic_iam_member" "generator_publisher" {
  project = var.project_id
  topic   = var.topic_name
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${var.service_account_email}"
}
