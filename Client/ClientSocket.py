"""클라이언트 소켓 파일"""
import threading
import pickle


from PyQt5.QtCore import QObject, pyqtSignal
from socket import *

class ClientSocket(QObject):
    db_signal = pyqtSignal(list)
    chat_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def clientsocket_Set(self):
        """클라이언트 소켓 연결"""
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 7001))
        self.run()

    def client_Send_Func(self, header, msg):
        """
        :param header: 데이터의 타입을 설정
        :param msg: 서버에게 보낼 내용
        :return:
        """
        data = f'{header}:{msg}'
        self.client_socket.send(data.encode('utf-8'))  # msg + buffer형태로 서버에 send.

    def _recv_from_server(self):
        """서버에게 받은 recv값"""
        while True:
            msg_type = self.client_socket.recv(1024)
            try:
                msg = pickle.loads(msg_type)
                print(type(msg))
                self.db_signal.emit(msg)
            except:
                msg = msg_type.decode('utf-8')
                print(msg)
                self.chat_signal.emit(msg)

    def thread_Func(self):
        """recv 기능 활성화를 위해 쓰레드 설정"""
        recv_thread = threading.Thread(target=self._recv_from_server)
        recv_thread.start()

    def run(self):
        """recv 쓰레드 스타트"""
        self.thread_Func()


