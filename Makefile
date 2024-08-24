setup-infrastructure:
	sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
	wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
	gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
	echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com focal main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
	sudo apt update
	sudo apt-get install terraform

install-aws-cli:
	mkdir -p downloads
	sudo apt install unzip
	cd downloads && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install

download-nltk-data:
	pipenv run python -m nltk.downloader punkt stopwords averaged_perceptron_tagger wordnet omw-1.4

test: download-nltk-data
	pytest tests/unit_tests

# integration_test:
# 	pytest tests/integration_tests

quality_checks:
	isort .
	black .
	pylint --recursive=y .

# build: quality_checks test
# 	docker build -t ${LOCAL_IMAGE_NAME} .

# integration_test: build
# 	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash integraton-test/run.sh

# publish: build integration_test
# 	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash scripts/publish.sh

setup: download-nltk-data
	# Install pipenv
	pip install --upgrade pip
	pip install pipenv
	pipenv install --dev

	# Pre-commit hooks
	pre-commit install

install-software:
	sudo yum update -y
	mkdir -p ../downloads

	# Install Python
	cd ../downloads && wget https://repo.anaconda.com/archive/Anaconda3-2023.07-1-Linux-x86_64.sh && \
	bash Anaconda3-2023.07-1-Linux-x86_64.sh
	echo "export PATH=$HOME/anaconda3/bin:$PATH" >> ~/.bashrc

	# Run bash file
	source ~/.bashrc

	# Install PostgreSQL
	sudo dnf update -y
	sudo dnf install postgresql15.x86_64 postgresql15-server -y
	sudo postgresql-setup --initdb
	sudo systemctl start postgresql
	sudo systemctl enable postgresql
	sudo systemctl status postgresql

	# Install docker-compose
	cd ../downloads && wget https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-linux-x86_64 -O docker-compose && \
	sudo chmod +x docker-compose
	echo "export PATH=$HOME/downloads:$PATH" >> ~/.bashrc

	# Run bash file
	source ~/.bashrc

	# Install Docker
	sudo yum install docker -y
	sudo usermod -a -G docker ec2-user
	newgrp docker
	sudo systemctl enable docker.service

	# Install act
	curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
