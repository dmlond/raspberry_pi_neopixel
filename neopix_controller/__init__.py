#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify
import os
from flask_bootstrap import Bootstrap
from pathlib import Path

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  Bootstrap(app)

  @app.route('/')
  def index():
      return render_template('index.html',path=__path__)
  
  @app.route('/api/v1/state')
  def christmas_state():
    try:
      current_state = Path('/home/pi/state').read_text().rstrip()
    except FileNotFoundError:
      # default
      current_state = 'static'
    return current_state

  @app.route('/api/v1/down')
  def christmas_down():
    with open('/home/pi/state', 'w') as the_file:
      the_file.write('down')
    return 'down'

  @app.route('/api/v1/blink')
  def christmas_blink():
    with open('/home/pi/state', 'w') as the_file:
      the_file.write('blink')
    return 'blink'

  @app.route('/api/v1/static')
  def christmas_static():
    with open('/home/pi/state', 'w') as the_file:
      the_file.write('static')
    return 'static'

  return app
