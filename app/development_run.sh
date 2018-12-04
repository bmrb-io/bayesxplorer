#!/bin/sh
export FLASK_APP=explorer.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port 8011
