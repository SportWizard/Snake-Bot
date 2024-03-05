import numpy as np
import cv2
import mss
import pyautogui
from PIL import Image
from pytesseract import pytesseract

running = True
template = cv2.imread("snake.png")
template2 = cv2.imread("apple.png")
save_screen = cv2.imread("save.png")

left_wall = 20
right_wall = left_wall + 580
top_wall = 20
botton_wall = top_wall + 500
wall_warning = 120

threshold = 0.75

method = cv2.TM_SQDIFF_NORMED

def screen_shot(left=0, top=0, width=1920, height=1080):
    stc = mss.mss()
    scr = stc.grab({
        'left': left,
        'top': top,
        'width': width,
        'height': height
    })

    img = np.array(scr)
    img = cv2.cvtColor(img, cv2.IMREAD_COLOR)

    return img

while running:
    screen = screen_shot(660, 320, 600, 530)

    #snake
    result = cv2.matchTemplate(screen, template, method)
    min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

    bottom_template_right = (location[0] + 50, location[1] + 50)

    cv2.rectangle(screen, location, bottom_template_right, (255, 0, 0), 5)

    #apple

    result2 = cv2.matchTemplate(screen, template2, method)
    min_value2, max_value2, min_loc2, max_loc2 = cv2.minMaxLoc(result2)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location2 = min_loc2
    else:
        location2 = max_loc2

    bottomtemplateRight2 = (location2[0] + 50, location2[1] + 50)

    cv2.rectangle(screen, location2, bottomtemplateRight2, (0, 0, 255), 5)

    #calculation
    print(location, location2)
    if location[0] > location2[0]:
        pyautogui.press("a")
    else:
        pyautogui.press("d")

    if location[1] > location2[1]:
        pyautogui.press("w")
    else:
        pyautogui.press("s")

    #boundaries
    if (location[0] - left_wall) < wall_warning:
        pyautogui.press("w")
    elif (location[0] - right_wall + 20) > (wall_warning * -1):
        pyautogui.press("w")
    if (location[1] - top_wall) < wall_warning:
        pyautogui.press("a")
    elif (location[1] - botton_wall + 20) > (wall_warning * -1):
        pyautogui.press("a")

    #save
    result3 = cv2.matchTemplate(screen, save_screen, method)
    min_value3, max_value3, min_loc3, max_loc3 = cv2.minMaxLoc(result3)

    print(max_loc3)
    if max_loc3 > threshold:
        pyautogui.press("space")

    cv2.imshow("Scanner", screen)

    key = cv2.waitKey(25)

    if key == ord("q"):
        running = False

cv2.destroyAllWindows()