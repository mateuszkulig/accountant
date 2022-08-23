import random
import time
import pyautogui

def decode_move(file):
    f = open(file, "r")
    c = 0
    moves = []
    while True:
        ln = f.readline()
        if ln =="":
            break
        print(c, ln, end="")
        sp = ln.split(" ")
        if sp[0] == "c":
            moves.append((int(sp[1]), int(sp[2])))
        c += 1
    f.close()

    for mv in moves:
        pyautogui.moveTo(mv[0], mv[1], 0.00001)

# def decode_move(file):
#     f = open(file, "r")
#     c = 0
#     while True:
#         ln = f.readline()
#         if ln =="":
#             break
#         print(c, ln, end="")
#         sp = ln.split(" ")
#         if sp[0] == "c":
#             pyautogui.moveTo(int(sp[1]), int(sp[2]), 0)
#         else:
#             time.sleep(float(sp[1]))
#
#         c += 1
#     f.close()

def sim_click():
    pyautogui.mouseDown()
    time.sleep(random.random()/20)
    pyautogui.moveRel(1, 1, 0)
    pyautogui.mouseUp()
    pyautogui.moveRel(-1, -1, 0)

# decode_move("swing1.txt")
# sim_click()
# decode_move("swing2.txt")
# sim_click()
# decode_move("swing3.txt")
# sim_click()
# decode_move("swing4.txt")
# sim_click()
# decode_move("swing5.txt")
# sim_click()
# decode_move("swing6.txt")
# sim_click()