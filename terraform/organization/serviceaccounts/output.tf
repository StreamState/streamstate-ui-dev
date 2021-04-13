output "docker_write_svc_email" {
  value = google_service_account.docker-write.email
}

output "docker_write_svc_name" {
  value = google_service_account.docker-write.name
}

output "spark_gcs_svc_name" {
  value = google_service_account.spark-gcs.name
}
output "spark_history_svc_email" {
  value = google_service_account.spark-history.email
}
output "spark_history_svc_name" {
  value = google_service_account.spark-history.name
}

output "org_registry" {
  value = google_artifact_registry_repository.orgrepo.name
}
output "spark_history_bucket_url" {
  value = google_storage_bucket.sparkhistory.url
}
