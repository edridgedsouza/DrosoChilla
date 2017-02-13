#! /usr/bin/env bash
# Setup script. Only run this once to ensure proper setup.
# Run as su

echo "Installing pigpio"
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
rm pigpio.zip
cd PIGPIO
sudo make
sudo make install
cd ..
sudo rm -rf PIGPIO # You don't technically need to remove these, but it prevents clutter
echo "Installed pigpio input/output library"

echo "Installing DHT22 sensor class"
# Download the python class
wget http://abyz.co.uk/rpi/pigpio/code/DHT22_py.zip
unzip DHT22_py.zip
rm DHT22_old.py
rm DHT22_py.zip
echo "Installed DHT22 sensor class for python"

echo "Installing Flask web framework"
sudo apt-get install python3-flask
echo "Installed Flask web framework"

echo "Installing Twitter python library"
sudo pip3 install tweepy
echo "Installed Twitter python library"


# Change local date/time
echo "Adjusting date and time"
sudo dpkg-reconfigure tzdata
sudo /etc/init.d/ntp stop
sudo ntpd -q -g
sudo /etc/init.d/ntp start
echo "Local data and time is changed. Current date and time is:

$(date)"