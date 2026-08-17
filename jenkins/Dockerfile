FROM jenkins/jenkins:lts
USER root

# 1. Install prerequisites (no software-properties-common needed)
RUN apt-get update && \
    apt-get -y install ca-certificates curl gnupg

# 2. Add Docker's official GPG key the modern way
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg

# 3. Add the Docker repository (Hardcoded to 'bookworm' for compatibility)
RUN echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list

# 4. Install the Docker CLI
RUN apt-get update && \
    apt-get -y install docker-ce-cli

# 5. Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

USER jenkins
