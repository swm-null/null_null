#!bin/bash
nohup poetry run uvicorn main:app --reload --ssl-keyfile=./ssl/key.pem --ssl-certfile=./ssl/cert.pem --host 192.168.1.12 > nohup.log &
