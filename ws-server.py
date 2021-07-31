import os
import sys
import time
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import queue
import threading

class WSServerInstance(WebSocket):
    def handleMessage(self):
        # 这里的server就是绑定的WSServer里的server
        self.server.data_queue.put(self.data)

    def handleConnected(self):
        print(self.address, "connected")

    def handleClose(self):
        print(self.address, "closed")

class WSServer(object):
    def __init__(self, port):
        self.server = SimpleWebSocketServer('', port, WSServerInstance)
        self.server.data_queue = queue.Queue(1000)
        self.server_thread = None
        self.run()

    def run(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def run_server(self):
        self.server.serveforever()

    def broadcast_message(self, message):
        """
            Sent all client message
        """
        for key, client in self.server.connections.items():
            client.sendMessage(message)

    def main_proccess(self):
        """
           loop add stream code
        """
        while True:
            if (not self.server.data_queue.empty()):
                message = self.server.data_queue.get()
                print("on get message:", message)
                self.broadcast_message(message)
            # other proccess

ws_server = WSServer(9000)
ws_server.main_proccess()
