resource "google_artifact_registry_repository" "main" {
  project       = var.project_id
  location      = var.location
  repository_id = var.repository_id
  format        = "DOCKER"
}

# Allows the service account to push images (used by CI/CD)
resource "google_artifact_registry_repository_iam_member" "writer" {
  project    = var.project_id
  location   = var.location
  repository = google_artifact_registry_repository.main.name
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${var.service_account_email}"
}

# Allows Cloud Run to pull images at runtime
resource "google_artifact_registry_repository_iam_member" "reader" {
  project    = var.project_id
  location   = var.location
  repository = google_artifact_registry_repository.main.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${var.service_account_email}"
}
