#!/bin/bash

cp new_years.json colors
sudo python3 /home/pi/run_lights.py > /home/pi/run_lights.log 2>&1 &
ps aux | grep run_lights | head -1 | awk '{print $2}' > /home/pi/run_lights.pid
export FLASK_APP=/home/pi/neopix_controller
flask run -h 0.0.0.0 > flask.log 2>&1 &
echo $! > /home/pi/flask.pid
