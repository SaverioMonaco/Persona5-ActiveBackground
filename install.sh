#!/bin/bash

awk 'NR==4 {$0="FPATH='$(pwd)'/"} { print }' ./main.sh > ./temp
mv ./temp ./main.sh

mkdir weather
echo "Enter your location (for the Weather feature):"
read location
echo "Enter your OpenWeatherMap API Key (Get one for free here: https://openweathermap.org/price)"
read token

echo $location > weather/location.info
echo $token > weather/token.info

echo "Weather information set!"
echo "Running the script once..."
chmod +x ./main.sh
bash ./main.sh
echo "Done!"

echo "Setting the systemd service..."
echo "[Unit]
Description=Persona 5 calendar on the Background

[Service]
Type=oneshot
User=$(whoami)
ExecStart=/bin/bash \"$(pwd)/main.sh\"

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
