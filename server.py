import os
from datetime import datetime
import threading
import socket
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


def handle_client(client_socket, addr, host, port):
    node_id = None
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message.startswith("register:"):
                    node_id = message.split(":")[1]
                    with clients_lock:
                        clients[node_id] = (client_socket, addr)
                    print(
                        f"Registered {node_id} with address {addr}", flush=True)
                elif node_id:
                    sender_id, recipient_id, content = parse_message(message)
                    # Log message received from sender
                    log_message("Received", time.time(
                    ), addr[0], host, addr[1], port, 'TCP', len(message), '0x010')
                    # Route the message to the recipient
                    route_message(sender_id, recipient_id, content)
            else:
                break
    except ConnectionResetError:
        print(f"Connection lost with {node_id}", flush=True)
    finally:
        with clients_lock:
            if node_id in clients:
                del clients[node_id]
        client_socket.close()
        print(f"Unregistered {node_id}", flush=True)




def parse_message(message):
    # Assumes the message format is "sender_id:recipient_id:content"
    parts = message.split(':', 2)
    return parts[0], parts[1], parts[2]


def route_message(sender_id, recipient_id, content):
    with clients_lock:
        recipient_info = clients.get(recipient_id)
        if recipient_info:
            recipient_socket, recipient_addr = recipient_info
            try:
                full_message = f"{sender_id}:{content}"
                recipient_socket.send(full_message.encode('utf-8'))

                # Log message sent to recipient
                if recipient_addr:  # Ensure we have the address for logging
                    log_message("Sent", time.time(
                    ), recipient_addr[0], recipient_addr[0], recipient_addr[1], recipient_addr[1], 'TCP', len(full_message), '0x010')
            except socket.error as e:
                print(
                    f"Error sending message to {recipient_id}: {e}", flush=True)
        else:
            print(f"No client found with node ID {recipient_id}", flush=True)


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
                target=handle_client, args=(client_socket, addr, host, port))  
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down server...", flush=True)
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
