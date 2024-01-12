from krecik_iot_controller.krecik_iot_controller import KrecikIOTController

import os

def main():

    bt_token = os.getenv('BT_TOKEN')

    bt_iv = os.getenv('BT_IV')

    controller = KrecikIOTController(
        bt_token=bt_token,
        bt_iv=bt_iv,
    )
    controller.run(
        sleep_interval_s=20*60, # [min]
    )


if __name__ == '__main__':
    main()
