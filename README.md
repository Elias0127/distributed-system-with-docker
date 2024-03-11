# distributed-system-with-docker
# by Abrham Tamiru 029802004
# Brodcast communication between a server and 4 nodes
we create a master server and 4 nodes using python socket module.
This design allows for the broadcast of messages from the server to all connected nodes, creating a decentralized communication network
# server implementation 
The server is responsible for listening to incoming messages and broadcasting them to all connected nodes. we created broadcast server that sends a message to all nodes in the network
It uses a UDP socket for communication and binds to the address '0.0.0.0' on port 12345. The server continuously listens for messages and broadcasts them to all nodes using the broadcast address 
  Creates a UDP (User Datagram Protocol) socket.
  Binds the server socket to listen on all available network interfaces ('0.0.0.0') on port 12345.
  Prints a message indicating that the broadcast server is listening.
  Receives a message and the address of the sender. The maximum message size is set to 1024 bytes.
  Broadcasts the received message to all clients by sending it to the broadcast address on port 12345.
  using a loop to Ensures that the server continues to run indefinitely, continuously listening for and broadcasting messages.
# node implementation 
Nodes are individual entities that listen for broadcast messages from the server. Each node uses a UDP socket, sets the SO_BROADCAST socket option, and binds to the same address and port as the server. The nodes continuously listen for broadcast messages and print the received messages along with the node identifier.
our design assigns a unique identifier to each node based on their position in the network (e.g., "Node1", "Node2")
# conclution 
The broadcast communication mechanism that has been devised makes it possible for numerous nodes to communicate effectively with a central server. When a network of linked devices needs to receive real-time updates or notifications, this can be helpful. The system is readily expandable and offers a basis for future security, error-recovery, and identifying mechanism improvements.

# by Elias woldie 
# unicast communication between a server and 4 nodes
The unicast communication design involves a central server and multiple nodes that can connect to the server to send and receive messages.
we create a master server and 4 nodes using python socket module.
# server implementation 
the server serves as the central hub for communication. It performs 
  Binds to a specific IP address and port (12345) using a TCP socket.
  Listens for incoming connections from nodes using server_socket.accept().
  Handles each connected node in a separate thread using the handle_client function.
  Allows nodes to register with a unique identifier by sending a registration message in the format "register:node_id".
  Routes messages between nodes based on the sender and recipient IDs.
  Logs communication events (received and sent messages) to a CSV file.
# node implementation 
Each node represents a node in the network. 
Nodes perform 
  Connect to the server using a TCP socket.
  Send a registration message to the server upon successful connection.
  Exchange messages with other nodes through the server.
  Display received messages.
# conclution 
For nodes to register with a central server and exchange messages, a basis for unicast communication is provided by the system design. It illustrates the fundamentals of networked unicast communication and can be improved further for certain use cases. For the aim of debugging and optimization, the logging mechanism allows for the monitoring and analysis of communication events.

# by Besufekad Tessema ID:028628390
# Monitor the communication
for broadcast and unicast 
  The communication log is stored in a CSV file
  The log captures various details about each communication, including type, timestamps, IP addresses, ports, protocol, message length, and flags.
we introduce login function 
  log_message: Logs communication details to the CSV file.
  parse_message: Parses the incoming messages to extract sender, recipient, and content information.
When a node registers with the server, it is logged as a "Received" message with the sender's and server's details.
Any communication between registered nodes is logged as "Received" and "Sent" messages, including sender and recipient details.
communication log includes
Type either recieve or send
time, souce and destination id, source and destination port, protocol, length(byte) and flag(hex)
# connclution
The network analysis is built into the script and automatically records all communication events. This information can be further analyzed using various network analysis tools or custom scripts to generate insights into network behavior.
