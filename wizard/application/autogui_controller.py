import pyautogui

def move_cursor(x, y):
    pyautogui.moveTo(x, y)

def press_left_mouse_button():
    pyautogui.mouseDown(button='left')

def release_left_mouse_button():
    pyautogui.mouseUp(button='left')

def click_right_mouse_button():
    pyautogui.click(button='right')
    