from djitellopy import tello
from time import sleep

me = tello.Tello()
me.connect()
me.takeoff()
sleep(4)
me.send_rc_control(0, 50, 0, 0)
sleep(2)
me.send_rc_control(0, -50, 0, 0)
sleep(2)
me.land()