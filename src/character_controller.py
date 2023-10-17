import pyautogui

class CharacterController:
    def __init__(self):
        pass

    def move_up(self):
        pyautogui.press('up')

    def move_down(self):
        pyautogui.press('down')

    def move_left(self):
        pyautogui.press('left')

    def move_right(self):
        pyautogui.press('right')

    def interact(self):
        pyautogui.press('a')

    def open_menu(self):
        pyautogui.press('enter')
