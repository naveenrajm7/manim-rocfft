#!/bin/bash

# aws modules
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install linux-modules-extra-aws

# Install docker
sudo apt-get -y update
sudo apt-get -y install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update

# docker
sudo apt-get -y install docker-ce docker-ce-cli containerd.io


# Ubuntu AMDGPU installer installation
wget https://repo.radeon.com/amdgpu-install/6.3.3/ubuntu/noble/amdgpu-install_6.3.60303-1_all.deb
sudo apt -y install ./amdgpu-install_6.3.60303-1_all.deb
sudo apt -y update

# Install AMDGPU driver
sudo usermod -a -G video,render ubuntu
amdgpu-install -y --usecase=dkms
sudo reboot
