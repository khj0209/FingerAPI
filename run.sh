#!/bin/bash

echo "[+] Installing dependencies..."
pip install -r requirements.txt

echo "[+] Initializing DB..."
python backend/database.py

echo "[+] Starting API server..."
python backend/main.py &
sleep 2

echo "[+] Starting serial listener..."
# python serial_listener/listener.py
