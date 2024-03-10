FROM python:3.8
COPY server.py /app/server.py
COPY node1.py /app/node1.py
COPY node2.py /app/node2.py
COPY node3.py /app/node3.py
COPY node4.py /app/node4.py

WORKDIR /app
RUN mkdir -p /app/logs && chmod 777 /app/logs
CMD ["python", "-u", "server.py"]
