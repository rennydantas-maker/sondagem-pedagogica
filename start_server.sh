#!/bin/bash
cd /home/ubuntu/sondagem-app
export FLASK_APP=app.py
export FLASK_ENV=production
python3 app.py
