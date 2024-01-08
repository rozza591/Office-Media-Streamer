#!/bin/bash

echo 'Starting services...'
sleep 3

read -p 'Enter the IP which you want to stream on: ' ip_address

echo 'Activating PYENV...'
cd /bin/scripts/myenv/
source bin/activate
sleep 2

echo 'Starting TS Generator...'
sleep 2
python3 /bin/scripts/ts_generator.py
sleep 2

echo 'Starting Playlist Generator...'
sleep 10
python3 /bin/scripts/playlist_generator.py
sleep 2

echo 'Starting RTSP Server...'
sleep 3
../mediamtx
sleep 2

echo 'Starting Streamer with IP:', $ip_address
sleep 3
python3 /bin/scripts/streamer.py $ip_address
sleep 2

echo 'Services Started'
