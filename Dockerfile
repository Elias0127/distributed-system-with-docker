FROM python:3.8

# Install ping and telnet
RUN apt-get update && apt-get install -y \
    iputils-ping \
    telnet

# Copy Unicast protocol files and logs
COPY UnicastProtocol /app/UnicastProtocol

# Copy Broadcast protocol files
COPY BroadcastProtocol /app/BroadcastProtocol


WORKDIR /app/UnicastProtocol
RUN chmod 777 logs
CMD ["python", "-u", "server.py"]
