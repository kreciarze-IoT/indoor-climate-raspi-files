from cputemp.cputemp import bt_le_server, ThermometerService, ThermometerAdvertisement

def main():

    # @TODO: zaktualizować serwisy i advertisment cputemp
    #
    # Wprowadzenie do Bluetooth LE:
    # https://devzone.nordicsemi.com/guides/short-range-guides/b/bluetooth-low-energy/posts/ble-services-a-beginners-tutorial
    #
    # Docelowo ten serwis (jako cały) wywoływać tylko na samym początku, dla nieskonfigurowanego urządzenia (lub po factor-resecie ???)

    bt_server = bt_le_server()
    bt_server.add_service(ThermometerService(0))
    bt_server.register()

    adv = ThermometerAdvertisement(0)
    adv.register()

    try:
        bt_server.run()
    except KeyboardInterrupt:
        bt_server.quit()

    #################################   


if __name__=='__main__':
    main()
