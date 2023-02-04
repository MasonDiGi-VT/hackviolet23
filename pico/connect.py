import network
import time
import ntptime

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Apache HTTP Server', '12345678')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

print(wlan.ifconfig())

#while True:
#    try:
#        ntptime.settime()
#        break
#    except:
#        pass
#tm = time.localtime()
#machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3]-5, tm[4], tm[5], 0))
#print(time.localtime())