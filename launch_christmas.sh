#!/bin/bash

sudo python3 /home/pi/christmas.py > /home/pi/christmas.log 2>&1 &
export FLASK_APP=/home/pi/neopix_controller
flask run -h 0.0.0.0 > flask.log 2>&1 &