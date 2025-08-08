import numpy as np
import cv2
import mss
import pyautogui
import pygetwindow
from PIL import Image
from pytesseract import pytesseract
import threading

template = cv2.imread("snake.png")
template2 = cv2.imread("apple.png")

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
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    img = cv2.resize(img, (width // 2, height // 2))

    return img

def snake(screen):
    result = cv2.matchTemplate(screen, template, method)
    min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)

    # Use min_loc if the chosen method is TM_SQDIFF or TM_SQDIFF_NORMED
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        snake_loc = min_loc
    else:
        snake_loc = max_loc

    return snake_loc

def apple(screen):
    result2 = cv2.matchTemplate(screen, template2, method)
    min_value2, max_value2, min_loc2, max_loc2 = cv2.minMaxLoc(result2)

    # Use min_loc if the chosen method is TM_SQDIFF or TM_SQDIFF_NORMED
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        apple_loc = min_loc2
    else:
        apple_loc = max_loc2

    return apple_loc

def navigation(snake_loc, apple_loc):
    tolerance = 1

    # Snake
    if abs(snake_loc[0] - apple_loc[1]) > tolerance:
        pyautogui.press("a") if snake_loc[0] > apple_loc[0] else pyautogui.press("d")
    if abs(snake_loc[1] - apple_loc[1]) > tolerance:
        pyautogui.press("w") if snake_loc[1] > apple_loc[1] else pyautogui.press("s")

    # Boundaries
    if (snake_loc[0] - left_wall) < wall_warning or (snake_loc[0] - right_wall + 20) > (wall_warning * -1):
        pyautogui.press("w")
    if (snake_loc[1] - top_wall) < wall_warning or (snake_loc[1] - botton_wall + 20) > (wall_warning * -1):
        pyautogui.press("a") 

def process_frame(screen):
    snake_loc = snake(screen)
    apple_loc = apple(screen)

    print(f"Snake:", snake_loc)
    print(f"Apple:", apple_loc)

    navigation(snake_loc, apple_loc)  

def main():
    running = True
    window_name = "Snake Game — Mozilla Firefox"

    while running:
        game_window = pygetwindow.getWindowsWithTitle(window_name)[0]
        x, y, width, height = game_window.left, game_window.top, game_window.width, game_window.height

        screen = screen_shot(x, y, width, height)

        threading.Thread(target=process_frame, args=(screen,)).start()

        cv2.imshow("Scanner", screen)

        if cv2.waitKey(1) == ord("q"):
            running = False

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()