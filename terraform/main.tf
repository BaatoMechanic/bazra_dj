terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.digitalocean_token
}

# Define a DigitalOcean project
resource "digitalocean_project" "bazra_project" {
  name        = "Bazra Project"
  description = "Project for Bazra application"
  environment = "Development"
  purpose     = "Application"
}

# Create Kubernetes cluster on DigitalOcean
resource "digitalocean_kubernetes_cluster" "bazra_cluster" {
  name    = "bazra-k8s"
  region  = var.region
  version = "1.31.1-do.2"

  node_pool {
    name       = "default"
    size       = "s-2vcpu-4gb"
    node_count = 3
  }
}

output "kubernetes_cluster_id" {
  value = digitalocean_kubernetes_cluster.bazra_cluster.id
}

# Save the kubeconfig file locally after cluster creation
resource "local_file" "kubeconfig" {
  filename = "${path.module}/../.kube/kubeconfig.yaml"
  content  = digitalocean_kubernetes_cluster.bazra_cluster.kube_config.0.raw_config
}

# Configure the Kubernetes provider using the kubeconfig file we just saved
provider "kubernetes" {
  config_path = local_file.kubeconfig.filename
}

# Create a container registry to store Docker images
resource "digitalocean_container_registry" "bazra_registry" {
  name                    = "bazra"
  subscription_tier_slug  = "basic"
  region                  = var.region
}

output "container_registry_id" {
  value = digitalocean_container_registry.bazra_registry.id
}

# Get Docker credentials for the registry
resource "digitalocean_container_registry_docker_credentials" "bazra_registry_creds" {
  registry_name = digitalocean_container_registry.bazra_registry.name
  write         = true
}

# Create Kubernetes secret for DigitalOcean Container Registry authentication
# resource "kubernetes_secret" "bazra_registry_secret" {
#   metadata {
#     name      = "bazra-registry-secret"
#     namespace = "default"
#   }

#   data = {
#     ".dockerconfigjson" = digitalocean_container_registry_docker_credentials.bazra_registry_creds.docker_credentials
#   }

#   type = "kubernetes.io/dockerconfigjson"
# }

# Associate resources with the project
resource "digitalocean_project_resources" "project_resources" {
  project = digitalocean_project.bazra_project.id
  resources = [
    digitalocean_kubernetes_cluster.bazra_cluster.urn
  ]
}
