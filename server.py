import os
from datetime import datetime
import threading
import socket
import sys
import csv
import time

# Dictionary to store the clients connected to the server. Key: node ID, Value: client socket
clients = {}
clients_lock = threading.Lock()


log_file_path = '/app/logs/communication_log.csv'

# Initialize file_exists at the top level, not inside the function
file_exists = os.path.isfile(log_file_path)

# If the file doesn't exist, we write the header when the script starts
if not file_exists:
    with open(log_file_path, mode='w', newline='') as log_file:
        log_writer = csv.writer(log_file, delimiter=',')
        headers = ["Type", "Time(s)", "Source_Ip", "Destination_Ip", "Source_Port",
                   "Destination_Port", "Protocol", "Length (bytes)", "Flags (hex)"]
        log_writer.writerow(headers)

def log_message(message_type, elapsed_time, source_ip, dest_ip, source_port, dest_port, protocol, length, flags):
    with open(log_file_path, mode='a', newline='') as log_file:
        log_writer = csv.writer(log_file, delimiter=',')
        log_writer.writerow([message_type, elapsed_time, source_ip,
                            dest_ip, source_port, dest_port, protocol, length, flags])



def handle_client(client_socket, addr, host):
    with clients_lock:
        node_id = f"node_{len(clients) + 1}"
        clients[node_id] = client_socket
    print(f"Registered {node_id} with address {addr}", flush=True)

    try:
        while True:
            start_time = time.time()
            message = client_socket.recv(1024).decode('utf-8')
            end_time = time.time()
            transmission_time = end_time - start_time
            if message:
                print(f"Message from {node_id} ({addr}): {message}")
                # Log the received message here
                log_message('Unicast', transmission_time, addr[0], host, addr[1], '12345', 'TCP', len(message), '0x010')
                if "Acknowledged" not in message:
                    response = f"Received: {message}"
                    send_message_to_node(node_id, response)
                    # Don't log the acknowledgment
            else:
                break
    except ConnectionResetError:
        print(f"Connection lost with {node_id}", flush=True)
    finally:
        with clients_lock:
            del clients[node_id]
        client_socket.close()
        print(f"Unregistered {node_id}", flush=True)


def send_message_to_node(node_id, message):
    with clients_lock:
        if node_id in clients:
            client_socket = clients[node_id]
            client_socket.send(message.encode('utf-8'))
        else:
            print(f"No client found with node ID {node_id}", flush=True)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname('server')
    print(f"The server IP address is: {host}", flush=True)
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}", flush=True)

    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket, addr, host))
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down server...", flush=True)
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
