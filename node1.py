import datetime
import os
import socket
import sys
import csv
import time

# Unique identifier for this node
node_id = "node1"

log_file_path = '/app/logs/communication_log.csv'


def log_message(message_type, elapsed_time, source_ip, dest_ip, source_port, dest_port, protocol, length, flags):
    with open(log_file_path, mode='a', newline='') as log_file:
        log_writer = csv.writer(log_file, delimiter=',')
        log_writer.writerow([message_type, elapsed_time, source_ip,
                            dest_ip, source_port, dest_port, protocol, length, flags])


def connect_to_server(host, port):
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        node_socket.connect((host, port))
        print(f"{node_id} connected to server at {host}:{port}")
        sys.stdout.flush()
        return node_socket
    except socket.error as e:
        print(f"{node_id} error connecting to server: {e}")
        sys.stdout.flush()
        return None


def main():
    server_hostname = 'server'
    port = 12345

# Retrieve the IP address using the hostname
    try:
        server_ip = socket.gethostbyname(server_hostname)
        print(f"Resolved {server_hostname} to IP address: {server_ip}")
    except socket.error as e:
        print(f"Error resolving {server_hostname}: {e}")

    node_socket = connect_to_server(server_ip, port)

    if node_socket:
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            local_port = node_socket.getsockname()[1]

            # Send a greeting message to the server
            start_time = time.time()  # Start the timer
            greeting = f"{node_id}: Hello, server!"
            node_socket.send(greeting.encode('utf-8'))
            end_time = time.time()  # End the timer

            # Calculate the duration and log the message
            transmission_time = end_time - start_time
            log_message('Unicast', transmission_time, local_ip, host, local_port,
                        port, 'TCP', len(greeting), '0x010')

            while True:
                message = node_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"{node_id} received message from server: {message}")
                    sys.stdout.flush()
                    # Respond to the server's message but don't log this response
                    if "Acknowledged" not in message:
                        response = f"{node_id}: Acknowledged"
                        node_socket.send(response.encode('utf-8'))
                else:
                    break
        except Exception as e:
            print(f"{node_id} error during communication: {e}")
            sys.stdout.flush()
        finally:
            node_socket.close()
            print(f"{node_id} disconnected from server")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
