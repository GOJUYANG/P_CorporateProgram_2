import threading

from socket import *

import pickle


class ClientSocket:
    def __init__(self):
        super().__init__()

    def clientsocket_Setting(self, ip_, port_):
        """클라이언트 소켓 연결"""
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip_, port_))
        self.buffer = 50000
        self.run()

    def client_Send_Function(self, msg: str = None):
        """
        클라이언트가 서버에게 msg + buffer 형태로 전달.
        :parameter
        msg = (클라이언트가 서버에게 보낼 내용) + buffer(공백값)
        """
        self.client_socket.send(f"{f'{msg}':{self.buffer}}".encode('utf-8'))  # msg + buffer형태로 서버에 send.

    def _client_Recv_Function(self):
        """서버에게 받은 recv값"""
        while True:
            msg = self.client_socket.recv(1024)
            print(msg)

    def thread_Function(self):
        """recv 기능 활성화를 위해 쓰레드 설정"""
        recv_thread = threading.Thread(target=self._client_Recv_Function)
        recv_thread.start()


    def run(self):
        """recv 쓰레드 스타트"""
        self.thread_Function()

    # def command_list(self):
    #     self.command_1 = 'DB'
    #     self.command_2 = 'ROOM'
    #     self.command_3 = 'NOMAL'
    #     self.command_4 = 'SYSTEM'
