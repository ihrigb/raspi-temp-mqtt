# Raspberry Pi Core Temperature to MQTT

Ready the core temperature of raspberry pi and sends it via MQTT.

# Installation

1. Clone this repo.
2. Install required modules: `pip install -r requirements.txt`
3. Create a directory for the configuration files (eg `mkdir ./config`)
4. Add configuration files (see exampleconfig directory)
5. Start application `./monitor.py -c <path_to_your_config_dir>` (optional `-l debug`)

## systemd startup-script

Modify `examplescripts/raspi-temp.service` to mach your setup and copy it to an appropriate place. E.g. `/lib/systemd/system/raspi-temp.service`.

Run `systemctl daemon-reload && systemctl enable raspi-temp && systemctl start raspi-temp`

Next time on boot, raspi-temp will connect and run.

# Credits

Credits to https://github.com/bendikwa/igrill.
