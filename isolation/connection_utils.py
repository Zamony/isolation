import socket

ONE_DIGIT_COORDS_LEN = len("(x, y)")

HOST_PROMPT = "Host: "
PORT_PROMPT = "Port: "


def receive_one_digit_coords(read_socket):
    return eval(read_socket.recv(ONE_DIGIT_COORDS_LEN).decode())


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
