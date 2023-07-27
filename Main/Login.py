import pickle
import sys

from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi

class LoginFunction(QDialog):
    def __init__(self, soc):
        super().__init__()
        loadUi('../UI/Login.ui', self)
        self.controller = soc
        self._default_set()
        self.data_ = None

    @pyqtSlot(list)
    def recv_from_Control(self, recv_list):
        """서버에게 받은 값을 리스트형태로 받음"""
        print(recv_list, "서버에서 Login파일로 슬롯 받은 DB데이터입니다.")
        self.login_check_func(recv_list)

    def login_check_func(self, data_):
        """로그인 체크 기능 추후 로그인 체크기능으로 수정해야합니다."""
        print(data_, "로그인 체크 기능으로 받은 데이터입니다.")
        self.label_5.clear()
        if data_[0] == 'not find':
            self.label_5.setText("이메일이 일치하지 않습니다.")
            self.lineEdit.setFocus()
        else:
            if self.lineEdit_2.text() == data_[1]:
                print('로그인 성공')
                self.data_ = data_
                self.close()
                return self.data_
            else:
                self.label_4.setText("비밀번호가 일치하지 않습니다.")
                self.lineEdit_2.clear()
                self.lineEdit_2.setFocus()

    def controller_to_send(self, header, msg):
        """
        :param msg: 서버에게 보내는 메시지
        :return:
        """
        self.controller.client_Send_Func(header, msg)

    def lineEdit_Func(self):
        """라인 에딧 텍스트의 값을 엔터시 클라이언트를 통해 서버에게 값을 전달함."""
        if self.lineEdit_2.text() == '':
            self.label_4.setText("비밀번호를 입력하지 않았습니다.")
            self.lineEdit_2.setFocus()

        if self.lineEdit.text() != '':
            user_email = self.lineEdit.text()
            self.controller_to_send("Server", f"None:None:DB/Login/{user_email}")
        else:
            self.label_5.setText("이메일을 입력하지 않았습니다.")
            self.lineEdit.setFocus()

    def _default_set(self):
        """윈도우 초기 설정값"""
        self._controller_connect_Function()
        self._btn_connect()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.lineEdit.setFocus()

    def _controller_connect_Function(self):
        """컨트롤러와 이어주는 기능"""
        self.controller.db_signal.connect(self.recv_from_Control)

    def _btn_connect(self):
        """버튼 연결 기능"""
        self.pushButton.clicked.connect(self.lineEdit_Func)
        self.pushButton_2.clicked.connect(self.close)

        self.lineEdit.returnPressed.connect(self.lineEdit_Func)
        self.lineEdit_2.returnPressed.connect(self.lineEdit_Func)
        self.lineEdit.textChanged.connect(self.lineEdit_text_check)

    def lineEdit_text_check(self, e):
        """이메일 입력시 예외처리"""
        text_list = [':', ';', ',', '{', '}', '(', ')', '[', ']', '\\', '/', '>', '<', '-', '=', '+', '?', '!', '%', '\'', '\"']
        for i in self.lineEdit.text():
            if i in text_list:
                self.lineEdit.setText(self.lineEdit.text()[:-1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainapp = LoginFunction()
    mainapp.show()
    sys.exit(app.exec_())





