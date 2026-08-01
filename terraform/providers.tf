terraform {
    backend "gcs" {
        bucket = "flight-app-demo"
        prefix = "terraform"
        //credentials = "C:\\Users\\hansj\\Downloads\\devops-project-503800-141ec14e66f1.json"
    }
    required_providers {
        google = {
            source = "hashicorp/google"
            version = "5.42.0"
        }
    }
}

provider "google" {
  project = var.gcp_project
  //credentials = file(var.key_path)
  zone = var.project_zone
}
