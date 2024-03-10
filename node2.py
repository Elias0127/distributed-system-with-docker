import socket
import sys
import csv
import time

# Unique identifier for this node
node_id = "node2"


def log_message(message_type, source_ip, dest_ip, source_port, dest_port, protocol, length, flags):
    with open('/app/logs/communication_log.csv', mode='a', newline='') as log_file:
        log_writer = csv.writer(log_file, delimiter=',')
        log_writer.writerow([message_type, time.time(
        ), source_ip, dest_ip, source_port, dest_port, protocol, length, flags])


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
    host = socket.gethostbyname('server')  # Use the container name of the server
    port = 12345
    node_socket = connect_to_server(host, port)
    if node_socket:
        try:
            # Send a greeting message to the server
            greeting = f"{node_id}: Hello, server!"
            node_socket.send(greeting.encode('utf-8'))
            log_message('Unicast', 'node_ip', host, 'node_port',
                        port, 'TCP', len(greeting), '0x010')

            while True:
                message = node_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"{node_id} received message from server: {message}")
                    sys.stdout.flush()
                    # Only send a response if the message is not an acknowledgment
                    if "Acknowledged" not in message:
                        response = f"{node_id}: Acknowledged"
                        node_socket.send(response.encode('utf-8'))
                        log_message('Unicast', host, 'node_ip', port,
                                    'node_port', 'TCP', len(response), '0x010')
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
