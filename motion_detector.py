import time
import network
import urequests
from machine import Pin, I2C
import neopixel
from mpu import MPU
from machine import Timer


ssid = "qwer"
key = "0902232907"
neo_pin = Pin(0, Pin.OUT)
neo_power = Pin(2, Pin.OUT,Pin.PULL_UP)
num_led = 1
neo_power.value(1)
np = neopixel.NeoPixel(neo_pin,num_led)
led = Pin(13, Pin.OUT)
led.value(0)
armed = 0
timer = Timer(0)
THINGSPEAK_URL = "https://api.thingspeak.com/channels/3197083/fields/1.json?api_key=CCTDR170TJCO5DAN&results=1"
IFTTT_URL = "https://maker.ifttt.com/trigger/motion_notification/with/key/dRoABceAQVLTv37k8GgO0M4F38PtLTcdi5Ebz4vG8-7"


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid,key)
        while not wlan.isconnected():
            pass
    print('Connected to', ssid)
    print('IP Address:', wlan.ifconfig()[0])


def read_thingspeak():
    res = urequests.get(THINGSPEAK_URL)
    data = res.json()
    res.close()
    feeds = data.get("feeds", [])
    cmd = feeds[0].get("field1", "")
    return cmd.strip().lower()


def send_notification(x, y, z):
    url = f"{IFTTT_URL}?value1={x}&value2={y}&value3={z}"
    res = urequests.get(url)
    res.close()


def callback_thingspeak(timer):
    global armed
    cmd = read_thingspeak()
    if cmd == "1":
        armed = True
        np[0] = (0,100,0)
        np.write()

    elif cmd == "0":
        armed = False
        np[0] = (0,0,0)
        np.write()



def calibrate_sensor(mpu, samples=20):
    total_x = 0
    total_y = 0
    total_z = 0
    for _ in range(samples):
        ax, ay, az = mpu.acceleration()
        total_x += ax
        total_y += ay
        total_z += az
        time.sleep(0.05)
    base = (total_x / samples,total_y / samples,total_z / samples,)
    return base


def motion_detected(current, base):
    dx = abs(current[0] - base[0])
    dy = abs(current[1] - base[1])
    dz = abs(current[2] - base[2])

    if dx > 3 or dy > 3 or dz > 3:
        return True
    return False

def main():
    do_connect()
    i2c = I2C(0, scl=Pin(14), sda=Pin(22))
    mpu = MPU(i2c)
    base = calibrate_sensor(mpu)
    print("Calibration done")
    if armed:
        np[0] = (0, 100, 0)
    else:
        np[0] = (0, 0, 0)
    np.write()
    timer.init(period = 30000,mode = Timer.PERIODIC,callback = callback_thingspeak)
    pre_state = False

    while True:
        if armed: 
            ax, ay, az = mpu.acceleration()
            current = (ax, ay, az)
            moving = motion_detected(current, base)

            if moving and not pre_state:
                send_notification(ax, ay, az)
                led.value(1)
                time.sleep(2)

            elif not moving and pre_state:
                led.value(0)

            pre_state = moving

if __name__ == "__main__":
    main()
