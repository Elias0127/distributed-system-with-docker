# Distributed Communication Protocols with Docker

This project demonstrates the implementation of two fundamental communication protocols in a distributed system using Docker and Python: Unicast and Broadcast. The Unicast protocol enables one-to-one communication between nodes, while the Broadcast protocol allows a master server to send messages to multiple nodes simultaneously.

## Project Structure

The project is divided into two main parts, each representing a different communication protocol:

### UnicastProtocol

- **Server**: Manages client registrations and routes messages between nodes.
- **Nodes (node1, node2, node3, node4)**: Connect to the server, send registration messages, and exchange messages with other nodes.

### BroadcastProtocol

- **Master Server**: Broadcasts messages to all connected nodes.
- **Nodes (node1, node2, node3, node4)**: Listen for broadcast messages from the master server and process them upon receipt.

## Running the Project

The project is containerized using Docker, and each component runs in its own Docker container. To run the project, use the following commands:

### UnicastProtocol

1. Start the server:
   ```bash
   docker run --name server --network proj1-distributed-network -v "$(pwd)/logs:/app/logs" proj1-distributed-network:latest python -u /app/UnicastProtocol/server.py
   ```
2. Start the nodes:
   ```bash
   docker run --name node1 --network proj1-distributed-network -v "$(pwd)/logs:/app/logs" proj1-distributed-network:latest python -u /app/UnicastProtocol/node1.py
   docker run --name node2 --network proj1-distributed-network -v "$(pwd)/logs:/app/logs" proj1-distributed-network:latest python -u /app/UnicastProtocol/node2.py
   docker run --name node3 --network proj1-distributed-network -v "$(pwd)/logs:/app/logs" proj1-distributed-network:latest python -u /app/UnicastProtocol/node3.py
   docker run --name node4 --network proj1-distributed-network -v "$(pwd)/logs:/app/logs" proj1-distributed-network:latest python -u /app/UnicastProtocol/node4.py
   ```

### BroadcastProtocol

1. Start the master server:
   ```bash
   docker run --name server --network proj1-distributed-network -v "$(pwd)"/logs:/app/logs proj1-distributed-network:latest python -u /app/BroadcastProtocol/server.py
   docker run --name node1 --network proj1-distributed-network -v "$(pwd)"/logs:/app/logs proj1-distributed-network:latest python -u /app/BroadcastProtocol/node1.py
   docker run --name node2 --network proj1-distributed-network -v "$(pwd)"/logs:/app/logs proj1-distributed-network:latest python -u /app/BroadcastProtocol/node2.py
   docker run --name node3 --network proj1-distributed-network -v "$(pwd)"/logs:/app/logs proj1-distributed-network:latest python -u /app/BroadcastProtocol/node3.py
   docker run --name node4 --network proj1-distributed-network -v "$(pwd)"/logs:/app/logs proj1-distributed-network:latest python -u /app/BroadcastProtocol/node4.py
   ```
2. Broadcast a message from the master server:
   ```bash
   docker exec server python /app/BroadcastProtocol/broadcast_message.py
   ```
