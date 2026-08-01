gcp_project = "devops-project-503800"
key_path = "C:\\Users\\hansj\\Downloads\\devops-project-503800-141ec14e66f1.json"
project_zone = "us-central1-a"

//GKE

cluster_name = "demo-cluster"
cluster_location = "us-central1-a"

private_cluster_config = {
    enable_private_endpoint = false
    enable_private_nodes = false
    master_global_access_config = true
}

node_pool_name = "demo-node-pool"
node_autoscaler = {
    enabled = true,
    min_node_count = 0,
    max_node_count = 6
}
node_config = {
    machine_type = "e2-medium"
    image_type = "cos_containerd"
    disk_size_gb = 100
    disk_type = "pd-standard"
}

// IP ADDRESS
static_ip_name = "flight-app-static-ip"
address_type = "EXTERNAL"

// CLOUD DNS
domain_name = "flight-app-zone"
domain_host = "flightsnotfeelings.shop."
subdomain_host = "flight-app.flightsnotfeelings.shop."