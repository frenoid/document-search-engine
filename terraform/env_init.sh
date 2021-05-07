#!/bin/bash
sudo amazon-linux-extras enable python3.8
sudo yum update
sudo yum -y install python3.8 git python3-pip
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 2
