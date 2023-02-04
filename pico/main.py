import time
from machine import Pin, Timer, I2C
from time import sleep
from pico_i2c_lcd import I2cLcd
import connect
import servotest

# global variables
buttonPressed = False
startTime = 0
inSetup = False

from twilio import TwilioSMS as Client
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC71aad870e880b93b2e6edb0a45f85109'
auth_token = '88eb7a1482ee5a7e555c1019ac2d84c0'
client = Client(account_sid, auth_token)
def send(text):
  message = client.create(
                     body=text,
                     from_='+18333130978',
                     to='+19088093670'
                 )

  print(message.text)


def getButton():
    return Pin("GP5", mode=Pin.IN, pull=Pin.PULL_DOWN).value()


def callback(pin):
    global buttonPressed
    if (not inSetup):
        buttonPressed = True
        servotest.servo_Angle(0)
        time.sleep(0.5)
        servotest.servo_Angle(90)
        


def pillTimer(current_pill_number):
  global buttonPressed
  count = 0
  while(count < 5):
    pills_missed_in_a_row = 0
    count = count + 1
    if (buttonPressed):
      current_pill_number = current_pill_number + 1
      pills_missed_in_a_row = 0
      break
    else:
        pass
  if (not buttonPressed):
    send("you missed your birth control today, please try not to miss it tommorow")
    #print("you missed your birth control today, please try not to miss it tommorow")
    pills_missed_in_a_row = pills_missed_in_a_row + 1
    if (pills_missed_in_a_row >= 2):
      send("You forgot to take your birth control for" + pills_missed_in_a_row + "days in a row, your protection from pregnacy may be affected")
      #print("You forgot to take your birth control for" + pills_missed_in_a_row + "days in a row, your protection from pregnacy may be affected")
  buttonPressed = False
  return current_pill_number
    
    
def pillTimer():
    if not buttonPressed:
      send("make sure you take you birth control today")
      #print("make sure you take you birth control today")
        

def PT():
    def missed():
        global buttonPressed
        if (not buttonPressed):
            #print("you missed your birth control today, please try not to miss it tommorow")
            send("you missed your birth control today, please try not to miss it tommorow")
        buttonPressed = False
    for i in range(6):
        timer = Timer(period=2000*i, mode=Timer.ONE_SHOT, callback=lambda t: pillTimer())
    
    timer = Timer(period=2000*6, mode=Timer.ONE_SHOT, callback=lambda t: missed())


def setupLoop(lcd):
    global inSetup
    inSetup = True
    timeButton = Pin("GP6", mode=Pin.IN, pull=Pin.PULL_DOWN)
    pickButton = Pin("GP5", mode=Pin.IN, pull=Pin.PULL_DOWN)
    startTime = 0
    while True:
        if (timeButton.value() == 1):
            startTime = (startTime+1) % 24
            lcd.clear()
            lcd.putstr("Set interval:\n")
            lcd.putstr(f"{startTime:02d}:00-{(startTime+3)%24:02d}:00")
            time.sleep(0.1)
        if (pickButton.value() == 1):
            lcd.clear()
            lcd.putstr("Program Set")
            time.sleep(1)
            inSetup = False
            return startTime
        time.sleep(0.01)


if __name__ == "__main__":
    #pill = 0
    #PT()
    #timeButton.irq(trigger=Pin.IRQ_RISING, handler=nextTime)
    print(time.localtime())
    servotest.servo_Angle(90)
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    I2C_ADDR = i2c.scan()[0]
    lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
    lcd.putstr("Set interval:\n")
    lcd.putstr("00:00-03:00")
    startTime = setupLoop(lcd)
    lcd.clear()
    lcd.putstr("Take Pills from:\n")
    lcd.putstr(f"{startTime:02d}:00-{(startTime+3)%24:02d}:00")
    
    
    pickButton = Pin("GP5", mode=Pin.IN, pull=Pin.PULL_DOWN)
    pickButton.irq(trigger=Pin.IRQ_RISING, handler=callback)
    now = time.localtime()
    start = list(now)
    start[3] = startTime
    start[4] = 0
    waitTime = time.mktime(tuple(start))-time.mktime(now)
    if waitTime < 0:
        waitTime = time.mktime(tuple(start))+24*60*60 - time.mktime(now)
    #sleep(waitTime)
    PT()
    timer = Timer(period=24*60*60*1000, mode=Timer.PERIODIC, callback=lambda t: PT())
    while True:
        pass