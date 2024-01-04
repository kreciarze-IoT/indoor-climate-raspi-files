# indoor-climate-raspi-files

Bluetooth Low Energy module based on [Douglas6's cputemp](https://github.com/douglas6/cputemp). 
Licensed under the [MIT License](src/bluetooth/cputemp/LICENSE).

[Wprowadzenie do Bluetooth LE](https://devzone.nordicsemi.com/guides/short-range-guides/b/bluetooth-low-energy/posts/ble-services-a-beginners-tutorial)


## Installation

### Changing the bluetooth device name

If you want to change the bluetooth device name permanently,
you have to create a file called /etc/machine-info which should have the following content:
PRETTY_HOSTNAME=device-name

### Enabling bluetooth auto-connect 
One should do it after each reboot, so it's an element of activate.sh script.
Activate.sh should be run after each reboot, e.g. by adding it to /etc/rc.local
```bash
    sudo bluetoothctl <<EOF
    power on
    discoverable on
    pairable on
    agent NoInputNoOutput
    default-agent 
    EOF
    
    sudo service bluetooth restart
```

### Configuring the bluetooth service
edit file: /etc/bluetooth/main.conf
    ControllerMode = le
    TemporaryTimeout = 0
edit file /etc/bluetooth/input.conf 
    IdleTimeout=0
sudo service bluetooth restart
