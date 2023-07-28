import sys
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QDate, QPoint, Qt
from PyQt5.QtWidgets import *
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QTextCharFormat

class View(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../UI/MainView.ui', self)


        self.draw_calendar()
        self.btn_setting.clicked.connect(self.update_project_date)

    def update_project_date(self):
        start_day = self.ldt_project_start.text()
        end_day = self.ldt_project_end.text()

        # if len(start_day) >= 7 or len(end_day) >= 7:
        #     self.dlg.set_dialog_type(1, 'len_over_date')
        #     self.dlg.exec()
        # elif len(start_day) < 6 or len(end_day) < 6:
        #     self.dlg.set_dialog_type(1, 'len_over_date')
        #     self.dlg.exec()
        # else:
        start = datetime.strptime('20' + start_day, "%Y%m%d")
        end = datetime.strptime('20' + end_day, "%Y%m%d")
        diff = end - start

        start_day_f = QDate.fromString('20' + start_day, 'yyyyMMdd')
        end_day_f = QDate.fromString('20' + end_day, 'yyyyMMdd')
        self.calendarWidget.setDateRange(start_day_f, end_day_f)

        fm = QTextCharFormat()
        fm.setForeground(QColor('red'))
        fm.setBackground(QColor('yellow'))

        # self.calendarWidget.setDateTextFormat(start_day_f, fm)
        # self.calendarWidget.setDateTextFormat(end_day_f, fm)

        for i in range(diff.days-1):
            self.calendarWidget.setDateTextFormat(start_day_f.addDays(i+1), fm)

    def draw_calendar(self):

        self.calendarWidget.setDateTextFormat(QDate(), QTextCharFormat())
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()
    view.show()
    app.exec_()