import sys
from PyQt5.uic import loadUi

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from Views.DialongWarning import DialogWarning
from Server.DataRead import DataClass
from Server.ServerSocket import ServerMain

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

        # 서버 소켓과 연결
        self.s = ServerMain(self)
        # self.ip = socket.gethostbyname(socket.gethostname())
        # self.port = 7001

        # --- DB연결
        self.db = DataClass()
        self.dlg = DialogWarning()

        # --- 관리자화면
        self.server_btn.clicked.connect(self.server_start)
        self.btn_add.clicked.connect(self.insert_table_widget)
        self.btn_crew.clicked.connect(self.insert_crew)
        self.btn_captain.clicked.connect(self.insert_captain)
        self.btn_team.clicked.connect(self.return_team)
        self.btn_clear.clicked.connect(self.ldt_clear)

    def server_start(self, state):
        if state:
            ip = self.ldt_ip.text()
            port = self.ldt_port.text()
            if self.s.start(ip, int(port)):
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
        """DB로 구성 팀 반환 [{},{}...] """
        dict_team = {'Number': '', 'captain': '', 'crew': []}
        team_name = self.ldt_name.text()
        team_captain = self.ldt_captain.text()
        team_crews = self.ldt_crew.text()[:-1]
        dict_team['Number'] = [team_name]
        dict_team['captain'] = [team_captain]
        dict_team['crew'] = [team_crews]
        self.team_list.append(dict_team)
        crew_num = len(team_crews.split(','))
        self.db.insert_team_info(self.team_list, crew_num)
        self.team_list.clear()
        self.dlg.set_dialog_type(1, 'save_team')
        self.dlg.exec()

    def ldt_clear(self):
        self.ldt_captain.clear()
        self.ldt_crew.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = ServerScreen()
    screen.show()
    app.exec()