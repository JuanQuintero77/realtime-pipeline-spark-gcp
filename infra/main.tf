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