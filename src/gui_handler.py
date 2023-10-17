from PIL import ImageGrab

import cv2
import pygetwindow as gw
import numpy as np


class GUIHandler:
    def __init__(self, window_title, pid=None):
        self.window_title = window_title
        self.pid = pid

    def capture_screen(self):
        left, top, width, height = None, None, None, None
        window = gw.getWindowsWithTitle(self.window_title)
        if window:
            left, top, width, height = window[0].left, window[0].top, window[0].width, window[0].height

        if left is not None and top is not None and width is not None and height is not None:
            left, top, right, bottom = int(left), int(
                top), int(left + width), int(top + height)
            screen = ImageGrab.grab(
                bbox=(left, top, right, bottom))
            screen_np = np.array(screen)
            return cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)
        else:
            print(
                f"No se pudo encontrar la ventana con el título {self.window_title} o el PID {self.pid}.")
            return None
