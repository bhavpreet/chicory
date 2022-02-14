#!/usr/bin/env python3
import json
import urequests as requests

MOON_URL = "https://chicory-server.herokuapp.com/"
class moon:
    def __init__(self):
        pass

    def get(self):
        r = requests.get(MOON_URL)
        moonData = r.json()
        r.close()
        return moonData
