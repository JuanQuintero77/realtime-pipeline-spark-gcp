output "bucket_name" {
  value       = google_storage_bucket.tf_state.name
  sensitive   = true
  description = "Bucket name for Terraform state storage"
}
