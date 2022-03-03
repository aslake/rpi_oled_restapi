"""
Client class for OLED REST-API.
Simplified access to onboard screen control from python scripts.

Import the Oled_connector class into you Python script for easy interfacing.

Aslak Einbu 2022
"""
import time
import requests
from requests.utils import quote

api_ip= '192.168.1.158'

class Oled_connector():
    """ Class for sending text to RPI onboard OLED screen. """
    def __init__(self, api_ip):
        self.ip = api_ip

    def clearscreen(self):
        """ Clear screen """
        return (requests.get(f"http://{self.ip}:5000/screen/clearscreen").text)

    def clearbody(self):
        """ Clear body text (not header) """
        return (requests.get(f"http://{self.ip}:5000/screen/clearbody").text)

    def body(self, text):
        """ Body text in small """
        return (requests.get(f"http://{self.ip}:5000/screen/body", params=f"text={quote(text)}").text)

    def header(self, text):
        """ Headline text """
        return (requests.get(f"http://{self.ip}:5000/screen/header", params=f"text={quote(text)}").text)

    def message(self, text):
        """ Message text """
        return (requests.get(f"http://{self.ip}:5000/screen/message", params=f"text={quote(text)}").text)

    def image(self, filename, rotate="False", background="white"):
        """ Show image file """
        return (requests.get(f"http://{self.ip}:5000/screen/image", params={'filename':quote(filename), 'rotate':quote(rotate),'background':quote(background)}).text)


if __name__ == '__main__':
    oled = Oled_connector(api_ip)
    print(oled.image(filename='logo.png', rotate="True"))
    time.sleep(2)
    print(oled.message("Testscript"))
    time.sleep(1)

    print(oled.clearscreen())
    time.sleep(1)

    print(oled.header('TEST'))
    for     i in range(10):
            print(oled.body(f"Writing line {i}"))
            time.sleep(0.5)
    print(oled.clearbody())
    
    time.sleep(1)

    print(oled.header('TEST 2'))
    for     i in range(10):
            print(oled.body(f"Writing line {i}"))
            time.sleep(0.5)
    print(oled.clearbody())
    
    print(oled.message("TEST FINISHED"))
