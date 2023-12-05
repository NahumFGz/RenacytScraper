#!/bin/bash -x

# 0. Cambiar el modo interactivo de needrestart para que no pregunte
lsb_release -a
sudo sed -i 's/#$nrconf{restart} = '"'"'i'"'"';/$nrconf{restart} = '"'"'a'"'"';/g' /etc/needrestart/needrestart.conf

# 1. Update and upgrade
yes | sudo apt update
# yes | sudo apt upgrade

# 2. Instalar escritorio remoto
wget https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb
sudo apt-get install --assume-yes ./chrome-remote-desktop_current_amd64.deb

# 3. instalar ubuntu-desktop
yes | sudo apt install ubuntu-desktop

# 4. reiniciar
sudo reboot


#sudo systemctl status chrome-remote-desktop@$USER
#/opt/google/chrome-remote-desktop/chrome-remote-desktop --stop
#/opt/google/chrome-remote-desktop/chrome-remote-desktop --start

# dpkg -l | grep ubuntu-desktop
# which gnome-session

# sudo passwd ubuntu
# sudo passwd nahumfg
# sudo passwd brew_test_gcp_01

# sudo usermod -aG sudo brew_test_gcp_01
# sudo vim /etc/gdm3/custom.conf

# sudo vim /etc/gdm3/daemon.conf
