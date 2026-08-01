resource "google_container_cluster" "demo_cluster" {
    name = var.cluster_name
    location = var.cluster_location

    remove_default_node_pool = true
    initial_node_count = 1

    private_cluster_config {
        enable_private_endpoint = var.private_cluster_config["enable_private_endpoint"]
        enable_private_nodes = var.private_cluster_config["enable_private_nodes"]
        master_global_access_config {
            enabled = var.private_cluster_config["master_global_access_config"]
        }
    }
    maintenance_policy {
        recurring_window {
            recurrence = "FREQ=DAILY"
            start_time = "2024-08-25T02:00:00Z"
            end_time = "2024-08-25T06:00:00Z"
        }
    }
}

resource "google_container_node_pool" "node_pool" {
    name = var.node_pool_name
    cluster = google_container_cluster.demo_cluster.name
    location = var.cluster_location
    initial_node_count = 1
    autoscaling {
        max_node_count = var.node_autoscaler["enabled"] == true ? var.node_autoscaler["max_node_count"] : null
        min_node_count = var.node_autoscaler["enabled"] == true ? var.node_autoscaler["min_node_count"] : null
    }

    management {
        auto_repair = true
        auto_upgrade = true
    }
    
    node_config {
        machine_type = var.node_config["machine_type"]
        image_type = var.node_config["image_type"]
        disk_size_gb = var.node_config["disk_size_gb"]
        disk_type = var.node_config["disk_type"]
    }

    upgrade_settings {
        max_surge = 1
        max_unavailable = 1
    }
}   

resource "google_compute_address" "static_ip" {
  name = var.static_ip_name
  address_type = var.address_type
  region = "us-central1"
}

resource "google_dns_managed_zone" "zone" {
  name = var.domain_name
  description = "Flight App DNS Zone"
  dns_name = var.domain_host
}

resource "google_dns_record_set" "a_record" {
  name = var.subdomain_host
  type = "A"
  ttl = 15
  managed_zone = google_dns_managed_zone.zone.name

  rrdatas = [ google_compute_address.static_ip.address ]
}