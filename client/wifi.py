#!/usr/bin/env python3
import uos as os
import ujson as json
import network
import time
import web
import machine

ap_ssid = "Chicory"
ap_password = "12345678"
ap_authmode = 3 #wpa

class wifimgr:
    def __init__(self):
        self.sta_if = network.WLAN(network.STA_IF)
        self.ap_if = network.WLAN(network.AP_IF)

        print("Wake reason = ", machine.reset_cause())
        # if machine.reset_cause() == machine.WDT_RESET:
        if machine.reset_cause() == const.WAKE_REASON:
            self.reset()

    def reset(self):
        try:
            os.remove(const.WIFI_CONFIG_FILE)
        except:
            pass

    def start(self):
        f = ""
        try:
            f = open(const.WIFI_CONFIG_FILE, "r")
        except Exception as E:
            print("Unable to opening wifi file :", const.WIFI_CONFIG_FILE)
            print("Exception :", E)
            self.start_ap()

        while True:
            try:
                wifi_data = json.load(f)
                f.close()
                ssid = wifi_data["ssid"]
                password = wifi_data["password"]
                print("ssid = ", ssid, "password = ", password)
                # try connecting
                self.sta_if.active(True)
                self.sta_if.connect(ssid, password)
                while self.sta_if.isconnected() is False:
                    time.sleep(1)
                print ("Connected!")
                break
            except Exception as E:
                print("Exception occured: ", E)
                print("Will Retry...")

    def start_ap(self):
        #self.sta_if.active(True)
        self.ap_if.active(True)
        print("Starting AP..")
        self.ap_if.config(essid=ap_ssid, password=ap_password, authmode=ap_authmode)
        while self.ap_if.active() is False:
            print("sleeping..")
            time.sleep(1)
        web.run_ap(self.ap_if.ifconfig()[0])
