from krecik_iot_controller.krecik_iot_controller import KrecikIOTController


def main():
    controller = KrecikIOTController(
        bt_token=b'qVGchwXL8rZoitZ6IBL4UGL-LNlDbMIMykNvuTFbnpY=',
    )
    controller.run(
        sleep_interval_s=3600,
    )


if __name__ == '__main__':
    main()
