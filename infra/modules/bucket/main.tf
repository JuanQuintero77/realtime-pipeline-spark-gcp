resource "google_storage_bucket" "tf_state" {
  name     = "${var.project_id}-tfstate"
  location = var.location

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}