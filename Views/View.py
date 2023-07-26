import sys, os

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *

from Views.DialongWarning import DialogWarning
from Views.Setting import DlgSetting
from Views.login import DlgLogin
from Server.DataRead import DataClass

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 메인화면
main = resource_path('../UI/MainView.ui')
main_class = uic.loadUiType(main)[0]

class View(QWidget, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # --- 변수
        self.home_text = ['안녕하세요!', '협업을 위한!', '협업에 의한!', '당신을 위한!']

        # --- Qtimer 생성
        self.time = 0
        timer = QTimer(self)
        timer.start(1000)
        timer.timeout.connect(self.change_text)

        # 다이얼로그 인스턴스
        self.dlg = DialogWarning()
        self.setting = DlgSetting()
        self.login_popup = DlgLogin()

        # DB 연결
        self.db = DataClass(type='master')

        # 함수 호출
        self.init_ui()  # UI 설정
        self.connect_event()
        self.widget_click_event()
        self.label_click_event()

    def connect_event(self):
        """버튼 이벤트"""

        #===홈화면===#
        self.btn_click.clicked.connect(lambda: self.stackedWidget_main.setCurrentIndex(1))
        self.btn_click.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_login.clicked.connect(lambda: self.popup("login", 0, ""))
        self.btn_notice.clicked.connect(lambda: self.popup("setting", 3, ""))

    def widget_click_event(self):
        """위젯 클릭 이벤트"""
        pass

    def label_click_event(self):
        """라벨 클릭 이벤트"""
        self.lb_setting.mousePressEvent = lambda e: self.open_dlg_setting
        pass

    def init_ui(self):
        """초기 화면을 설정합니다."""
        self.stackedWidget.setCurrentWidget(self.page_login)
        self.login_popup.lb_warning_email.setText("")
        self.login_popup.lb_warning_pwd.setText("")

    def popup(self, type:str, bt_cnt:int, t_type:str):
        """다이얼로그 창을 띄우는 함수입니다."""
        if type == 'login':
            self.login_popup.show()
        elif type == "setting":
            user_list = self.db.select_user_info('user_email, user_nm')
            self.setting.set_users_login_info(user_list)
            self.setting.exec()
        elif type == 'dlg':
            self.dlg.set_dialog_type(1, bt_cnt, t_type)

    def change_text(self):
        """메인 홈 환영 문구를 변경 합니다"""
        idx = self.time % 4
        self.lb_middle.setText(self.home_text[idx])
        self.time += 1

    def open_dlg_setting(self):
        img, name, state = self.setting.update_user_state()
        self.setting.profile_setting(img, name, state)
        self.db.update_user_info(img, name, state)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()
    view.show()
    app.exec_()