#서버 코드
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *

import threading, socket
import time
import pickle

from Server.DataRead import DataClass
from Views.DialongWarning import DialogWarning

class Room: #채팅방s
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

class ServerScreen(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../UI/ui_server.ui', self)

        self.checkBoxList_1 = []
        self.checkBoxList_2 = []
        self.checked_list_1 = []
        self.crew_list = []
        self.team_list = []
        self.captain = ""

        # --- DB연결
        self.db = DataClass()
        self.dlg = DialogWarning()
        self.server = ServerMain()

        # --- 관리자화면
        self.server_btn.clicked.connect(self.server_start)
        self.btn_add.clicked.connect(self.insert_table_widget)
        self.btn_crew.clicked.connect(self.insert_crew)
        self.btn_captain.clicked.connect(self.insert_captain)
        self.btn_team.clicked.connect(self.return_team)
        self.btn_clear.clicked.connect(self.ldt_clear)

    def server_start(self, addr, state):
        if state:
            if self.server.run():
                self.server_btn.setText('서버 종료')
        else:
            self.s.stop()
            self.msg.clear()
            self.server_btn.setText('서버 실행')

    def insert_table_widget(self):
        """관리자 view 내 테이블 위젯 명단 업로드"""
        list_name = self.db.select_user_info('user_nm')
        print(list_name)
        for i, name in enumerate(list_name):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.QTablewidget.setItem(i, 0, QTableWidgetItem(f"{name[0].strip('')}"))
            self.QTablewidget.item(i, 0).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

            ckbox = QCheckBox()
            ckbox.setCheckState(Qt.Unchecked)
            self.checkBoxList_1.append(ckbox)
            cellWidget_1 = QWidget()
            layout_1 = QHBoxLayout(cellWidget_1)
            layout_1.addWidget(self.checkBoxList_1[i])
            layout_1.setAlignment(Qt.AlignCenter)
            layout_1.setContentsMargins(0, 0, 0, 0)
            cellWidget_1.setLayout(layout_1)
            self.QTablewidget.setCellWidget(i, 1, cellWidget_1)

            ckbox = QCheckBox()
            self.checkBoxList_2.append(ckbox)
            cellWidget_2 = QWidget()
            layout_2 = QHBoxLayout(cellWidget_2)
            layout_2.addWidget(self.checkBoxList_2[i])
            layout_2.setAlignment(Qt.AlignCenter)
            layout_2.setContentsMargins(0, 0, 0, 0)
            cellWidget_2.setLayout(layout_2)
            self.QTablewidget.setCellWidget(i, 2, cellWidget_2)

    def insert_captain(self):
        """선택한 팀장, 팀장 명단에 삽입"""
        for i in range(16):
            if self.checkBoxList_2[i].isChecked():
                self.checkBoxList_2[i].setCheckable(False)
                self.checkBoxList_2[i].setEnabled(False)
                captain = self.QTablewidget.item(i, 0)
                captain_name = captain.text()
                self.ldt_captain.setText(captain_name)

    def insert_crew(self):
        self.checked_list_1.clear()
        """선택한 팀원, 팀원 명단에 삽입"""
        crew_text = ""
        for i in range(16):
            if self.checkBoxList_1[i].isChecked():
                self.checkBoxList_1[i].setCheckable(False)
                self.checked_list_1.append((i, 1))
            else:
                pass

        for j in range(len(self.checked_list_1)):
            row = self.checked_list_1[j][0]
            item = self.QTablewidget.item(row, 0)
            crew = item.text()
            self.crew_list.append(crew)
            crew_text += crew + ","
            self.checkBoxList_1[row].setEnabled(False)
        self.ldt_crew.setText(crew_text)
        self.crew_list = []

    def return_team(self):
        dict_team = {'Number': '', 'captain': '', 'crew': ''}

        team_name = self.ldt_name.text()
        team_captain = self.ldt_captain.text()
        team_crews = self.ldt_crew.text()[:-1]

        dict_team['Number'] = team_name
        dict_team['captain'] = team_captain
        dict_team['crew'] = team_crews

        self.db.insert_team_info(dict_team)
        self.team_list.clear()
        self.dlg.set_dialog_type(1, 'save_team')
        self.dlg.exec()

    def ldt_clear(self):
        self.ldt_captain.clear()
        self.ldt_crew.clear()

class ServerMain(ServerScreen):
    """메인 서버 클래스"""
    # 서버 가동 시그널 -> 서버 스크린 emit
    server_on_signal = pyqtSignal(tuple, bool)
    def __init__(self, host_, port_):
        super().__init__()
        self.server_soc = None
        self.room = Room()
        self.address = (host_, port_)

        # -- 서버 스크린
        self.screen = ServerScreen()
        self.server_on_signal.connect(self.screen.server_start)

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
            """▼추가한 함수▼"""
            self.server_on_signal.emit(addr, True)
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