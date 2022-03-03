# OLED REST-API

### **API for populating RPI-box OLED screen.** 

[![Version](https://img.shields.io/badge/Version-1.0-green)](https://stash.code.sintef.no/projects/NP/repos/rasputin_restapi/browse)
[![Status](https://img.shields.io/badge/Status-Operational-green)](https://app.gitkraken.com/glo/board/XmnjcgOfgAAUsewg)
[![Platform](https://img.shields.io/badge/Platform-Python_3.8-darkgreen)](https://www.python.org/downloads/release/python-380/)

### REST-API server

Python REST-API flask server for for RPI Linux-box onboard screen text inputs.

Various processes and code running on the box or remote can push text to the onboard screen through this API. API endpoints include various functionalities (clear screen, clear body text, make heading, write body line, write message, show image.)

API accessed over RPI ip (or localhost) on port 5000.
API documentation and webapp served on http://<ip address>:5000
API documentation and web-interface.

### REST-API client

The repo also contains a simplified Python client for the API found in 'oled_client.py'.
The 'Oled.connector' class can be imported in other Python code for easy API interfacing 

Python example for using the client:
```
    from oled_client import Oled_connector

    display = Oled_connector("localhost')
    print(oled.image(filename='logo.png')
    time.sleep(2)

    print(oled.message("Hello world!"))
    time.sleep(1)
```




## Authors
    Aslak Einbu 2022























