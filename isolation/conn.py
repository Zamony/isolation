"""
Module conn implements utility functions
to run game over the network
"""

import socket
import re

ONE_DIGIT_COORDS_LEN = len("(x, y)")

def receive_one_digit_coords(read_socket):
    msg = b''
    while len(msg) < ONE_DIGIT_COORDS_LEN:
        msg += read_socket.recv(ONE_DIGIT_COORDS_LEN - len(msg))

    m = re.match(r"\(([0-6]), ([0-6])\)", msg.decode())
    if not m:
        raise ValueError("invalid coordinates format")

    return int(m.group(1)), int(m.group(2))


def send_coords(write_socket, coords):
    return write_socket.sendall(str.encode(str(coords)))


def start_server_on_port(server_socket, port, num_connections=1):
    server_socket.bind((socket.gethostname(), port))
    server_socket.listen(num_connections)


def blocking_wait_for_player(server_socket):
    client_socket, _ = server_socket.accept()
    return client_socket
