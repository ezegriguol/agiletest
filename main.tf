terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  version = "3.5.0"

  credentials = file("C:\\KEYS\\agileenginetest-dcb1485410ad.json")

  project = "agileenginetest"
  region  = "us-central1"
  zone    = "us-central1-c"
}

#Configure Storage buckets (for images & code)
resource "google_storage_bucket" "photos_cache" {
  name = "photos_cache"
}

resource "google_storage_bucket" "code" {
  name = "code-functions"
}

#Configure Pub/Sub
resource "google_pubsub_topic" "photos" {name = "photos" }

#Cloud Function search
data "archive_file" "search" {
 type        = "zip"
 source_dir = "${path.root}/search"
 output_path = "${path.root}/search.zip"
}

resource "google_storage_bucket_object" "search" {
 name   = "search.zip"
 bucket = "code-functions"
 source = "${path.root}/search.zip"
}

resource "google_cloudfunctions_function" "search" {
  name        = "search"
  description = ""
  runtime     = "python37"
  entry_point = "search"
  project = "agileenginetest"
  region = "us-central1"
  available_memory_mb   = 256
  timeout = 60
  service_account_email = "agileenginetest@appspot.gserviceaccount.com"
  source_archive_bucket = "google_storage_bucket_object"
  source_archive_object = "search"
  trigger_http          = true
}

#Cloud Function downloadall
data "archive_file" "downloadall" {
 type        = "zip"
 source_dir = "${path.root}/downloadall"
 output_path = "${path.root}/downloadall.zip"
}

resource "google_storage_bucket_object" "downloadall" {
 name   = "downloadall.zip"
 bucket = "code-functions"
 source = "${path.root}/downloadall.zip"
}

resource "google_cloudfunctions_function" "downloadall" {
  name        = "downloadall"
  description = ""
  runtime     = "python37"
  entry_point = "master"
  project = "agileenginetest"
  region = "us-central1"
  available_memory_mb   = 256
  timeout = 60
  service_account_email = "agileenginetest@appspot.gserviceaccount.com"
  source_archive_bucket = "google_storage_bucket_object"
  source_archive_object = "downloadall"
  trigger_http          = true
  environment_variables = {
    CACHE_TIME = "10",
    API_KEY = "23567b218376f79d9415"
  }
}

#Cloud Function download_detail
data "archive_file" "download_detail" {
 type        = "zip"
 source_dir = "${path.root}/download_detail"
 output_path = "${path.root}/download_detail.zip"
}

resource "google_storage_bucket_object" "download_detail" {
 name   = "download_detail.zip"
 bucket = "code-functions"
 source = "${path.root}/download_detail.zip"
}

resource "google_cloudfunctions_function" "download_detail" {
  name        = "download_detail"
  description = ""
  runtime     = "python37"
  entry_point = "master"
  project = "agileenginetest"
  region = "us-central1"
  available_memory_mb   = 256
  timeout = 60
  service_account_email = "agileenginetest@appspot.gserviceaccount.com"
  source_archive_bucket = "google_storage_bucket_object"
  source_archive_object = "download_detail"
  trigger_http          = null
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "projects/agileenginetest/topics/photos"
  }
}