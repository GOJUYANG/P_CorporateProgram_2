import sys
from datetime import datetime, timedelta

from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QDate, QPoint, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Views.DialongWarning import DialogWarning
from Views.Setting import DlgSetting
from Views.login import DlgLogin
from Server.DataRead import DataClass
from Client.ClientSocket import ClientSocket # 추가한 파일(클라이언트 소켓)

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../UI/MainView.ui', self)

        # --- 변수
        self.home_text = ['안녕하세요!', '협업을 위한!', '협업에 의한!', '당신을 위한!']

        # --- Qtimer 생성
        self.time = 0
        timer = QTimer(self)
        timer.start(1000)
        timer.timeout.connect(self.change_text)

        # DB 연결
        self.db = DataClass()

        # 함수 호출
        self.init_ui()
        self.connect_event()
        self.widget_click_event()
        self.label_click_event()
        self.delete_worktable()
        ## 새로추가한 함수 ##
        self._default_set()

        # 다이얼로그 인스턴스
        self.dlg = DialogWarning()
        self.setting = DlgSetting()
        self.login_popup = DlgLogin(self.ClientSocket)

    def _default_set(self):
        self.ClientSocket = ClientSocket()
        self.ClientSocket.clientsocket_Set()

    def connect_event(self):
        """버튼 이벤트"""

        #--home page
        self.btn_click.clicked.connect(lambda: self.login_popup.show())
        self.btn_login.clicked.connect(lambda: self.popup("login", 0, ""))
        self.btn_notice.clicked.connect(lambda: self.popup("setting", 3, ""))

        #--stakoverflow page
        self.btn_comm_send.clicked.connect(self.upload_comment)

        #--calender page
        self.btn_setting.clicked.connect(self.update_project_date)
        self.btn_ing.clicked.connect(lambda : self.insert_worktable('진행'))
        self.btn_done.clicked.connect(lambda : self.insert_worktable('완료'))
        self.btn_text.clicekd.connect(self.draw_calendar)

    def widget_click_event(self):
        """위젯 클릭 이벤트"""
        self.widget_flow.mousePressEvent = lambda e: self.stackedWidget_main_2.setCurrentWidget(self.page_list)
        self.widget_calender.mousePressEvent = lambda e: self.stackedWidget_main_2.setCurrentWidget(self.page_calender)

    def label_click_event(self):
        """라벨 클릭 이벤트"""
        self.lb_exit.mousePressEvent = lambda e: self.popup("dlg", 2, 'sure_to_logout')
        self.lb_setting.mousePressEvent = lambda e: self.popup("setting")
        self.lb_upload.mousePressEvent = lambda e, idx=2: self.move_page(idx)
        self.lb_clear.mousePressEvent = lambda e: self.chat_clear
        self.lb_exit_2.mousePressEvent = self.home_page

    def home_page(self, e):
        self.stackedWidget.setCurrentWidget(self.page_login)
        self.stackedWidget_main.setCurrentWidget(self.page_home)

    def init_ui(self):
        """초기 화면 설정"""
        self.stackedWidget_title.setCurrentWidget(self.page_login)
        # self.login_popup.lb_warning_email.setText("")
        # self.login_popup.lb_warning_pwd.setText("")
        # self.setting_teammate()

    def popup(self, type: str, bt_cnt: int, t_type: str):
        """다이얼로그 창 띄우기"""
        if type == 'login':
            self.login_popup.show()

        elif type == "setting":
            # user_list = self.db.select_user_info('user_email, user_nm')
            # self.setting.set_users_login_info(user_list)
            # self.setting.exec()
            pass

        elif type == 'dlg':
            self.dlg.set_dialog_type(bt_cnt, t_type)
            self.dlg.exec()

    def change_text(self):
        """메인 홈 환영 문구를 변경 합니다"""
        idx = self.time % 4
        self.lb_middle.setText(self.home_text[idx])
        self.time += 1

    def open_dlg_setting(self):
        img, name, state = self.setting.update_user_state()
        self.setting.profile_setting(img, name, state)
        # self.db.update_user_info(img, name, state)

    def move_page(self, idx):
        self.stackedWidget_main.setCurrentIndex(idx)
        self.upload_code()

    def move_title_page(self, idx):
        self.stackedWidget.setCurrentIndex(idx)

    # def setting_teammate(self):
    #     my_teammate = self.db.find_my_teammate()
    #     icon_list = [self.icon_crew_1, self.icon_crew_2, self.icon_crew_3]
    #     name_list = [self.lb_crew_name_1, self.lb_crew_name_2, self.lb_crew_name_3]
    #     state_list = [self.lb_crew_state_1,self.lb_crew_state_2,self.lb_crew_state_3]
    #     for i in range(len(my_teammate)):
    #         if my_teammate[i][2] != 'none':
    #             self.icon_captain.setPixmap(QPixmap(f'../IMG/profile/{my_teammate[i][4]}'))
    #             self.lb_captain_name.setText(f"{my_teammate[i][2].rstrip(' ')}")
    #             self.lb_captain_state.setText(f"{my_teammate[i][5]}")
    #         else:
    #             for j in range(len(my_teammate)-1):
    #                 icon_list[j].setPixmap(QPixmap(f'../IMG/profile/{my_teammate[j][4]}'))
    #                 name_list[j].setText(f"{my_teammate[j][3].rstrip(' ')}")
    #                 state_list[j].setText(f"{my_teammate[j][5]}")

    def upload_code(self):
        self.ldt_title.setReadOnly(False)

    def upload_comment(self):
        if self.ldt_comment.text() == "":
            self.dlg.set_dialog_type(1,'upload_only_code')
            #코드만 올리는 코드
        elif self.text_code.text() == "":
            self.dlg.set_dialog_type(1, 'upload_only_comment')
            #댓글만 올리는 코드
        else:
            #댓글+코드 업로드하는 코드
            pass

    def chat_clear(self):
        """채팅방 내용 삭제"""
        pass

    def update_project_date(self):
        start_day = self.ldt_project_start.text()
        end_day = self.ldt_project_end.text()

        if len(start_day) >= 7 or len(end_day) >= 7:
            self.dlg.set_dialog_type(1, 'len_over_date')
            self.dlg.exec()
        elif len(start_day) < 6 or len(end_day) < 6:
            self.dlg.set_dialog_type(1, 'len_over_date')
            self.dlg.exec()
        else:
            start = datetime.strptime('20' + start_day, "%Y%m%d")
            end = datetime.strptime('20' + end_day, "%Y%m%d")
            diff = end - start

        start_day_f = QDate.fromString(start_day, 'yyyyMMdd')
        end_day_f = QDate.fromString(end_day, 'yyyyMMdd')
        self.calendarWidget.setDateRange(start_day_f, end_day_f)


        fm = QTextCharFormat()
        fm.setForeground(QColor('red'))
        fm.setBackground(QColor('yellow'))

        # self.calendarWidget.setDateTextFormat(start_day_f, fm)
        # self.calendarWidget.setDateTextFormat(end_day_f, fm)

        for i in range(diff.days-1):
            self.calendarWidget.setDateTextFormat(start_day_f.addDays(i+1), fm)

    def draw_calendar(self):

        self.calendarWidget.setDateTextFormat(QDate(), "")

        self.calendarWidget.events = {
            QDate(2023, 7, 24): ["시작"],
            QDate(2023, 7, 29): ["마감"]
        }

        # QCalendarWidget에 직접 paintCell 이벤트를 연결합니다.
        self.calendarWidget.paintCell = self.customPaintCell

    def customPaintCell(self, painter, rect, date):
        """QCalendarWidget의 PaintCell()을 커스텀하였습니다."""
        QCalendarWidget.paintCell(self.calendarWidget, painter, rect, date)

        if date in self.calendarWidget.events:
            painter.setBrush(Qt.red)
            painter.drawEllipse(rect.topLeft() + QPoint(12,7),3,3)
            painter.drawText(rect.topLeft() + QPoint(30,10),
                             "{}".format(", ".join(self.calendarWidget.events[date])))

        painter.restore()

    def insert_worktable(self, name):
        if self.ldt_work == "":
            self.dlg.set_dialog_type(1, "fill_up_ldt")
            self.dlg.exec()
        else:
            date = self.calendarWidget.selectedDate()
            date = date.toString('yyyy.MM.dd')
            time = self.listWidget.currentItem().text()
            work = self.ldt_work.text()
            state = name

            row = self.work_table.rowCount()
            self.work_table.insertRow(row)
            self.work_table.setItem(row,0,QTableWidgetItem(date+time))
            self.work_table.setItem(row,1,QTableWidgetItem("일단조원아무나"))
            self.work_table.setItem(row,2,QTableWidgetItem(state))
            self.work_table.setItem(row,3,QTableWidgetItem(work))
            self.ldt_work.clear()

    def delete_worktable(self):
        # 현재 시간
        current_time = datetime.now()

        # 하루 후 시간 계산
        one_day_after = current_time + timedelta(days=1)

        # 하루가 지났는지 확인
        if current_time < one_day_after:
            print("하루가 지나지 않았습니다.")
        else:
            print("하루가 지났습니다.")
            self.work_table.clearContents()
            print(" [ 삭제/QT ] : 일정공유 테이블 ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainView()
    view.show()
    app.exec_()
