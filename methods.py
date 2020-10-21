from python_imagesearch.imagesearch import *

def imageSearchAndClickLoop(image, timesample, precision=0.8):
    pos = imagesearch_loop(image, timesample, precision)
    pyautogui.moveTo(pos[0], pos[1], 0.05)
    pyautogui.click()

def imageSearchAndClick(image, precision=0.8) -> bool:
    pos = imagesearch(image, precision)
    if pos[0] != -1:
        pyautogui.moveTo(pos[0], pos[1], 0.05)
        pyautogui.click()
        return True
    return False
