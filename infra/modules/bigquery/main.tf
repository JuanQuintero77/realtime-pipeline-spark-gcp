resource "google_bigquery_dataset" "bronze" {
  dataset_id = "bronze"
  location   = var.location
}

resource "google_bigquery_dataset" "silver" {
  dataset_id = "silver"
  location   = var.location
}

resource "google_bigquery_dataset" "gold" {
  dataset_id = "gold"
  location   = var.location
}