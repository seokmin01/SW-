#!/usr/bin/env python
# -*- coding: utf-8 -*

####################################################################
# 프로그램명 : joy_cam.py
# 작 성 자 : 자이트론
# 생 성 일 : 2020년 07월 23일
# 본 프로그램은 상업 라이센스에 의해 제공되므로 무단 배포 및 상업적 이용을 금합니다.
####################################################################

import rospy, rospkg
import time
import serial
import threading
from xycar_msgs.msg import xycar_motor

import signal
import sys
import os

def signal_handler(sig, frame):
    import time
    time.sleep(3)
    os.system('killall -9 python rosout')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

Angle = 90
Speed = 90
angle_offset = -5.0
g_chk_time = 0.0
angle_ratio = 1.8
speed_ratio = 1.8

def th_motor():
    global Angle, Speed, g_chk_time, seridev

    r = rospy.Rate(10)
    while True:
       if (time.time() - g_chk_time) > 2:
          Speed = 90

       sndData = str.format("R,{},{}",Angle, Speed)
       #rospy.loginfo("R,"+str(Angle)+","+str(Speed))
       seridev.write(sndData)
       r.sleep()

def callback(data):
    global Angle, Speed, g_chk_time, angle_offset

    g_chk_time = time.time()

    data.angle = max(-70, min(data.angle, 70))
    data.speed = max(-50, min(data.speed, 50))
    print('angle : ', data.angle, ' speed ', data.speed)
    Angle = int((data.angle + 50) * angle_ratio)
    Angle -= int(angle_offset * angle_ratio)
    Angle = 100 * angle_ratio - Angle
    Speed = int((data.speed + 50) * speed_ratio)
    #print('angle11 : ', Angle, ' speed11 ', Speed)

def start():
    rospy.init_node('xycar_motor_c1')
    angle_offset = rospy.get_param("~angle_offset")

    rospy.Subscriber("xycar_motor", xycar_motor, callback, queue_size = 1)

    th = threading.Thread(target=th_motor)
    th.start()

    rospy.spin()

if __name__ == '__main__':
    global seridev

    seridev = serial.Serial('/dev/ttyMOTOR', 115200)
    start()
