##--------------------------------------
## LastCommit 2020/10/23 17:00
## PWM実装
##--------------------------------------

#import
import sys
#import Jetson.GPIO as GPIO
import  RPi.GPIO as GPIO
import time
import struct
import threading

#初期設定
tick1 = 50
tick2 = 50
usleep = lambda x: time.sleep(x/1000000.0)
GPIO.setwarnings(False)
prev_value = None

device_path = "/dev/input/js0"
EVENT_FORMAT = "LhBB"
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
##PWM用GPIO
GPIO.setup(32, GPIO.OUT, initial=GPIO.HIGH)
p1 = GPIO.PWM(32, 50)
GPIO.setup(33, GPIO.OUT, initial=GPIO.HIGH)
p2 = GPIO.PWM(33, 50)


try:
    # ##---PWM---
    # def pwm_1():
    #     global tick1
    #     scl=50
    #     #GPIO.output(12, GPIO.HIGH)
    #     GPIO.output(18, GPIO.HIGH)
    #     usleep(tick1*scl)
    #     #GPIO.output(12,GPIO.LOW)
    #     GPIO.output(18, GPIO.LOW)
    #     usleep((100-tick1)*scl)

    # def pwm_2():
    #     global tick2
    #     scl=50
    
    #     GPIO.output(12, GPIO.HIGH)
    #     #GPIO.output(18, GPIO.HIGH)
    #     usleep(tick2*scl)
    #     GPIO.output(12,GPIO.LOW)
    #     #GPIO.output(18, GPIO.LOW)
    #     usleep((100-tick2)*scl)

    # thread1 = threading.Thread(target = pwm_1)
    # thread2 = threading.Thread(target = pwm_2)
    # thread1.setDaemon(True)
    # thread2.setDaemon(True)

    # thread1.start()
    # thread2.start()


    with open(device_path, "rb") as device:
        event = device.read(EVENT_SIZE)
        while event:
            (ds3_time, ds3_val, ds3_type, ds3_num) = struct.unpack(
                EVENT_FORMAT, event)
            #print("{0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))
            if ds3_type == 1:
            #     if ds3_num == 10:
            #         GPIO.output(21, GPIO.LOW)
            #         GPIO.output(19, GPIO.HIGH)
            #         GPIO.output(24, GPIO.LOW)
            #         GPIO.output(22, GPIO.HIGH)
            #         print("up")
            #     elif ds3_num == 11:
            #         GPIO.output(21, GPIO.HIGH)
            #         GPIO.output(19, GPIO.LOW)
            #         GPIO.output(24, GPIO.HIGH)
            #         GPIO.output(22, GPIO.LOW)
            #         print("down")
                if ds3_num == 3:
                    GPIO.output(21, GPIO.HIGH)
                    GPIO.output(19, GPIO.HIGH)
                    GPIO.output(24, GPIO.HIGH)
                    GPIO.output(22, GPIO.HIGH)
                    print("stop")
                # elif ds3_num == 4:
                #     if(tick1 <= 90):
                #         tick1 += 10
                #     else:
                #         tick1 = 100
                #     print("Speed right"+str(tick1))
                # elif ds3_num == 6:
                #     if(tick1 >= 10):
                #         tick1 -= 10
                #     else:
                #         tick1 = 0
                #     print("Speed right"+str(tick1))
                # elif ds3_num == 12:
                #     if(tick2 <= 90):
                #         tick2 += 10
                #     else:
                #         tick2 = 100
                #     print("Speed left"+str(tick2))
                # elif ds3_num == 14:
                #     if(tick2 >= 10):
                #         tick2 -= 10
                #     else:
                #         tick2 = 0
                #     print("Speed left"+str(tick2))
            if ds3_type == 2:
                if ds3_num == 1:
                    if ds3_val>0:
                        GPIO.output(21, GPIO.HIGH)
                        GPIO.output(19, GPIO.LOW)
                        GPIO.output(24, GPIO.HIGH)
                        GPIO.output(22, GPIO.LOW)
                        tick1=int((ds3_val/32767)*100)+20
                        if tick1>100:
                            tick1=100
                    if ds3_val<0:
                        GPIO.output(21, GPIO.LOW)
                        GPIO.output(19, GPIO.HIGH)
                        GPIO.output(24, GPIO.LOW)
                        GPIO.output(22, GPIO.HIGH)
                        tick1=int(((ds3_val*(-1))/32767)*100)+20
                        if tick1>100:
                            tick1=100
                    if ds3_val==0:
                        GPIO.output(21, GPIO.HIGH)
                        GPIO.output(19, GPIO.HIGH)
                        GPIO.output(24, GPIO.HIGH)
                        GPIO.output(22, GPIO.HIGH)
                        tick1=0
                if ds3_num == 3:
                    if ds3_val>0:
                        GPIO.output(21, GPIO.HIGH)
                        GPIO.output(19, GPIO.LOW)
                        GPIO.output(24, GPIO.HIGH)
                        GPIO.output(22, GPIO.LOW)
                        tick2=int((ds3_val/32767)*100)+20
                        if tick2>100:
                            tick2=100
                    if ds3_val<0:
                        GPIO.output(21, GPIO.LOW)
                        GPIO.output(19, GPIO.HIGH)
                        GPIO.output(24, GPIO.LOW)
                        GPIO.output(22, GPIO.HIGH)
                        tick2=int(((ds3_val*(-1))/32767)*100)+20
                        if tick2>100:
                            tick2=100
                    if ds3_val==0:
                        GPIO.output(21, GPIO.HIGH)
                        GPIO.output(19, GPIO.HIGH)
                        GPIO.output(24, GPIO.HIGH)
                        GPIO.output(22, GPIO.HIGH)
                        tick2=0



                    
            p1.start(tick1)
            p2.start(tick2)
            event = device.read(EVENT_SIZE)

except KeyboardInterrupt:
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    GPIO.cleanup()
    sys.exit

# 終了処理
finally:
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    GPIO.cleanup()
    sys.exit
