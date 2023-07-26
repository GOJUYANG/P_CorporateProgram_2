import sys, os
from PyQt5 import uic

from PyQt5.QtWidgets import QDialog

from Views.DialongWarning import DialogWarning

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 메인화면
main = resource_path('../UI/Login.ui')
dlg_class = uic.loadUiType(main)[0]

class DlgLogin(QDialog, dlg_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 버튼 이벤트
        self.btn_close.clicked.connect(self.close_popup)

        # 라벨 이벤트
        self.lb_forgot_pwd.mousePressEvent = lambda e: self.send_email_pwd(e)

        # 클래스 호출
        self.dlg = DialogWarning()

    def close_popup(self):
        self.close()

    # def send_email_pwd(self, e):
    #     if self.ldt_email.text() == "":
    #         self.lb_warning_email.setText("로그인용 이메일을 입력해주세요")
    #     else:
    #         self.close()
    #         self.dlg.set_dialog_type(1, "pw_send_email")
    #         self.dlg.exec()
    #         self.db
