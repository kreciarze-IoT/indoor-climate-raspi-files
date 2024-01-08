from krecik_iot_controller.krecik_iot_controller import KrecikIOTController

import os

def main():

    bt_token = os.getenv('BT_TOKEN')
    if bt_token == '':
        bt_token = None
    else:
        bt_token = bytes(bt_token, encoding='utf-8')

    encrypt = os.getenv('ENCRYPT') == 'true'

    controller = KrecikIOTController(
        bt_token=bt_token,
        encrypt=encrypt
    )
    controller.run(
        sleep_interval_s=3600,
    )


if __name__ == '__main__':
    main()
