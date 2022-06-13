import time
import logging
import PIL.Image
import pyautogui
import win32api
# import pyfiglet
from itertools import product
from typing import List, Tuple
from key_check import ask_for_key, check_key
import multiprocessing
import keyboard
# import os

toggle_button = 'n'
autoshoot_button = 'ctrl'
auto_shoot_logger = logging.getLogger('auto_shoot')

COLORS = {
    'red': [(110, 29, 28), (160, 45, 35), (115, 20, 10)],
    'blue': [(45, 65, 65)],  # (36, 58, 61)],
    'r': [(110, 29, 28), (160, 45, 35), (115, 20, 10)],
    'b': [(45, 65, 65)]     # (54, 78, 83)]
}

ENEMY = 'red'

ENEMY_COLORS = COLORS[ENEMY]


def click_mouse(dx: int = 0, dy: int = 0) -> None:
    win32api.mouse_event(0x0002, dx, dy)
    time.sleep(0.1)  # 0.003, 0.02 - good, 0.05 - norm
    win32api.mouse_event(0x0004, 0, 0)


def get_center() -> List[int]:
    auto_shoot_logger.debug('Screen size is {} * {}'.format(*pyautogui.size()))
    return [side // 2 for side in pyautogui.size()]


CENTER = get_center()


def get_area(x1: int, y1: int, x2: int, y2: int) -> PIL.Image.Image:
    return pyautogui.screenshot(region=(x1, y1, x2, y2))


def do_colors_match(source_color: Tuple[int, int, int], target_color: Tuple[int, int, int], tolerance: int = 10) -> bool:
    delta = (abs(s_color - t_color) for s_color, t_color in zip(source_color, target_color))
    return all(map(lambda x: x <= tolerance, delta))


def is_enemy_in_scope(x_coord: int, y_coord: int, delta: int = 5) -> bool:
    area = get_area(x_coord - delta, y_coord - delta, x_coord + delta, y_coord + delta)
    return any((
        do_colors_match(color, area.getpixel((x, y)))
        for color in ENEMY_COLORS for x, y in product(range(delta * 2), repeat=2)
    ))


def check_profile() -> None:
    global ENEMY, ENEMY_COLORS

    ENEMY = input('Введите цвет врага (red/blue): ')

    if colors := COLORS.get(ENEMY):
        auto_shoot_logger.info('Changed enemy to {}'.format(ENEMY))
        ENEMY_COLORS = colors


def start_seeking() -> None:
    while True:
        if keyboard.is_pressed(toggle_button):
            auto_shoot_logger.info("Статус: OFF")
            time.sleep(0.1)
            return
        if is_enemy_in_scope(*CENTER):
            # auto_shoot_logger.debug('Enemy detected in {}, {}'.format(*CENTER))
            if keyboard.is_pressed(autoshoot_button):
                click_mouse()
                auto_shoot_logger.debug('Bang')
        time.sleep(.001)


def main() -> None:
    while not check_key():
        ask_for_key()
    #preview_config = pyfiglet.Figlet(font='standard')
    print('\nМодуль NAUTILUS установлен!\n')
    print('By Reisen "Ножевые Ранения" Raumberg\n')
    while True:
        check_profile()
        auto_shoot_logger.info("Статус: ON")
        auto_shoot_logger.debug('Starting macros')
        auto_shoot_logger.info('Starting seeking for enemy in coordinates {}, {}'.format(*CENTER))
        start_seeking()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s', datefmt='%H:%M:%S')
    main()
