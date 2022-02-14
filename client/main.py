from eink import eink
from moon import moon
import network
import machine
import time
from wifi import wifimgr
#from timezone import tz_mgr
import utime as time

def setupWifi(_eink):
    
    w = wifimgr()
    w.start()

    # sta_if = network.WLAN(network.STA_IF)
    # sta_if.active(True)
    # sta_if.connect('_b_', 'deepbreaths')
    # sta_if.ifconfig()

if __name__ == '__main__':
    while True:
        print("Initializing eInk display")
        try:
            # setup eink
            e = eink()
            print("eInk initialized")
        except Exception as E:
            print("Unable to initialize eink display...")
            print("Exception:", E)
            print("Retrying...")
            continue

        try:
            # setup wifi
            print("Seting up wifi")
            setupWifi(e)
        except Exception as E:
            print("Exception in settup wifi:", E)
            print("Retrying...")
            continue

        try:
            print("Seting up moon")
            # setup moon
            m = moon()
            moonData = m.get()
            print("Fireing...")
            e.display(moonData["moon_b"], moonData["moon_r"])
            print("DONE!")
        except Exception as E:
            time.sleep(5)
            print("Exception occured: ", E)

        t = time.localtime()
        t2 = time.mktime((t[0], t[1], t[2] + 1, 8, 00, t[5], t[6], t[7]))
        t1 = time.mktime(t)
        
        print("Deep sleeping till a new day...", t2-t1, "sec")
        # sleep for next 1 hours
        machine.deepsleep((t2 - t1) * 1000)
