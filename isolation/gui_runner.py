"""
Module gui_runner implements functions to run
different types of the game in GUI mode
"""

import socket

import pygame as pg
import pygame_menu as pg_menu

from . import ai
from . import config
from .localization import Msg, _
from . import conn
from .game import run_game
from .ui import GUI

from .player import (
    UserControlledPlayer,
    LocalUserControlledPlayer,
    RemoteUserControlledPlayer,
    RobotControlledPlayer,
)


def run_local_gui(difficulty):
    """
    Starts game versus computer with the selected difficulty
    """
    ui = GUI()
    player_a = UserControlledPlayer(ui, ui.ANN_ICON)
    player_b = RobotControlledPlayer(ui, difficulty)
    run_game(ui, player_a, player_b)


def run_local_pvp():
    """
    Starts local game for two controlled players
    """
    ui = GUI()
    player_a = UserControlledPlayer(ui, ui.ANN_ICON)
    player_b = UserControlledPlayer(ui, ui.BOB_ICON)
    run_game(ui, player_a, player_b)


def host_online_pvp(port, window=None):
    """
    Starts game server on the given port and waits for another player to connect
    :param port: a port to run the game on
    :param window: current pygame window if it is present
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        conn.start_server_on_port(server_socket, int(port))
        client_socket = conn.blocking_wait_for_player(server_socket)

        ui = GUI(window)
        player_a = LocalUserControlledPlayer(ui, ui.ANN_ICON, client_socket)
        player_b = RemoteUserControlledPlayer(ui, ui.BOB_ICON, client_socket)

        run_game(ui, player_a, player_b)


def join_online_pvp(host, port, window=None):
    """
    Connects to the specified host and port to join the game assuming that game server has been started there
    :param host: host to connect to
    :param port: host's port to connect to
    :param window: current pygame window if it is present
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((host, int(port)))

        ui = GUI(window)
        player_a = RemoteUserControlledPlayer(ui, ui.ANN_ICON, server_socket)
        player_b = LocalUserControlledPlayer(ui, ui.BOB_ICON, server_socket)

        run_game(ui, player_a, player_b)


def main_menu(window):
    """
    Displays main menu with game mode choice
    """
    menu = default_menu(_(Msg.WELCOME_HEADER))
    menu.add_button(_(Msg.PVE_BUTTON), difficulty_menu, window)
    menu.add_button(_(Msg.PVP_BUTTON), local_or_remote_pvp_menu, window)
    menu.add_button(_(Msg.QUIT_BUTTON), pg_menu.events.EXIT)
    menu.mainloop(window)


def difficulty_menu(window):
    """
    Displays difficulty choice menu if 'Player vs Computer' mode has been chosen
    """
    menu = default_menu(_(Msg.CHOOSE_DIFFICULTY_HEADER))
    menu.add_button(_(Msg.EASY_BUTTON), run_local_gui, ai.Difficulty.easy)
    menu.add_button(_(Msg.NORMAL_BUTTON), run_local_gui, ai.Difficulty.normal)
    menu.add_button(_(Msg.HARD_BUTTON), run_local_gui, ai.Difficulty.hard)
    menu.add_button(_(Msg.BACK_BUTTON), main_menu, window)
    menu.mainloop(window)


def local_or_remote_pvp_menu(window):
    """
    Displays the menu for choosing which kind of 'Player vs Player' mode should be used
    """
    menu = default_menu(_(Msg.CHOOSE_PVP_TYPE_HEADER))
    menu.add_button(_(Msg.THIS_COMPUTER_BUTTON), run_local_pvp)
    menu.add_button(_(Msg.TWO_COMPUTERS_BUTTON), host_or_join_menu, window)
    menu.add_button(_(Msg.BACK_BUTTON), main_menu, window)
    menu.mainloop(window)


def host_or_join_menu(window):
    """
    Displays 'host or join' choice menu if online game has been chosen
    """
    menu = default_menu(_(Msg.CHOOSE_ROLE_HEADER))
    menu.add_button(_(Msg.HOST_BUTTON), host_menu, window)
    menu.add_button(_(Msg.JOIN_BUTTON), join_menu, window)
    menu.add_button(_(Msg.BACK_BUTTON), local_or_remote_pvp_menu, window)
    menu.mainloop(window)


def host_menu(window):
    """
    Displays host settings menu
    """
    menu = default_menu(_(Msg.CREATE_GAME_HEADER))
    port_input_button = menu.add_text_input(_(Msg.PORT_INPUT), input_type=pg_menu.locals.INPUT_INT)
    menu.add_button(_(Msg.CREATE_AND_WAIT), host_game, port_input_button, window)
    menu.add_button(_(Msg.BACK_BUTTON), host_or_join_menu, window)
    menu.mainloop(window)


def join_menu(window):
    """
    Displays the menu for entering host information to connect to it
    """
    menu = default_menu(_(Msg.JOIN_GAME_HEADER))
    host_input_button = menu.add_text_input(_(Msg.HOST_INPUT))
    port_input_button = menu.add_text_input(_(Msg.PORT_INPUT), input_type=pg_menu.locals.INPUT_INT)
    menu.add_button(_(Msg.CONNECT_BUTTON), join_game, host_input_button, port_input_button, window)
    menu.add_button(_(Msg.BACK_BUTTON), host_or_join_menu, window)
    menu.mainloop(window)


def host_game(port_input_button, window):
    """
    Callback for getting specified host settings and running it
    :param port_input_button: menu input field containing port value
    :param window: pygame menu window
    """
    host_online_pvp(port_input_button.get_value(), window)


def join_game(host_input_button, port_input_button, window):
    """
    Callback for getting specified host information and connecting to it
    :param host_input_button: menu input field containing host name
    :param port_input_button: menu input field containing port value
    :param window: pygame menu window
    """
    join_online_pvp(host_input_button.get_value(), port_input_button.get_value(), window)


def default_menu(header):
    """
    Initializes default menu with the predefined configuration and style
    :param header: menu's name to be showed to the user
    :return: the created default menu
    """
    return pg_menu.Menu(
        config.WINDOW_SIZE[1],
        config.WINDOW_SIZE[0],
        header,
        theme=pg_menu.themes.THEME_BLUE,
    )


def main():
    pg.init()
    window = pg.display.set_mode(config.WINDOW_SIZE, pg.SRCALPHA)

    try:
        main_menu(window)
    except Exception:
        pass
