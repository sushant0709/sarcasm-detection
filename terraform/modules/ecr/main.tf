data "aws_ecr_authorization_token" "token" {}

resource "aws_ecr_repository" "ecr_repo" {
  name                 = var.ecr_repo_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  force_delete = true
}

resource "null_resource" "docker_ops" {
  triggers = {
    ecr_repository_url = aws_ecr_repository.ecr_repo.repository_url
  }

  provisioner "local-exec" {
    command = <<-EOT
        docker login ${data.aws_ecr_authorization_token.token.proxy_endpoint} -u AWS -p ${data.aws_ecr_authorization_token.token.password}
        docker pull alpine
        docker tag alpine ${aws_ecr_repository.ecr_repo.repository_url}:latest
        docker push ${aws_ecr_repository.ecr_repo.repository_url}:latest
    EOT
  }

  depends_on = [aws_ecr_repository.ecr_repo]
}