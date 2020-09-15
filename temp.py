import logging
import threading
import time
import os

import utils


def read_temperature():
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp.replace("temp=", "")


class TempThread(threading.Thread):
    def __init__(self, thread_id, mqtt_config, run_event, topic, interval):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.mqtt_client = utils.mqtt_init(mqtt_config)
        self.topic = topic
        self.interval = interval
        self.run_event = run_event

    def run(self):
        while self.run_event.is_set():
            try:
                logging.debug("Temp thread (re)started, trying to get temperature")
                self.mqtt_client.reconnect()
                while True:
                    temperature = read_temperature()
                    utils.publish(temperature, self.mqtt_client, self.topic)
                    logging.debug("Published temp: {} to topic: {}.".format(temperature, self.topic))
                    logging.debug("Sleeping for {} seconds".format(self.interval))
                    time.sleep(self.interval)
            except Exception as e:
                logging.debug(e)
                logging.debug("Sleeping for {} seconds before retrying".format(self.interval))
                time.sleep(self.interval)

        logging.debug("Thread exiting")
