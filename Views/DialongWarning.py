import sys, os
from PyQt5 import uic

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 메인화면
main = resource_path('../UI/warning_dialog.ui')
dlg_class = uic.loadUiType(main)[0]

class DialogWarning(QDialog, dlg_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.connect_event()

    # 아니오, 닫기 눌렀을 때
    def close_screen(self):
        self.close()

    # 이벤트 연결
    def connect_event(self):
        # 예, 확인 : accept (1)
        # 아니오, 닫기 : reject (0)
        self.btn_single.clicked.connect(self.close_screen)
        self.btn_yes.clicked.connect(self.close_screen)
        self.btn_close.clicked.connect(self.close_screen)
        self.btn_no.clicked.connect(self.close_screen)

    # 다이얼로그 타입 설정
    # bt_cnt : 버튼 수량
    # t_type : 다이얼로그 타입
    def set_dialog_type(self, bt_cnt: int, t_type="", text=""):
        if bt_cnt == 1:
            self.layout_double.setVisible(False)
            self.btn_single.setVisible(True)

        elif bt_cnt == 2:
            self.layout_double.setVisible(True)
            self.btn_single.setVisible(False)
        if t_type == 'login':
            self.lbl_text.setText('로그인 완료')
        elif t_type == 'email_no_input':
            self.lbl_text.setText('이메일을 입력해주세요.')
        elif t_type == 'pw_input':
            self.lbl_text.setText('비밀번호를 입력해주세요')
        elif t_type == 'pw_not_match':
            self.lbl_text.setText('잘못된 비밀번호입니다.')
        elif t_type == 'pw_send_email':
            self.lbl_text.setText('비밀번호를 이메일로 전송했습니다.')
        elif t_type == 'pw_alphabet_1':
            self.lbl_text.setText('비밀번호에 최소 영대문자 1글자 이상 포함되어야 합니다.')
        elif t_type == 'pw_unique_word':
            self.lbl_text.setText('비밀번호에 최소 특수문자 1글자 이상 포함되어야 합니다.')
        elif t_type == 'pw_len_limited':
            self.lbl_text.setText('비밀번호는 최소 5자, 최대 16자까지 입력가능합니다.')
        elif t_type == 'state_len_limit':
            self.lbl_text.setText('상태메세지는 최대 20자까지 가능합니다.')
        elif t_type == 'email_no_check':
            self.lbl_text.setText('이메일 인증을 진행 해주세요.')

