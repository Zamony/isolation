import socket
import re

ONE_DIGIT_COORDS_PATTERN = r"\([0-6], [0-6]\)"
ONE_DIGIT_COORDS_LEN = len("(x, y)")

HOST_PROMPT = "Host: "
PORT_PROMPT = "Port: "


def receive_one_digit_coords(read_socket):
    received = read_socket.recv(ONE_DIGIT_COORDS_LEN).decode()
    if not __validate_coordinates(received):
        raise ValueError("The received string '%s' can't be parsed as coordinates" % received)
    return eval(received)


def send_coords(write_socket, coords):
    return write_socket.sendall(str.encode(str(coords)))


def start_server_on_port(server_socket, port, num_connections=1):
    server_socket.bind((socket.gethostname(), port))
    server_socket.listen(num_connections)

    print(HOST_PROMPT + socket.gethostname())
    print(PORT_PROMPT + str(port))


def blocking_wait_for_player(server_socket):
    print("Waiting for the second player to join the game...")
    client_socket, address = server_socket.accept()
    print("Player 2 has joined: ", address)
    return client_socket


def __validate_coordinates(coords_str):
    return True if re.match(ONE_DIGIT_COORDS_PATTERN, coords_str) else False
