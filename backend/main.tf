# Terraform configuration
terraform {
  required_providers {
    k3d = {
      source = "pvotal-tech/k3d"
      version = "0.0.6"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.11.0"
    }
    helm = {
      source = "hashicorp/helm"
      version = "2.5.1"
    }
  }
}

# Configuration providers 

provider "k3d" {
  # Configuration options
}

# Configure the k3d cluster
resource "k3d_cluster" "mycluster" {
  name  = "test_cluster_2" 
  servers = 1
  agents  = 3 

  kube_api {
    host      = "localhost"
    host_ip   = "127.0.0.1"
    host_port = 6445
  }

  port {
    host_port      = 8080
    container_port = 8080
    node_filters = [
      "loadbalancer",
    ]
  }

  k3d {
    disable_load_balancer     = false
    disable_image_volume      = false
  }

   kubeconfig {
    update_default_kubeconfig = true
    switch_current_context    = true
  }

  runtime {
    agents_memory= "5000M" 
  }
}