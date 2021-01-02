#!/bin/bash
if [ -f /home/pi/run_lights.pid ]
then
    sudo kill -s HUP $(cat /home/pi/run_lights.pid)
    run /home/pi/run_lights.pid
fi

if [ -f /home/pi/flask.pid ]
then
    kill $(cat /home/pi/flask.pid)
    rm /home/pi/flask.pid
fi
