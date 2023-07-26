import sys, os
from PyQt5 import uic

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from Server.DataRead import DataClass

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 메인화면
main = resource_path('../UI/setting.ui')
dlg_class = uic.loadUiType(main)[0]

class DlgSetting(QDialog, dlg_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 변수
        self.img = 'img_profile_1'
        self.state = self.lineEdit_state.text()

        # 뒤로가기
        self.btn_back_1.clicked.connect(lambda: self.stack_setting.setCurrentIndex(0))
        self.btn_back_2.clicked.connect(lambda: self.stack_setting.setCurrentIndex(0))
        self.btn_back_3.clicked.connect(lambda: self.stack_setting.setCurrentIndex(0))

        # close
        self.btn_close.clicked.connect(self.close_screen)
        self.btn_close_2.clicked.connect(self.close_screen)

        # 첫화면 버튼
        self.btn_notice.clicked.connect(lambda: self.stack_setting.setCurrentWidget(self.page_notice))
        self.btn_profile.clicked.connect(lambda: self.stack_setting.setCurrentWidget(self.page_profile))
        self.btn_logout.clicked.connect(self.close_screen)

        # 프로필
        self.btn_img_edit.clicked.connect(lambda: self.stack_setting.setCurrentWidget(self.page_img_choice))
        self.btn_profile_save.clicked.connect(self.update_user_state)
        self.btn_choice.clicked.connect(self.change_profile_img)

        # ui 설정
        self.init_setting()

    def init_setting(self):
        self.lbl_img_profile.setPixmap(QPixmap(f'../IMG/profile/{self.img}.png'))

    def set_users_login_info(self, login_list):
        for k, v in enumerate(login_list):
            self.tableWidget.setItem(k, 0, QTableWidgetItem(f"{login_list[k][1]}"))
            self.tableWidget.setItem(k, 2, QTableWidgetItem(f"{login_list[k][0]}"))

    def profile_setting(self, profile, name, state):
        self.lbl_img_profile.setPixmap(QPixmap(f'../IMG/profile/{profile}.png'))
        self.ldt_name.setText(f"{name}")
        self.lineEdit_state.setText(f"{state}")

    def change_profile_img(self):
        for btn in self.btn_bundle.findChildren(QPushButton):
            if btn.isChecked():
                self.img = btn.objectName()
                self.lbl_img_profile.setPixmap(QPixmap(f"../IMG/profile/{self.img}.png"))
                break

        self.stack_setting.setCurrentWidget(self.page_profile)

    # 프로필 변경사항 -> DB
    def update_user_state(self):
        img_ = self.img
        name_ = self.ldt_name.text()
        state_ = self.lineEdit_state.text()
        return img_, name_, state_


    def close_screen(self):
        self.close()