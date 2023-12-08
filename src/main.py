from bluetooth.krecik_ble_server import krecik_ble_server

from time import sleep


def main():

    # Docelowo ten serwis (jako cały) wywoływać tylko na samym początku,
    # dla nieskonfigurowanego urządzenia (lub po factor-resecie ???)

    ble = krecik_ble_server()
    ble.run()

    try:
        i = 0
        while True:
            sleep(1)
            print(f"Krecik BLE server is running... {i}")
            i+=1
    except KeyboardInterrupt:
        ble.quit()


if __name__=='__main__':
    main()
