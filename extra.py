import pyautogui
import time


time.sleep(2)
pyautogui.typewrite('funLoadDetails(30);')
for i in range(155,200):
    pyautogui.typewrite(f'funLoadDetails({i});')
    pyautogui.press('enter')
    time.sleep(1)
    
    