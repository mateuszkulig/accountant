from ppadb.client import Client as AdbClient
from os import system as powershell
import time
import requests

def start_server():
    """start the adb server from adb/adb.exe"""
    powershell(".\\adb\\adb.exe start-server")

def kill_server():
    """kill the adb server from adb/adb.exe"""
    powershell(".\\adb\\adb.exe kill-server")

def get_ip():
    """get ip addres from ident.me"""
    response = requests.get("https://api.ipify.org")
    print(response)
    return response.text

def network_reset(dev):
    """use the adb input tap command with x and y"""
    start_ip = get_ip()
    print(f"current ip {start_ip}")
    dev.shell(
        "input tap 1200 650; sleep 1; input tap 1200 1650; sleep 1; input tap 1200 650; sleep 1; "
        "input tap 1200 1150; sleep 1"
    )
    time.sleep(5)
    while True:
        try:
            print(f"new ip {get_ip()}")
            break
        except requests.exceptions.ConnectionError:
            continue
    # while get_ip() == start_ip:
    #     time.sleep(1)

def setup():
    """setup adb device"""
    client = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037
    return client.devices()[0]

if __name__ == "__main__":
    phone = setup()
    for i in range(5):
        network_reset(phone)
