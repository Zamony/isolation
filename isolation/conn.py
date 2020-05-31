"""
Module conn implements utility functions
to run game over the network
"""

import socket
import re

ONE_DIGIT_COORDS_LEN = len("(x, y)")


def receive_one_digit_coords(read_socket):
    """
    Tries to read coordinates from socket consisting of one digit each.
    The expected coordinates format is '(1, 2)'.

    :param read_socket: socket to read coordinates from
    :raises ValueError: in case of invalid coordinates passed through the socket
    :return: tuple of two values corresponding to the coordinates
    """
    msg = b''
    while len(msg) < ONE_DIGIT_COORDS_LEN:
        msg += read_socket.recv(ONE_DIGIT_COORDS_LEN - len(msg))

    m = re.match(r"\(([0-6]), ([0-6])\)", msg.decode())
    if not m:
        raise ValueError("invalid coordinates format")

    return int(m.group(1)), int(m.group(2))


def send_coords(write_socket, coords):
    """
    Converts passed coordinates to byte representation and sends via socket.

    :param write_socket: socket to write given coordinates to
    :param coords: tuple of two numbers
    :return: None
    """
    return write_socket.sendall(str.encode(str(coords)))


def start_server_on_port(server_socket, port, num_connections=1):
    """
    Binds given socket to the current hostname and given port
    and enables it to accept connections.

    :param server_socket: socket to start server on
    :param port: port to start server on
    :param num_connections: max number of accepted connections
    :return: None
    """
    server_socket.bind((socket.gethostname(), port))
    server_socket.listen(num_connections)


def blocking_wait_for_player(server_socket):
    """
    Enters blocking waiting for client's connection to the given socket.
    :param server_socket: socket to which client should connect
    :return: socket of the connected client
    """

    client_socket, _ = server_socket.accept()
    return client_socket
