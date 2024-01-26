from krecik_iot_controller.krecik_iot_controller import KrecikIOTController

import os


def main():

    bt_token = os.getenv('BT_TOKEN')
    bt_iv = os.getenv('BT_IV')
    iv = os.urandom(16)
    iv = iv.hex()
    auth_key = os.getenv("AUTH_KEY")

    controller = KrecikIOTController(
        bt_token=bt_token,
        bt_iv=bt_iv,
        iv=iv,
        auth_key=auth_key
    )
    controller.run(
        sleep_interval_s=20,
    )


if __name__ == '__main__':
    main()
