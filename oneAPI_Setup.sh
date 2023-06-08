#!/bin/bash

#  Prerequisites for First-Time Users

# Set up the repository. To do this, download the key to the system keyring:
wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \ gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
# Add the signed entry to APT sources and configure the APT client to use the Intel repository:
echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list
# Update the packages list and repository index.
sudo apt update







# APT Package Manager
sudo apt install intel-aikit
# Intel® AI Analytics Toolkit (version 2023.1.1) has been updated to include functional and security updates. Users should update to the latest version as it becomes available.
