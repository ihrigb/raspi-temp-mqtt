from config import strip_config
import logging
import paho.mqtt.client as mqtt
from temp import TempThread

config_requirements = {
    'specs': {
        'required_entries': {'temp': dict, 'mqtt': dict}
    },
    'children': {
        'temp': {
            'specs': {
                'required_entries': {'topic': str, 'interval': int}
            }
        },
        'mqtt': {
            'specs': {
                'required_entries': {'host': str},
                'optional_entries': {'port': int,
                                     'keepalive': int,
                                     'auth': dict,
                                     'tls': dict}
            },
            'children': {
                'auth': {
                    'specs': {
                        'required_entries': {'username': str},
                        'optional_entries': {'password': str}
                    }
                },
                'tls': {
                    'specs': {
                        'optional_entries': {'ca_certs': str,
                                             'certfile': str,
                                             'keyfile': str,
                                             'cert_reqs': str,
                                             'tls_version': str,
                                             'ciphers': str}
                    }
                }
            }
        }
    }
}

config_defaults = {
    'mqtt': {
        'host': 'localhost'
    }
}


def log_setup(log_level, logfile):
    """Setup application logging"""

    numeric_level = logging.getLevelName(log_level.upper())
    if not isinstance(numeric_level, int):
        raise TypeError("Invalid log level: {0}".format(log_level))

    if logfile != '':
        logging.info("Logging redirected to: {0}".format(logfile))
        # Need to replace the current handler on the root logger:
        file_handler = logging.FileHandler(logfile, 'a')
        formatter = logging.Formatter('%(asctime)s %(threadName)s %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)

        log = logging.getLogger()
        for handler in log.handlers:
            log.removeHandler(handler)
        log.addHandler(file_handler)

    else:
        logging.basicConfig(format='%(asctime)s %(threadName)s %(levelname)s: %(message)s')

    logging.getLogger().setLevel(numeric_level)
    logging.info("log_level set to: {}".format(log_level))


def mqtt_init(mqtt_config):
    """Setup mqtt connection"""

    mqtt_client = mqtt.Client()

    if 'auth' in mqtt_config:
        auth = mqtt_config['auth']
        mqtt_client.username_pw_set(**auth)

    if 'tls' in mqtt_config:
        if mqtt_config['tls']:
            tls_config = mqtt_config['tls']
            mqtt_client.tls_set(**tls_config)
        else:
            mqtt_client.tls_set()

    mqtt_client.connect(**strip_config(mqtt_config, ['host', 'port', 'keepalive']))
    return mqtt_client


def publish(temperature, client, topic):
    client.publish(topic, temperature)


def get_temp_thread(temp_config, mqtt_config, run_event):
    if temp_config is None:
        logging.warn('No config')
        return {}

    return [TempThread(ind, mqtt_config, run_event, **d) for ind, d in enumerate(temp_config)]
