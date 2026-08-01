variable "gcp_project" {
  type = string
}

variable "key_path" {
  type = string
}

variable "project_zone" {
  type = string
}

// GKE
variable "cluster_name" {
  type = string
}

variable "cluster_location" {
  type = string
}

variable "private_cluster_config" {
  type = object({
    enable_private_endpoint = bool,
    enable_private_nodes = bool,
    master_global_access_config = bool 
  })
}

variable "node_pool_name" {
  type = string
}

variable "node_autoscaler" {
  type = object({
    enabled = bool,
    max_node_count = number,
    min_node_count = number 
  })
}

variable "node_config" {
  type = object({
    disk_type = string,
    machine_type = string,
    disk_size_gb = number,
    image_type = string 
  })
}

// IP ADDRESS
variable "static_ip_name" {
  type = string
}

variable "address_type" {
  type = string
}

// CLOUD DNS
variable "domain_name" {
  type = string
}

variable "domain_host" {
  type = string
}

variable "subdomain_host" {
  type = string
}