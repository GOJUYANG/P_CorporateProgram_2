#서버 코드
import threading, socket
import time
import pickle


class Room: #채팅방
    """클라이언트들에게 메시지를 전부 보내기위한 기능"""
    def __init__(self):
        self.clients = []  # 접속된 클라이언트들을 담을 리스트

    def addClient(self, cos):
        """클라이언트가 접속시 리스트에 추가하기 위한 기능"""
        self.clients.append(cos)

    def deleteClient(self, cos):
        self.clients.remove(cos)

    def sendAllClients(self, msg):
        """클라이언트 전부에게 메세지 전달 기능"""
        for cos in self.clients:
            cos.sendMsg(msg)

class ChatClient:
    """클라이언트 send값을 recv하는 클래스"""
    def __init__(self, num, soc, room):
        self.client_socket = soc
        self.room = room
        self.num = num

    def recvMsg(self):
        """클라이언트들의 메시지를 받는 기능"""
        while True:
            data_and_buffer = self.client_socket.recv(1024)  # msg + buffer형태
            data = data_and_buffer.strip()  # buffer을 제거
            if data == 'stop':
                print(self.num, "번 클라이언트 접속해제")
                break
        self.room.deleteClient(self)

    def sendMsg(self, msg):
        """해당 클라이언트에게 메시지 전달하기 위한 기능"""
        if type(msg) == bytes:
            msg = msg

        self.client_socket.sendall(msg.encode('utf-8'))

    def run(self):
        """recv를 쓰레드 및 스타트 하는 기능"""
        recvtread = threading.Thread(target=self.recvMsg)
        recvtread.start()

class ServerMain:
    """메인 서버 클래스"""
    def __init__(self, host_, port_):
        self.server_soc = None
        self.room = Room()
        self.address = (host_, port_)

    def open(self):
        """서버 소켓의 설정"""
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.bind(self.address)
        self.server_soc.listen()

    def run(self):
        """서버 소켓 오픈 및 연결 기능"""
        self.open()
        print('서버시작')
        while True:
            connect_socket, addr = self.server_soc.accept()
            print(addr, '접속완료')
            user_num = (len(self.clients)+1)
            clientconnect = ChatClient(user_num, connect_socket, self.room)
            self.room.addClient(clientconnect)
            clientconnect.run()
            time.sleep(0.1)

def main():
    """메인 클래스를 꺼지지않게 쓰레드 설정 및 시작"""
    server = ServerMain('', 7001)
    threading.Thread(target=server.run).start()


mainapp = main()