import isolation
import socket

from isolation import connection_utils

JOIN_COMMAND = "/join"
HOST_COMMAND = "/host"

available_commands = [HOST_COMMAND, JOIN_COMMAND]


def get_help_str(commands):
    return " or ".join(commands) + "?"


if __name__ == "__main__":
    help_str = get_help_str(available_commands)
    command = ""
    while command not in available_commands:
        command = input("\n" + help_str + "\n").strip()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        ui = isolation.GUI()

        if command == HOST_COMMAND:
            port = int(input("Enter the desired port number: ").strip())

            connection_utils.start_server_on_port(server_socket, port)
            client_socket = connection_utils.blocking_wait_for_player(server_socket)

            player_a = isolation.LocalUserControlledPlayer(ui, isolation.TUI.ANN_ICON, client_socket)
            player_b = isolation.RemoteUserControlledPlayer(ui, isolation.TUI.BOB_ICON, client_socket)
        elif command == JOIN_COMMAND:
            host = input(connection_utils.HOST_PROMPT).strip()
            port = int(input(connection_utils.PORT_PROMPT).strip())

            server_socket.connect((host, int(port)))

            player_a = isolation.RemoteUserControlledPlayer(ui, isolation.TUI.ANN_ICON, server_socket)
            player_b = isolation.LocalUserControlledPlayer(ui, isolation.TUI.BOB_ICON, server_socket)

        isolation.run_game(ui, player_a, player_b)
