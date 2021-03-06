#!/bin/bash

set -e

apt-get update
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88 | grep "9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88"

if [ $? -eq 0 ]
then
  echo "All good"
else
  echo "Wrong fingerprint"
  exit 1
fi

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
 
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
 
usermod -aG docker azureuser
