import serial
import requests

ser = serial.Serial('COM3', 9600)  # 아두이노 포트에 맞게 수정

while True:
    if ser.in_waiting > 0:
        finger_id = ser.readline().decode().strip()
        print(f"[INFO] Detected Finger ID: {finger_id}")
        res = requests.post("http://localhost:8000/send", json={"finger_id": finger_id})
        print(res.json())
