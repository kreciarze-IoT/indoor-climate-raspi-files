from krecik_iot_controller.krecik_iot_controller import KrecikIOTController


def main():
    controller = KrecikIOTController()
    controller.run(
        sleep_interval_s = 3600
    )

if __name__ == '__main__':
    main()
