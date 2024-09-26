#!/bin/bash; 
sudo apt update -y && sudo apt install wkhtmltopdf -y && sudo apt install python3-pip -y && python3 -m pip install -r req.txt && nohup python3 app.py > app.log 2>&1 & echo "Flask app started and running in the background. Logs can be found in app.log."
