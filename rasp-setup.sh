#!/bin/sh

# User setup 
sudo apt install vim
sudo apt install tree
echo "alias py='python'" >> ~/.bash_aliases
echo "alias ls='ls --color=always -hp" >> ~/.bash_aliases
echo "set rnu" > ~/.vimrc

# Git config
git config --global user.email "robotronsc@gmail.com"
git config --global user.name "robotron-sc"

# Updgrades
sudo apt update
sudo apt upgrade -y
# sudo apt install python3-distutils -y

# CMake dev tools
sudo apt install build-essential cmake pkg-config -y

# OpenCV dependencies
sudo apt install libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran -y

# Python3 header files
sudo apt install python3-dev -y

# Pip
sudo apt install python3-pip -y

# Python virtual enviornment
sudo pip3 install virtualenv virtualenvwrapper
[ ! -f ~/.bashrc ] && touch ~/.bashrc
echo "\
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

# Python packages
pip3 install "picamera[array]"
pip3 install opencv-python
pip3 install flask