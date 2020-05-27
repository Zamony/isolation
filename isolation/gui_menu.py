import pygame as pg
import pygame_menu as pg_menu

from . import ai
from . import config
from .cli import run_local_gui, run_local_pvp, host_online_pvp, join_online_pvp


def main_menu(window):
    menu = pg_menu.Menu(config.WINDOW_SIZE[1], config.WINDOW_SIZE[0], "Welcome to Isolation!",
                        theme=pg_menu.themes.THEME_BLUE)

    menu.add_button("Play with computer", difficulty_menu, window)
    menu.add_button("Play with a friend", local_or_remote_pvp_menu, window)
    menu.add_button("Quit", pg_menu.events.EXIT)
    menu.mainloop(window)


def difficulty_menu(window):
    menu = pg_menu.Menu(config.WINDOW_SIZE[1], config.WINDOW_SIZE[0], "Choose difficulty",
                        theme=pg_menu.themes.THEME_BLUE)
    menu.add_button("Easy", run_local_gui, ai.Difficulty.easy)
    menu.add_button("Normal", run_local_gui, ai.Difficulty.normal)
    menu.add_button("Hard", run_local_gui, ai.Difficulty.hard)
    menu.add_button("< Back", main_menu, window)
    menu.mainloop(window)


def local_or_remote_pvp_menu(window):
    menu = pg_menu.Menu(config.WINDOW_SIZE[1], config.WINDOW_SIZE[0], "Choose PVP type",
                        theme=pg_menu.themes.THEME_BLUE)

    menu.add_button("This computer", run_local_pvp)
    menu.add_button("Two computers", host_or_join_menu, window)
    menu.add_button("< Back", main_menu, window)
    menu.mainloop(window)


def host_or_join_menu(window):
    menu = pg_menu.Menu(config.WINDOW_SIZE[1], config.WINDOW_SIZE[0], "Choose role",
                        theme=pg_menu.themes.THEME_BLUE)

    menu.add_button("Host", host_menu, window)
    menu.add_button("Join", join_menu, window)
    menu.add_button("< Back", local_or_remote_pvp_menu, window)
    menu.mainloop(window)


def host_menu(window):
    menu = pg_menu.Menu(config.WINDOW_SIZE[1], config.WINDOW_SIZE[0], "Choose port",
                        theme=pg_menu.themes.THEME_BLUE)

    port_input_button = menu.add_text_input("Port:  ", input_type=pg_menu.locals.INPUT_INT)
    menu.add_button("Start game", host_game, port_input_button)
    menu.add_button("< Back", host_or_join_menu, window)
    menu.mainloop(window)


def join_menu(window):
    menu = pg_menu.Menu(config.WINDOW_SIZE[1], config.WINDOW_SIZE[0], "Join a game",
                        theme=pg_menu.themes.THEME_BLUE)

    host_input_button = menu.add_text_input("Host:  ")
    port_input_button = menu.add_text_input("Port:  ", input_type=pg_menu.locals.INPUT_INT)
    menu.add_button("Start game", join_game, host_input_button, port_input_button)
    menu.add_button("< Back", host_or_join_menu, window)
    menu.mainloop(window)


def host_game(port_input_button):
    host_online_pvp(port_input_button.get_value())


def join_game(host_input_button, port_input_button):
    join_online_pvp(host_input_button.get_value(), port_input_button.get_value())


def main():
    pg.init()
    window = pg.display.set_mode(config.WINDOW_SIZE, pg.SRCALPHA)

    main_menu(window)
