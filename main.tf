provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment" "my_app" {
  metadata {
    name      = "my-app"
    namespace = "default"
  }

  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "my-app"
      }
    }
    template {
      metadata {
        labels = {
          app = "my-app"
        }
      }
      spec {
        containers {
          name  = "simple-container"
          image = "nginx:latest"
          ports {
            container_port = 80
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "my_app_service" {
  metadata {
    name      = "my-app-service"
    namespace = "default"
  }

  spec {
    selector = {
      app = "my-app"
    }
    ports {
      protocol    = "TCP"
      port        = 80
      target_port = 80
    }
    type = "ClusterIP"
  }
}
