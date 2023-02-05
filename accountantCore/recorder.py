import pyautogui
import time
import random

f = open("test.txt", "w")
lasttime = time.time()
newtime = time.time()
lastx = 0
lasty = 0
start = False
end = False
counter = 0
while True:
    x, y = pyautogui.position()
    if lastx != x and lasty != y:
        print(x, y)
        f.write(f"c {x} {y}\n")
        lastx = x
        lasty = y
        start = False
    else:
        if not start:
            lasttime = time.time()
            if counter == 0:
                counter = random.random()/1000
            print(counter)
            f.write(f"t {counter}\n")
        start = True
    if start:
        counter = time.time() - lasttime

    time.sleep(0.000001)