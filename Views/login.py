import sys, os
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.Qt import *

from Views.DialongWarning import DialogWarning
from Server.DataRead import DataClass

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 메인화면
main = resource_path('../UI/Login.ui')
dlg_class = uic.loadUiType(main)[0]

class DlgLogin(QDialog, dlg_class):
    def __init__(self, soc):
        super().__init__()
        self.setupUi(self)


        """추가한 항목▼"""
        self.controller = soc
        self._default_set()
        self.data_ = None
        """추가한 항목▲"""


        # 인증메일 송신자
        self.s_email = 'rhrnaka@gmail.com'
        self.s_pwd = 'tpomkywvwdqzwbvj'
        self.r_email = ""
        self.user_nm = ""
        self.user_pw = ""

        # 버튼 이벤트
        self.btn_close.clicked.connect(self.close_popup)
        self.btn_login.clicked.connect(self.req_login)

        # 라벨 이벤트
        self.btn_pwd.clicked.connect(self.click_forgot_password)

        # 클래스 호출
        self.dlg = DialogWarning()
        self.db = DataClass()
    """▼추가한 함수▼"""

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
    def _default_set(self):
        """윈도우 초기 설정값"""
        self._controller_connect_Function()
        self._btn_connect()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.ldt_email.setFocus()

    def _controller_connect_Function(self):
        """컨트롤러와 이어주는 기능"""
        self.controller.db_signal.connect(self.recv_from_Control)

    def _btn_connect(self):
        """버튼 연결 기능"""
        self.btn_login.clicked.connect(self.lineEdit_Func)
        self.btn_close.clicked.connect(self.close)

        self.ldt_email.returnPressed.connect(self.lineEdit_Func)
        self.ldt_pwd.returnPressed.connect(self.lineEdit_Func)
        self.ldt_email.textChanged.connect(self.lineEdit_text_check)
    def lineEdit_Func(self):
        """라인 에딧 텍스트의 값을 엔터시 클라이언트를 통해 서버에게 값을 전달함."""
        if self.ldt_pwd.text() == '':
            self.lb_warning_pwd.setText("비밀번호를 입력하지 않았습니다.")
            self.ldt_pwd.setFocus()

        if self.ldt_email.text() != '':
            user_email = self.ldt_email.text()
            self.controller_to_send("Server", f"None:None:DB/Login/{user_email}")
        else:
            self.ldt_email.setText("이메일을 입력하지 않았습니다.")
            self.ldt_email.setFocus()
    def controller_to_send(self, header, msg):
        """
        :param msg: 서버에게 보내는 메시지
        :return:
        """
        self.controller.client_Send_Func(header, msg)
    def lineEdit_text_check(self, e):
        """이메일 입력시 예외처리"""
        text_list = [':', ';', ',', '{', '}', '(', ')', '[', ']', '\\', '/', '>', '<', '-', '=', '+', '?', '!', '%', '\'', '\"']
        for i in self.ldt_pwd.text():
            if i in text_list:
                self.ldt_pwd.setText(self.ldt_pwd.text()[:-1])

    """▲▲추가한 함수▲▲"""
    def close_popup(self):
        self.close()

    def req_login(self):
        if self.ldt_email == "":
            self.lb_warning_email.setText("이메일을 입력해주세요")
        elif self.ldt_pwd == "":
            self.lb_warning_pwd.setText("비밀번호를 입력하지 않았습니다.")
        else:
            login_result = self.db.select_user_info(column='user_pw, user_img, user_nm, user_state', user_email=self.ldt_email.text(), plus=f" user_pw='{self.ldt_pwd.text()}'")
            if login_result in [None, 0]:
                self.dlg.set_dialog_type(1, "pw_not_match")
            else:
                self.dlg.set_dialog_type(1, "login")
                self.dlg.exec()
                return login_result
        return False

    def click_forgot_password(self):
        if self.ldt_email.text() == "":
            self.lb_warning_email.setText("로그인용 이메일을 입력해주세요")
        else:
            self.close()
            self.dlg.set_dialog_type(1, "pw_send_email")
            self.dlg.exec()
            find_email_result = self.db.select_user_info('user_nm, user_pw', self.ldt_email.text())
            if find_email_result:
                self.user_nm = find_email_result[0][0].strip('')
                self.user_pw = find_email_result[0][1].strip('')
                self.r_email = self.ldt_email.text()
                self.send_pwd_email()

    def email_content(self):
        """메일 html 리턴"""
        To = f'{self.r_email}'
        e_content_1 = f"{self.user_nm}님의 비밀번호입니다."
        e_content_2 = f"비밀번호 : {self.user_pw}"
        title = f"[NONE ERROR] {self.user_nm}님의 비밀번호를 보내드립니다."

        html = f"""\
        <!DOCTYPE html>
         <html lang="en">
         <head>
             <meta charset="UTF-8" />
             <meta name="viewport" content="width=device-width, initial-scale=1.0" />
             <title>{title}</title>
         </head>
         <body>
             <h4>안녕하세요. {self.user_nm} 님. </h4>
             <p style="padding:5px 0 0 0;">{e_content_1} </p>
             <p style="padding:5px 0 0 0;">{e_content_2} </p>
         </body>
         </html>
         """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = self.s_email
        msg['To'] = self.r_email
        html_msg = MIMEText(html, 'html')
        msg.attach(html_msg)

        return msg

    def send_pwd_email(self):
        # SMTP()서버의 도메인 및 포트를 인자로 접속하여 객체 생성
        server = smtplib.SMTP('smtp.gmail.com', 587)

        # 접속 후 프로토콜에 맞춰 먼저 SMTP서버에 HELLO 메세지를 전송한다.
        server.ehlo()

        # 서버의 암호화 방식을 설정 -> TLS : Gmail 권장, SSL보다 향상된 보안
        server.starttls()

        # 서버 로그인
        server.login(self.s_email, self.s_pwd)
        # 이메일 발송
        try:
            server.sendmail(self.s_email, self.r_email, self.email_content().as_string())
            print("이메일 전송 성공")
        except Exception as e:
            print(e)
            print("이메일 전송 실패")

        # 작업을 마친 후 SMTP와의 연결을 끊는다.
        server.quit()


