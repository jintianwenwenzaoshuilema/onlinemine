import pyautogui
import win32gui
import win32api
import time
import numpy as np
import math
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import win32con
import re
from danmu import Danmu

WINDOW_TITLE = '扫雷'

bzhan = Danmu()


class mine():
    def __init__(self):
        self.gameover = 0
        self.gamewin = 0

        self.init()

    def init(self):
        self.getGameWindow()

    def getGameWindow(self):
        self.window = win32gui.FindWindow(None, WINDOW_TITLE)
        # 没有定位到窗体
        while not self.window:
            print('获取窗口失败，10秒后重新尝试')
            time.sleep(10)
            self.window = win32gui.FindWindow(None, WINDOW_TITLE)
        # 定位到窗体
        # 置顶窗口
        win32gui.SetForegroundWindow(self.window)
        pos = win32gui.GetWindowRect(self.window)
        print("Game windows at " + str(pos))


    def leftcilck(self, x, y):
        x = 25+x*20
        y = 75+y*20
        print(x, y)
        win32api.PostMessage(self.window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, (x & 0xffff) | ((y & 0xffff) << 16))
        win32api.PostMessage(self.window, win32con.WM_LBUTTONUP, 0, (x & 0xffff) | ((y & 0xffff) << 16))

    def rightclick(self, x, y):
        x = 25+x*20
        y = 75+y*20
        win32api.PostMessage(self.window, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, (x & 0xffff) | ((y & 0xffff) << 16))
        win32api.PostMessage(self.window, win32con.WM_RBUTTONUP, 0, (x & 0xffff) | ((y & 0xffff) << 16))

    def doubleclick(self, x, y):
        x = 25+x*20
        y = 75+y*20
        win32api.PostMessage(self.window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, (x & 0xffff) | ((y & 0xffff) << 16))
        win32api.PostMessage(self.window, win32con.WM_RBUTTONDOWN, win32con.MK_LBUTTON | win32con.MK_RBUTTON, (x & 0xffff) | ((y & 0xffff) << 16))
        win32api.PostMessage(self.window, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON | win32con.MK_RBUTTON, (x & 0xffff) | ((y & 0xffff) << 16))
        win32api.PostMessage(self.window, win32con.WM_RBUTTONUP, win32con.MK_LBUTTON, (x & 0xffff) | ((y & 0xffff) << 16))
        win32api.PostMessage(self.window, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, (x & 0xffff) | ((y & 0xffff) << 16))
        win32api.PostMessage(self.window, win32con.WM_LBUTTONUP, 0, (x & 0xffff) | ((y & 0xffff) << 16))




    def restart(self):
        zone = pyautogui.screenshot(region=(self.gamex, self.gamey, 502, 387))
        if self.gameover:
            img = Image.open('./data/gameover.bmp')
            for location in pyautogui.locateAll(img, zone, 0.7):
                x = location[0]+self.gamex
                y = location[1]+self.gamey
                x, y = pyautogui.center((x, y, 20, 20))
                pyautogui.click(x, y)
        if self.gamewin:
            img = Image.open('./data/gamewin.bmp')
            for location in pyautogui.locateAll(img, zone, 0.7):
                x = location[0]+self.gamex
                y = location[1]+self.gamey
                x, y = pyautogui.center((x, y, 20, 20))
                pyautogui.click(x, y)
        self.gameover = 0
        self.gamewin = 0
        self.playground = np.zeros([self.row, self.col], dtype=np.int32)
        self.onlineplay()

    def isidxvalid(self, x, y, a):
        if x >= 0 and x <= 20 and y >= 0 and y <= 30 and a >= 1 and a <= 3:
            return True
        return False

    def onlineupdateplayground(self):
        pass

    def onlinedig(self):
        msg = bzhan.get_danmu()
        print(msg)
        time.sleep(1)
        if msg:
            for move in msg:
                move = re.findall("[0-9]{1,2}-[0-9]{1,2}-[0-9]", move)
                if move:
                    move = move[0]
                    x, y, a = move.split('-')
                    x, y, a = int(x), int(y), int(a)
                    print(x, y, a)
                    if self.isidxvalid(x, y, a):
                        if a == 1:
                            self.leftcilck(y-1,x-1)
                        elif a == 2:
                            self.rightclick(y-1,x-1)
                        elif a == 3:
                            self.doubleclick(y-1,x-1)
        self.onlineupdateplayground()

    def onlineplay(self):
        while not self.gameover:
            self.onlinedig()
            if self.gamewin:
                break
        time.sleep(5)
        self.restart()

    

digmine = mine()
digmine.onlineplay()
