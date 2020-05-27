import argparse
import socket

from . import ai
from . import connection_utils
from .localization import translate
from .game import run_game
from .ui import (
    GUI,
    TUI,
)
from .player import (
    UserControlledPlayer,
    LocalUserControlledPlayer,
    RemoteUserControlledPlayer,
    RobotControlledPlayer,
)

JOIN_COMMAND = "/join"
HOST_COMMAND = "/host"

available_commands = [HOST_COMMAND, JOIN_COMMAND]

def get_help_str(commands):
    return translate(" or ").join(commands) + "?"

def run_online_pvp(*args):
    help_str = get_help_str(available_commands)
    command = ""
    while command not in available_commands:
        command = input("\n" + help_str + "\n").strip()

    if command == HOST_COMMAND:
        port = int(input(translate("Enter the desired port number: ")).strip())

        host_online_pvp(port)
    elif command == JOIN_COMMAND:
        host = input(connection_utils.HOST_PROMPT).strip()
        port = int(input(connection_utils.PORT_PROMPT).strip())

        join_online_pvp(host, port)


def host_online_pvp(port, window=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        connection_utils.start_server_on_port(server_socket, int(port))
        client_socket = connection_utils.blocking_wait_for_player(server_socket)

        ui = GUI(window)
        player_a = LocalUserControlledPlayer(ui, ui.ANN_ICON, client_socket)
        player_b = RemoteUserControlledPlayer(ui, ui.BOB_ICON, client_socket)

        run_game(ui, player_a, player_b)


def join_online_pvp(host, port, window=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((host, int(port)))

        ui = GUI(window)
        player_a = RemoteUserControlledPlayer(ui, ui.ANN_ICON, server_socket)
        player_b = LocalUserControlledPlayer(ui, ui.BOB_ICON, server_socket)

        run_game(ui, player_a, player_b)


def run_local_pvp(*args):
    ui = GUI()
    player_a = UserControlledPlayer(ui, ui.ANN_ICON)
    player_b = UserControlledPlayer(ui, ui.BOB_ICON)
    run_game(ui, player_a, player_b)


def run_local_gui(difficulty):
    run_local(GUI(), difficulty)

def run_local_tui(difficulty):
    run_local(TUI(), difficulty)

def run_local(ui, difficulty):
    player_a = UserControlledPlayer(ui, ui.ANN_ICON)
    player_b = RobotControlledPlayer(ui, difficulty)
    run_game(ui, player_a, player_b)


def main():
    commands = {
        "local-gui": run_local_gui,
        "local-tui": run_local_tui,
        "pvp-local": run_local_pvp,
        "pvp-online": run_online_pvp,
    }

    difficulty = {
        "hard": ai.Difficulty.hard,
        "normal": ai.Difficulty.normal,
        "easy": ai.Difficulty.easy,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="local-gui", choices=list(commands))
    parser.add_argument("--difficulty", default="normal", choices=list(difficulty))
    args = parser.parse_args()
    commands[args.mode](difficulty[args.difficulty])

if __name__ == "__main__":
    main()
