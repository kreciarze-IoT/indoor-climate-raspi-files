#!/bin/bash

sudo bluetoothctl power on
sudo bluetoothctl discoverable on
sudo bluetoothctl pairable on
sudo bluetoothctl agent NoInputNoOutput
sudo bluetoothctl default-agent

sudo service bluetooth restart

export BT_TOKEN="super_secret_token"

python /home/krecik/indoor-climate-raspi-files/src/main.py
