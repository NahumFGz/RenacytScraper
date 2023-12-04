#!/bin/bash -x

# 0. Cambiar el modo interactivo de needrestart para que no pregunte
# sudo sed -i 's/#$nrconf{restart} = '"'"'i'"'"';/$nrconf{restart} = '"'"'a'"'"';/g' /etc/needrestart/needrestart.conf
# yes | sudo dpkg --configure -a

# 1. Update and upgrade
yes | sudo apt update

# 2. Instalar java
yes | sudo apt install default-jre

# 3. Install virtualenv
yes | sudo apt install python3.10-venv
which virtualenv

# 4. Install PIP
yes | sudo apt install python3-pip
pip3 --version

# 5. Crear carpeta donde estara guardado todo y dar permisos
cd /home/brew_test_gcp_01/Desktop
mkdir runscrap
cd runscrap
python3 -m venv my_env
source my_env/bin/activate

