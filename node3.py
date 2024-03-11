import socket
import sys
import time
import csv

node_id = "node3"


def log_message(message_type, source_ip, dest_ip, source_port, dest_port, protocol, length, flags):
    # Log format may need to be updated based on the specific format you're looking for
    with open('/app/logs/communication_log.csv', mode='a', newline='') as log_file:
        log_writer = csv.writer(log_file, delimiter=',')
        log_writer.writerow([message_type, time.time(
        ), source_ip, dest_ip, source_port, dest_port, protocol, length, flags])


def connect_to_server(host, port):
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        node_socket.connect((host, port))
        print(f"{node_id} connected to server at {host}:{port}")
        return node_socket
    except socket.error as e:
        print(f"{node_id} error connecting to server: {e}", file=sys.stderr)
        return None


def send_message_to(node_socket, recipient_id, message):
    full_message = f"{node_id}:{recipient_id}:{message}"
    node_socket.send(full_message.encode('utf-8'))


def main():
    server_hostname = 'server'
    port = 12345

    server_ip = socket.gethostbyname(server_hostname)
    node_socket = connect_to_server(server_ip, port)

    if node_socket:
        try:
            # Example sending a message to node2 from this node
            send_message_to(node_socket, "node2", "Hello from nodeX!")

            while True:
                response = node_socket.recv(1024).decode('utf-8')
                if response:
                    print(f"{node_id} received message: {response}")
                else:
                    break
        except Exception as e:
            print(f"{node_id} error during communication: {e}", file=sys.stderr)
        finally:
            node_socket.close()
            print(f"{node_id} disconnected from server")


if __name__ == "__main__":
    main()
