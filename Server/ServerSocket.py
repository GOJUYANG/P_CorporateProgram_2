#서버 코드
import threading, socket
import time
import pickle

from Server.DataRead import DataClass


# from Server.SERVER import ServerScreen

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

    def recv_from_client(self):
        """클라이언트들의 메시지를 받는 기능"""
        while True:
            data_all = self.client_socket.recv(1024)  # msg + buffer형태
            data_s = data_all.decode('utf-8')
            data_list = data_s.split(':')
            print(data_list, "ServerSocket파일에서 받은 데이터 리스트입니다.")

            command = data_list[0]
            print(command, 'ServerSocket파일에서 받은 명령어 입니다.')

            msg_list = data_list[-1].split('/')
            print(msg_list, "ServerSocket파일에서 받은 메시지 리스트 입니다.")

            if command == 'Server':
                if msg_list[0] == 'Socket':
                    if msg_list[1] == 'Stop':
                        print(self.num, "번 클라이언트 접속해제")
                        break
                elif msg_list[0] == 'DB':
                    if msg_list[1] == 'Login':
                        DBdata = DataClass()
                        user_query = DBdata.select_user_info('*', msg_list[2])
                        print(user_query, "유저의 이메일을 조회한 DB 데이터 입니다.")
                        list_to_db = user_query.tolist()
                        print(list_to_db, "DB데이터를 tolist화 한것입니다.")
                        if len(list_to_db) > 0:
                            user_info = pickle.dumps(list_to_db[0])
                            print(user_info, "pickle.dump를 통해 list를 바이트화 한것입니다.")
                            self.send_to_client(user_info)
                        else:
                            user_info = pickle.dumps(["not find"])
                            self.send_to_client(user_info)
                    elif msg_list[1] == 'Pw_Change':
                        print(msg_list[2], msg_list[3])
            elif command == 'Team':
                if msg_list[0] == 'Chat':
                    print("Team파트에서 받은 챗입니다.")
                    msg = data_all
                    self.room.sendAllClients(msg)
        self.room.deleteClient(self)

    def send_to_client(self, msg):
        """해당 클라이언트에게 메시지 전달하기 위한 기능"""
        print(msg, "SerVerSocket파일에서 보낼 메시지입니다.")
        self.client_socket.sendall(msg)

    def run(self):
        """recv를 쓰레드 및 스타트 하는 기능"""
        recvtread = threading.Thread(target=self.recv_from_client)
        recvtread.start()

class ServerMain:
    """메인 서버 클래스"""

    def __init__(self, host_, port_):
        self.server_soc = None
        self.room = Room()
        self.address = (host_, port_)
        # self.server_screen = ServerScreen()
        # self.server_screen.show()

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
            user_num = (len(self.room.clients) + 1)
            clientconnect = ChatClient(user_num, connect_socket, self.room)
            self.room.addClient(clientconnect)
            clientconnect.run()
            time.sleep(0.1)

def main():
    """메인 클래스를 꺼지지않게 쓰레드 설정 및 시작"""
    server = ServerMain('', 7001)
    threading.Thread(target=server.run).start()


mainapp = main()