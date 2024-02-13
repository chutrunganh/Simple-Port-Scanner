import socket
import threading

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)

    print(f"Server listening on port {port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        client_socket.send(b"Welcome to the server!")
        client_socket.close()

if __name__ == "__main__":
    ports = [21, 22, 23, 25, 53, 80, 110,]  # Add more ports as needed

    threads = []

    for port in ports:
        thread = threading.Thread(target=start_server, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
