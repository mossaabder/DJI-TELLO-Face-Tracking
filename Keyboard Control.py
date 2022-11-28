from djitellopy import tello
import KeyPressModule as kp

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
me.takeoff()

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 80
    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("z"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("d"): yv = speed
    elif kp.getKey("q"): yv = -speed

    if kp.getKey("l"): yv = me.land()
    elif kp.getKey("t"): yv = me.takeoff()
    return [lr, fb, ud, yv]

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
