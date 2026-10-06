terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

provider "local" {}

resource "local_file" "demo" {
  filename = "${path.module}/demo.txt"
  content = "Terraform AI Review Demo - PR Test"
  
}
