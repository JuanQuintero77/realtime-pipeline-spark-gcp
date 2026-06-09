output "artifact_registry_url" {
  description = "Base URL for Docker images — use this to build the full image tag"
  value       = module.artifact_registry.repository_url
}

output "event_generator_job_name" {
  value = module.event_generator.job_name
}
