import pygame as pg
import pygame_menu as pg_menu

from . import ai
from . import config
from .cli import run_local_gui, run_local_pvp, host_online_pvp, join_online_pvp
from .localization import translate
from .menu_names import *


def main_menu(window):
    menu = default_menu()
    menu.add_button(translate(PVE_BUTTON), difficulty_menu, window)
    menu.add_button(translate(PVP_BUTTON), local_or_remote_pvp_menu, window)
    menu.add_button(translate(QUIT_BUTTON), pg_menu.events.EXIT)
    menu.mainloop(window)


def difficulty_menu(window):
    menu = default_menu()
    menu.add_button(translate(EASY_BUTTON), run_local_gui, ai.Difficulty.easy)
    menu.add_button(translate(NORMAL_BUTTON), run_local_gui, ai.Difficulty.normal)
    menu.add_button(translate(HARD_BUTTON), run_local_gui, ai.Difficulty.hard)
    menu.add_button(translate(BACK_BUTTON), main_menu, window)
    menu.mainloop(window)


def local_or_remote_pvp_menu(window):
    menu = default_menu()
    menu.add_button(translate(THIS_COMPUTER_BUTTON), run_local_pvp)
    menu.add_button(translate(TWO_COMPUTERS_BUTTON), host_or_join_menu, window)
    menu.add_button(translate(BACK_BUTTON), main_menu, window)
    menu.mainloop(window)


def host_or_join_menu(window):
    menu = default_menu()
    menu.add_button(translate(HOST_BUTTON), host_menu, window)
    menu.add_button(translate(JOIN_BUTTON), join_menu, window)
    menu.add_button(translate(BACK_BUTTON), local_or_remote_pvp_menu, window)
    menu.mainloop(window)


def host_menu(window):
    menu = default_menu()
    port_input_button = menu.add_text_input(translate(PORT_INPUT), input_type=pg_menu.locals.INPUT_INT)
    menu.add_button(translate(CREATE_AND_WAIT), host_game, port_input_button, window)
    menu.add_button(translate(BACK_BUTTON), host_or_join_menu, window)
    menu.mainloop(window)


def join_menu(window):
    menu = default_menu()
    host_input_button = menu.add_text_input(translate(HOST_INPUT))
    port_input_button = menu.add_text_input(translate(PORT_INPUT), input_type=pg_menu.locals.INPUT_INT)
    menu.add_button(translate(START_GAME_BUTTON), join_game, host_input_button, port_input_button, window)
    menu.add_button(translate(BACK_BUTTON), host_or_join_menu, window)
    menu.mainloop(window)


def host_game(port_input_button, window):
    host_online_pvp(port_input_button.get_value(), window)


def join_game(host_input_button, port_input_button, window):
    join_online_pvp(host_input_button.get_value(), port_input_button.get_value(), window)


def default_menu():
    return pg_menu.Menu(config.WINDOW_SIZE[1], config.WINDOW_SIZE[0], translate(JOIN_GAME_HEADER),
                        theme=pg_menu.themes.THEME_BLUE)


def main():
    pg.init()
    window = pg.display.set_mode(config.WINDOW_SIZE, pg.SRCALPHA)

    main_menu(window)
