terraform {
  backend "gcs" {
    bucket  = "realtimepipeline-tfstate"
    prefix  = "terraform/state"
  }
}

module "storage" {
  source = "./modules/datalake"

  project_id               = var.project_id
  location                 = var.location
  lifecycle_days_raw       = var.lifecycle_days_raw
  lifecycle_days_processed = var.lifecycle_days_processed
  service_account_email    = var.service_account_email
}

module "data_warehouse" {
  source = "./modules/bigquery"

  project_id               = var.project_id
  location                 = var.location
}

module "pubsub" {
  source = "./modules/pubsub"

  project_id        = var.project_id
  topic_name        = "events"
  subscription_name = "events-sub"
}

module "artifact_registry" {
  source = "./modules/artifact_registry"

  project_id            = var.project_id
  location              = var.region
  service_account_email = var.service_account_email
}

locals {
  # Placeholder used on first apply (image doesn't exist yet).
  # After docker push, update this to the real image and run terraform apply again,
  # or let CI/CD update the job via: gcloud run jobs update event-generator --image=...
  generator_image = "us-docker.pkg.dev/cloudrun/container/hello:latest"
  real_image      = "${module.artifact_registry.repository_url}/event-generator:latest"
}

module "event_generator" {
  source = "./modules/cloud_run_job"

  project_id            = var.project_id
  location              = var.region
  container_image       = local.generator_image
  service_account_email = var.service_account_email
  topic_name            = "events"
  max_runtime_seconds   = 300
}