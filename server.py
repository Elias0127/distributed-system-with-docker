import threading
import socket
import sys

# Dictionary to store the clients connected to the server. Key: node ID , Value: client socket
clients = {}


def handle_client(client_socket, addr):
    # Register the client
    # Assign a node ID based on the current number of clients
    node_id = f"node_{len(clients) + 1}"
    clients[node_id] = client_socket
    print(f"Registered {node_id} with address {addr}")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Message from {node_id} ({addr}): {message}")
                sys.stdout.flush()

                # Only send a response if the message is not an acknowledgment
                if "Acknowledged" not in message:
                    response = f"Received: {message}"
                    send_message_to_node(node_id, response)
            else:
                break
        except:
            break

    # Cleanup on disconnect
    client_socket.close()
    del clients[node_id]
    print(f"Unregistered {node_id}")
    sys.stdout.flush()



def send_message_to_node(node_id, message):
    if node_id in clients:
        client_socket = clients[node_id]
        client_socket.send(message.encode('utf-8'))
    else:
        print(f"No client found with node ID {node_id}")
        sys.stdout.flush()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"

port = 12345
server_socket.bind((host, port))
server_socket.listen(5)
print(f"Server is listening on {host}:{port}")
sys.stdout.flush()

while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(
        target=handle_client, args=(client_socket, addr))
    client_thread.start()
