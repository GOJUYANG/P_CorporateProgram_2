from PyQt5.uic import loadUi

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

class DialogWarning(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../UI/MainView.ui', self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connect_event()

    # 이벤트 연결
    def connect_event(self):
        # 예, 확인 : accept (1)
        # 아니오, 닫기 : reject (0)
        self.btn_single.clicked.connect(self.close_screen)
        self.btn_yes.clicked.connect(self.close_screen)
        self.btn_close.clicked.connect(self.close_screen)
        self.btn_no.clicked.connect(self.close_screen)

    # 아니오, 닫기 눌렀을 때
    def close_screen(self):
        self.close()

    def set_dialog_type(self, bt_cnt: int, t_type=""):
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
        elif t_type == 'save_team':
            self.lbl_text.setText('팀 저장 완료')
        elif t_type == 'upload_only_code':
            self.lbl_text.setText('댓글 없이 올리시겠습니까?')
        elif t_type == 'upload_only_comment':
            self.lbl_text.setText('코드 없이 올리시겠습니까?')
        elif t_type == 'len_over_date':
            self.lbl_text.setText('날짜는 230724 와 같이 입력해주세요')
        elif t_type == 'fill_up_ldt':
            self.lbl_text.setText('한 일을 적어 주세요')
        elif t_type == 'sure_to_logout':
            self.lbl_text.setText('로그 아웃 하시겠습니까?')
