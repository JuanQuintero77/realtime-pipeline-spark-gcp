output "repository_url" {
  description = "Base URL for pushing/pulling images, e.g. LOCATION-docker.pkg.dev/PROJECT/REPO"
  value       = "${var.location}-docker.pkg.dev/${var.project_id}/${var.repository_id}"
}
