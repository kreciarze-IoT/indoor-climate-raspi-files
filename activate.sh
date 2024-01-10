#!/bin/bash

sudo bluetoothctl power on
sudo bluetoothctl discoverable on
sudo bluetoothctl pairable on
sudo bluetoothctl agent NoInputNoOutput
sudo bluetoothctl default-agent

sudo service bluetooth restart

export BT_TOKEN="super_secret_token"
export BT_IV="super_secret_iv"

/home/krecik/indoor-climate-raspi-files/venv/bin/python /home/krecik/indoor-climate-raspi-files/src/main.py
