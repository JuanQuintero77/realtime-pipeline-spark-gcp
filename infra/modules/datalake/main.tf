resource "google_storage_bucket" "datalake" {
  name     = "${var.project_id}-datalake"
  location = var.location

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age            = var.lifecycle_days_raw
      matches_prefix = ["raw/"]
    }
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age            = var.lifecycle_days_processed
      matches_prefix = ["processed/"]
    }
  }
}