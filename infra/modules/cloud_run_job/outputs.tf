output "job_name" {
  value = google_cloud_run_v2_job.event_generator.name
}

output "job_id" {
  value = google_cloud_run_v2_job.event_generator.id
}
