from krecik_iot_controller.krecik_iot_controller import KrecikIOTController

import os


def main():

    bt_token = os.getenv('BT_TOKEN')
    bt_iv = os.getenv('BT_IV')
    iv = os.urandom(16)
    iv = iv.hex()
    prod_key = os.getenv('PROD_KEY')
    device_id = os.getenv('DEVICE_ID')

    controller = KrecikIOTController(
        bt_token=bt_token,
        bt_iv=bt_iv,
        prod_key=prod_key,
        device_id=device_id,
        iv=iv
    )
    controller.run(
        sleep_interval_s=20*60,
    )


if __name__ == '__main__':
    main()
