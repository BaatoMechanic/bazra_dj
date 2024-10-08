output "kubernetes_cluster_endpoint" {
  value = digitalocean_kubernetes_cluster.bazra_cluster.endpoint
  description = "The endpoint of the Kubernetes cluster."
}

output "container_registry_name" {
  value = digitalocean_container_registry.bazra_registry.name
  description = "The name of the container registry."
}

output "container_registry_credentials" {
  value = digitalocean_container_registry_docker_credentials.bazra_registry_creds.docker_credentials
  description = "Docker credentials for the container registry."
  sensitive = true
}
