from krecik_iot_controller.krecik_iot_controller import KrecikIOTController

import os

def main():
    bt_token = os.getenv('BT_TOKEN')
    if bt_token is None:
        raise RuntimeError("BT_TOKEN env variable not set")
    bt_token = bytes(bt_token, encoding='utf-8')

    controller = KrecikIOTController(
        bt_token=bt_token,
    )
    controller.run(
        sleep_interval_s=3600,
    )


if __name__ == '__main__':
    main()
