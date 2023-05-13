#!/bin/bash

mkdir weather
echo "Enter your location (for the Weather feature):"
read location
echo "Enter your OpenWeatherMap API Key (Get one for free here: https://openweathermap.org/price)"
read token

#echo $location > weather/location.info
#echo $token > weather/token.info

echo "Weather information set!"
echo "Running the script once..."
python ./makebg.py
echo "Setting the background"
gsettings set org.gnome.desktop.background picture-uri-dark 'file://'$(pwd)'/background.jpg'

echo "Setting the systemd service..."
echo "[Unit]
Description=Persona 5 calendar on the Background

[Service]
Type=oneshot
User=$(whoami)
ExecStart=python \"$(pwd)/makebg.py\"

[Install]
WantedBy=multi-user.target" > ./p5_bg.service

# Copy the service file in the right directory:
# Copy the service files
sudo cp ./*.timer /etc/systemd/system/
sudo cp ./*.service /etc/systemd/system/

echo "Enabling the service"
systemctl enable p5_bg.service
systemctl enable p5_bg.timer
systemctl start p5_bg.timer

echo "Done!"
