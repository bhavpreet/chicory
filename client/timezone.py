#!/usr/bin/env python3
import uos as os
import network
import time
import web
import machine
import urequests as requests
import ujson as json

class tz_mgr:
    def __init__(self):
        print("Wake reason = ", machine.reset_cause())
        # if machine.reset_cause() == machine.WDT_RESET:
        if machine.reset_cause() == const.WAKE_REASON:
            self.reset()

        self.tz_info = self.get_local_time()

    def reset(self):
        try:
            os.remove(const.LOCATION_FILE)
        except:
            pass

    def get_local_time(self):
        print("Loading location.")
        while True:
            try:
                f = open(const.LOCATION_FILE)
                f.close()
                return json.load(f.read())
            except Exception as E:
                self.find_location()
                print("Location: retrying...")


    def find_location(self):
        try:
            print("Fetching Location.")
            resp = requests.get("http://ip-api.com/json")
            f = open(const.LOCATION_FILE, "w")
            f.write(json.dumps(resp.json()))
            f.close()
        except:
            raise
            
            
