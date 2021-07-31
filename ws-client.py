import time
from websocket import create_connection
ws = create_connection("ws://172.16.0.155")
for i in range(0,5000):
    print("Sending 'Hello, World'...")
    ws.send("Hello, World")
    print("Sent")
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)
ws.close()
