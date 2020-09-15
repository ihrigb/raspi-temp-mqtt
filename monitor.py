#!/usr/bin/env python

import argparse
import logging
import threading
import time

from config import Config
from utils import log_setup, config_requirements, config_defaults, get_temp_thread


def main():
    # Setup argument parsing
    parser = argparse.ArgumentParser(description='Monitor Raspberry Pi core temperature and export to MQTT')
    parser.add_argument('-c', '--config', action='store', dest='config_directory', default='.',
                        help='Set config directory, default: \'.\'')
    parser.add_argument('-l', '--log-level', action='store', dest='log_level', default='INFO',
                        help='Set log level, default_ \'info\'')
    parser.add_argument('-d', '--log-destination', action='store', dest='log_destination', default='',
                        help='Set log destination (file), default \'\' (stdout)')
    parser.add_argument('--configtest', help='Parse config only', action='store_true')
    options = parser.parse_args()

    # Setup logging
    log_setup(options.log_level, options.log_destination)

    config = Config(options.config_directory, config_requirements, config_defaults)

    if options.configtest:
        exit(config.isvalid())

    if not config.isvalid():
        raise ValueError("Config found in directory {0} is not valid".format(options.config_directory))

    run_event = threading.Event()
    run_event.set()

    # Get temp thread
    temp = get_temp_thread(config.get_config('temp'), config.get_config('mqtt'), run_event)
    temp.start()

    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        logging.info('Signaling all threads to finish')

        run_event.clear()
        temp.join()

    logging.info('All threads finished. Exiting')


if __name__ == '__main__':
    main()
