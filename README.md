Raspberry Pi Neopixel Controller
---

This project contains a python application,
library, and flask web application to control
a NeoPixel string of lights.

[[_TOC_]]

### Hardware

- [NeoPixel Lights](https://www.amazon.com/gp/product/B06XD72LYM). There are many other
types of NeoPixel lights on the market
- [5v/10A AC-DC Power Supply for NeoPixel](https://www.amazon.com/gp/product/B01M0KLECZ). 
Other NeoPixel lights may come with a power supply
- Raspberry Pi Zero W with headers
- breadboard
- 2 breadboard to Pi Header Jumper Wires
- 1 74AHCT125 level converter chip: safely transmits Pi GPIO wire signal to
5v/10A power without feeding back to the Pi
- 8 breadboard to breadboard jumper wires, or solid core 24 awg wires

I used the following color scheme:
- red/orange wire: 5v power
- black wire: ground
- yellow wire: data
- blue wire: GPIO

### Wiring the Pi with the Lights

The [AdaFruit Python NeoPixel Tutorial](https://learn.adafruit.com/neopixels-on-raspberry-pi) is an excellent resource, with diagrams, for
wiring your Pi with your NeoPixel using the breadboard, wires, level converter,
NeoPixel and power supply.

### Configure the Pi Software

1. Install [Raspberry Pi OS](https://www.raspberrypi.org/software/operating-systems/) on an sd card.

I used the Raspberry Pi OS Lite image on a 32 GB SD card

2. Set up WIFI and ssh

I created a headless installation, with $yourmount defined as
/var/run/media/$(id -nu) on my fedora linux, by doing the following:
- mount the sd card on your workstation
- create $your_mount/boot/wpa_supplicant.conf. This must have the
correct country code (US for US), and the user and password for you 
wifi ssid
- touch $your_mount/boot/ssh.

The above instructs the raspberry pi on bootup to configure and connect to
wifi, and enable ssh automatically. The default user/password is pi:raspberry.
You should change this as soon as you login for the first time using the
passwd command.

You can also connect a monitor, keyboard, and mouse to the raspberry pi, and
use the graphical configuration, or raspi-config, to enable ssh, and connect to
wifi.

By default, the raspberry pi will register itself on your network as
raspberrypi.local. You can use this to refer to the server using ssh or
the web browser, or you can ping it to get its IP address, and use that
instead (this is especially useful if you have more than 1 raspberry pi
on your network).

Once you can ssh to the running pi, you can create /home/pi/.ssh, with 700
permission, and use secure copy or ssh-copy-id to copy a public ssh key to 
/home/pi/.ssh/authorized_keys to enable secure passwordless login to your pi
using ssh key authentication.

Alternatively, if you are on a linux workstation, the `rootfs` directory will mount
in ${yourmount} next to `boot`. This is the filesystem that is presented when the
raspberry pi boots. You can create the .ssh directory, and copy a public key into place 
before you boot the pi. Make sure the files are all owned by user 1000, group 1000
(pi user and group on the Raspbery Pi OS) after you copy them.

```bash
sudo mkdir /var/run/media/${SUDO_USER}/rootfs/home/pi/.ssh
sudo chmod 700 /var/run/media/${SUDO_USER}/rootfs/home/pi/.ssh
sudo cp ~/.ssh/$yourkey.pub /var/run/media/${SUDO_USER}/rootfs/home/pi/.ssh/authorized_keys
sudo chown -R 1000:1000 /var/run/media/${SUDO_USER}/rootfs/home/pi/.ssh
```

3. Install software

- requirements.txt
- launch_christmas.sh
- launch_new_years.sh
- lights_down.sh
- run_lights.py
- simpletest.py
- lib
- neopix_controller
- new_years.json
- christmas.json

You can either use secure copy once the pi is running and connected to your wifi,
of, if you are on a linux workstation, you can copy these into the `rootfs`
/home/pi directory, and ensure they are owned by 1000:1000

For users of fedora (possibly other Linux variants) there is a script,
configure_pi.fedora.sh, that will do all of the above.

4. Install requirements

This must be done on the running raspbery pi, either using the graphical interface
and a terminal, or using ssh

a. update and upgrade apt-get, then install pip3
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
```

b. install requirements
This must be done with sudo, since the GPIO pin 18 requires root (see below)
```
sudo pip3 install -r requirements.txt
```

### Usage

The NeoPixel control system consists of the following components:

1. lib/neopixc.py
This library implements the NeoPixC class that run_lights.py interacts with.
You can use it in a python3 interactive terminal to test some of its functions:

```bash
sudo python3
from lib.neopixc import NeoPixC
n = NeoPixC()
...
```

This library is designed to work with the ALITOVE WS2811 Addressable LED Pixel
Lights that I purchased, using the default Order=RGB. Some NeoPixel lights
require a different order argument. Consult the documentation for the NeoPixel
library for details if this does not work for you. It also uses the GPIO
board.D18 pin. This pin is the only GPIO pin on the raspberry pi that consistently
works with the NeoPixel. In order for programs to use this pin, the program must
run as root, using sudo. Some have found success using the SPI board.D10 pin.
I did not have success on my raspberry pi zero W. 

2. run_lights.py
This python script uses the NeoPixC object to interact with the NeoPixel.

It requires a json file /home/pi/colors, which should be a json array of arrays,
with each internal array being an RGB definition of integers. Examples can be
found in new_years.json and christmas.json.

It supports 3 states, as defined using the following words as one line in an
optional file /home/pi/state:
- down: turn lights off
- blink: blink colors
- static: static colors
If /home/pi/state does not exist, the default is static.

Since the GPIO board.D18 pin requires root to work, this script must
be run with sudo.

```bash
sudo python3 run_lights.py > run_lights.log 2>&1 &
```

Both /home/pi/state and /home/pi/colors can be changed while run_lights.py is
running to change its behavior dynamically.

3. The neopix_controller [Flask](https://flask.palletsprojects.com/en/1.1.x/) application. This application uses [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/) to present three colored buttons at the server root:
- Static (blue)
- Blinking (green)
- Turn Off (red)

These use a javascript library neopix_controller/static/js/callbacks to interact
with the rest endpoints:
- /api/v1/state: returns the value in /home/pi/state. Returns
`static` if the file does not exist. Allows the frontend to display the
current state on page load, and after a button is pushed
- /api/v1/static: changes the value of /home/pi/state, and the frontend, to `static`
- /api/v1/blink: changes the value of /home/pi/state, and the frontend, to `blink`
- /api/v1/down: changes the value of /home/pi/state, and the frontend, to `down`
static, blink, and down will create /home/pi/state if it does not exist.

To run the application, make sure to bind it to 0.0.0.0 so other
computers on your wifi network can use it:

```bash
export FLASK_APP=/home/pi/neopix_controller
flask run -h 0.0.0.0 > flask.log 2>&1 &
```

launch_christmas.sh and launch_new_years.sh are scripts that run all of the above.
They do not require sudo, but require your user to be in the sudo group.

Navigate to either raspberrypi.local:5000, or its IP address.
You can also GET raspberrypi.local:5000/api/v1/state, static, blink, down
to test the API methods.

To bring the entire application (run_lights and the flask application) down,
you can run lights_down.sh.

***NOTE*** This application is not meant for production use, and is not very secure. It
meant for instructional use only, using a secure home network.

