import utime
from servo import Servo
 
s1 = Servo(13)       # Servo pin is connected to GP0
 
def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 90:
        angle = 90
    s1.goto(round(servo_Map(angle,0,90,0,1024))) # Convert range value to angle value
    
if __name__ == '__main__':
    #servo_Angle(90)
    while True:
        print("Turn left ...")
        for i in range(30,90,10):
            servo_Angle(i)
            utime.sleep(0.2)
        print("Turn right ...")
        for i in range(90,30,-10):
            servo_Angle(i)
            utime.sleep(0.2)