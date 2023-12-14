from bluetooth.krecik_ble_server import KrecikBleServer
from services.datasource import Datasource

from time import sleep


def initialize_datasource(ds):
    print("Started initialization process.")

    ble = KrecikBleServer()
    ble.run()
    print("Krecik BLE server running. Waiting for data...")

    try:
        awaiting_data = True
        while awaiting_data:
            try:
                data_from_phone = ble.get_data()
                print("Received data...", end=" ")

                ds.load_data_from_json(
                    data_from_phone,
                    save=True
                )
                ble.set_message("S")
                print("Data saved.")

                awaiting_data = False
            except RuntimeError as e:
                if str(e)[1] == ':':
                    ble.set_message(str(e)[0])
                    print(str(e)[3:])
                sleep(1)
        ble.quit(delay=5)  # time to read accepted state

    except KeyboardInterrupt:
        ble.quit()


def main():
    print("Szczesc Boze!")

    ds = Datasource(
        bt_token="krecik_krol",
        conf_file="src/conf/datasource.json"
    )

    if not ds.is_configured():
        print("Data source not configured.")
        initialize_datasource(ds)

    # Od tego momentu serwis ds jest już skonfigurowany. Zawiera dane
    # niezbędne do nawiązania połączenia z serwerem, oraz do autoryzacji
    # na nim. Przykład:
    print("Data source configured.")
    print("---------------------")
    print(ds)
    print("---------------------")

    response = request.post(
        f"{ds.host}:{ds.port}/dupa",
        data={"dupa": "dupa"},
        headers={"Authorization": ds.auth_token}
    )


if __name__ == '__main__':
    main()
