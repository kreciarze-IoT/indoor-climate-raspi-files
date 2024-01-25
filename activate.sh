#!/bin/bash

sudo bluetoothctl power on
sudo bluetoothctl discoverable on
sudo bluetoothctl pairable on
sudo bluetoothctl agent NoInputNoOutput
sudo bluetoothctl default-agent

# sudo service bluetooth restart
sudo systemctl stop bluetooth

export BT_TOKEN="306f56538ca5ecbc416a58480102f5f0735bf4fe29d409b81a18f621756e126c"
export BT_IV="41d2067961d7438aab6f2ac736b2d136"

export PROD_KEY="01903450c5d4795d2532868b9d89e686ede9951ecc6397c4c1691b4fc85ecad1"
export DEVICE_ID="grzegorz" #SERIAL_ID
export AUTH_KEY="c2540404-87f3-42f2-aa4f-07ecbfb7480b" #DEVICE_ID

$prompt /home/krecik/indoor-climate-raspi-files/venv/bin/python -u /home/krecik/indoor-climate-raspi-files/src/main.py | tee run.log
