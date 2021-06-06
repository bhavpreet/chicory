from moon.dialamoon import Moon
import cv2
import np
from PIL import Image
from datetime import datetime
from datetime import timedelta

SCALE_TO = (57, 57)
DIMENSIONS = (212, 104)

class moon:
    def __init__(self, width=DIMENSIONS[0], height=DIMENSIONS[1], mock=False):
        self.m = Moon()
        self.mock = mock
        self.width = width
        self.height = height
        self.moons = []
        self.aquiredMoonData = False
        self.setPhase()

    def setPhase(self, date=None, hour=None):
        self.today = ""
        self.yesterday = ""
        self.tomorrow = ""

        if date == None:
            date = datetime.today()# - timedelta(days=1)

        # return if we already have data for today.
        if self.aquiredMoonData and self.today == date.strftime('%Y-%m-%d'):
            return

        self.today = date.strftime('%Y-%m-%d')
        self.yesterday = (date - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (date + timedelta(days=1)).strftime('%Y-%m-%d')
        print(self.yesterday, self.today, self.tomorrow)

        if self.mock == True:
            self.m.image = cv2.imread("./mock_moon.png")
            self.moons = [self.m.image, self.m.image, self.m.image]
        else:
            self.m.set_moon_phase(self.yesterday, hour)
            self.moons.append(self.m.image)
            # Image.fromarray(self.m.image).save("/tmp/m1.png")

            self.m.set_moon_phase(self.today, hour)
            self.moons.append(self.m.image)
            # Image.fromarray(self.m.image).save("/tmp/m2.png")

            self.m.set_moon_phase(self.tomorrow, hour)
            self.moons.append(self.m.image)
            # Image.fromarray(self.m.image).save("/tmp/m3.png")
            self.aquiredMoonData = True

    def getImg_br(self, rotation=0):
        # LUT
        lut_in = [0, 36, 40, 67, 116, 255]
        lut_out = [0, 0, 30, 124, 180, 255]
        # lut_in = [0, 20, 50, 70, 90, 140, 200, 255]
        # lut_out = [0, 1, 10, 70, 140, 170, 250, 255]
        # lut_in = [0, 20, 80, 140, 200, 255]
        # lut_out = [0, 1, 10, 70, 200, 255]

        lut_8u = np.interp(np.arange(0, 256), lut_in, lut_out).astype(np.uint8)

        frameBuf = np.zeros((self.height,self.width,3), np.uint8)

        # lone_moon_eink = self.img_to_eink_hex(lone_moon)
        left_pad = 15
        inter_pad = 8
        y = 17
        for i in range(3):
            # convert('1') converts to black and white
            # TODO: Fix lone_moon
            lone_moon = self.moons[i]
            lone_moon = np.asarray(Image.fromarray(cv2.LUT(lone_moon, lut_8u)), np.uint8) #.convert('1')).astype(int)
            # Image.fromarray(lone_moon).show()
            lone_moon = cv2.resize(lone_moon, SCALE_TO)
            # x = (pad + (i * slot) + ((slot - SCALE_TO[0]) // 2))
            x = (left_pad + (SCALE_TO[0] * i) + (i * inter_pad))
            # Fill in the shape
            frameBuf[y:(y+lone_moon.shape[0]), x:(x+lone_moon.shape[1])] = lone_moon

            today = datetime.now()# - timedelta(days=1)
            day = ""
            if i == 0:
                day = "%s" % (today - timedelta(days=1)).date().day
            elif i == 1:
                day = "%s" % (today).date().day
            elif i == 2:
                day = "%s" % (today + timedelta(days=1)).date().day
                
            cv2.putText(
                frameBuf, #numpy array on which text is written
                day, #text
                (x + (SCALE_TO[0] // 4) + 3, y + SCALE_TO[1] + 16), #position at which writing has to start
                cv2.FONT_HERSHEY_DUPLEX, #font family
                0.3, #font size
                (255, 255, 255, 255), #font color
                1) #font stroke
           

        # add text
        # cv2.putText(
        #     frameBuf, #numpy array on which text is written
        #     "~ Moon Phases ~", #text
        #     (40, 98), #position at which writing has to start
        #     cv2.FONT_HERSHEY_SCRIPT_COMPLEX, #font family
        #     0.5, #font size
        #     (255, 255, 255, 255), #font color
        #     1) #font stroke
 
        if self.mock == True:
            Image.fromarray(frameBuf).show()
        # Rotate 270
        frameBuf = cv2.rotate(frameBuf, cv2.cv2.ROTATE_90_CLOCKWISE)
        frameBuf = cv2.rotate(frameBuf, cv2.cv2.ROTATE_90_CLOCKWISE)
        frameBuf = cv2.rotate(frameBuf, cv2.cv2.ROTATE_90_CLOCKWISE)

        # convert to b/w
        frameBuf = np.asarray(Image.fromarray(frameBuf).convert('1')).astype(int)

        # convert to black and white
        # gray = cv2.cvtColor(frameBuf, cv2.COLOR_BGR2GRAY)
        # frameBuf = cv2.threshold(gray, 100, 200, cv2.THRESH_BINARY)[1]
        # frameBuf = cv2.threshold(gray,100,200,cv2.THRESH_TOZERO)[1]
        # if self.mock == True:
        #     Image.fromarray(frameBuf).show()

        # embed lone_moon_eink into frameBuf in the center
        white = np.zeros((self.height,self.width,3), np.uint8)
        white.fill(255)
        white = cv2.rotate(white, cv2.cv2.ROTATE_90_CLOCKWISE)
        fb_eink = img_to_eink_hex(frameBuf)
        w_eink = img_to_eink_hex(white)
        return fb_eink, w_eink

    # def getImg_br(self, rotation=0):
    #     frameBuf = np.zeros((self.height,self.width,3), np.uint8)

    #     # lone_moon_eink = self.img_to_eink_hex(lone_moon)
    #     pad = 15
    #     slot = (self.width - pad * 2 )// 3

    #     y = 25
    #     for i in range(3):
    #         lone_moon = cv2.resize(self.moons[i], SCALE_TO)
    #         x = (pad + (i * slot) + ((slot - SCALE_TO[0]) // 2))
    #         frameBuf[y:(y+lone_moon.shape[0]), x:(x+lone_moon.shape[1])] = lone_moon

    #     frameBuf = cv2.rotate(frameBuf, cv2.cv2.ROTATE_90_CLOCKWISE)

    #     # Apply LUT
    #     lut_in = [0, 20, 80, 140, 200, 255]
    #     lut_out = [0, 1, 10, 70, 200, 255]
    #     lut_8u = np.interp(np.arange(0, 256), lut_in, lut_out).astype(np.uint8)
    #     frameBuf = np.asarray(Image.fromarray(cv2.LUT(frameBuf, lut_8u)).convert('1')).astype(int)

    #     # convert to black and white
    #     # gray = cv2.cvtColor(frameBuf, cv2.COLOR_BGR2GRAY)
    #     # frameBuf = cv2.threshold(gray, 100, 200, cv2.THRESH_BINARY)[1]
    #     # frameBuf = cv2.threshold(gray,100,200,cv2.THRESH_TOZERO)[1]
    #     # Image.fromarray(frameBuf).show()
    #     # embed lone_moon_eink into frameBuf in the center
    #     white = np.zeros((self.height,self.width,3), np.uint8)
    #     white.fill(255)
    #     white = cv2.rotate(white, cv2.cv2.ROTATE_90_CLOCKWISE)
    #     fb_eink = self.img_to_eink_hex(frameBuf)
    #     w_eink = self.img_to_eink_hex(white)
    #     return fb_eink, w_eink

    
def img_to_eink_hex(cim):
    byte = 8
    i = 0
    arr = []
    h = 0
    for r in cim:
        for c in r:
            bit = 1
            if type(c) == np.ndarray:
                if c[0] == 0:
                    bit = 0
            else:
                if c == 0:
                    bit = 0
            h = (h << 1) | bit
            i += 1

            if i == byte:
                i = 0
                arr.append(h)
                h = 0

    # print(len(cim[0]))
    # print_img(arr, len(cim[0]))
    return arr


if __name__ == '__main__':
    m = moon(mock=True)
    m.getImg_br()
