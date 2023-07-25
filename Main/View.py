import sys

from PyQt5.QtWidgets import QWidget, QApplication

from UI.UI_MainView import Ui_MainWidget

class View(QWidget, Ui_MainWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 큐 프레임과 스택 위젯의 초기 크기 설정
        initial_queue_frame_width = 100
        initial_stacked_widget_width = self.page_3.width() - initial_queue_frame_width
        self.splitter.setSizes([initial_stacked_widget_width, initial_queue_frame_width])

        def update_sizes(pos, index):
            queue_frame_width = self.splitter.sizes()[1]
            stacked_widget_width = self.splitter.sizes()[0]
            # 큐 프레임과 스택 위젯의 크기 설정
            self.frame_talk.setFixedWidth(queue_frame_width)
            self.stackedWidget_main.setFixedWidth(stacked_widget_width)

        self.splitter.splitterMoved.connect(update_sizes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()
    view.show()
    app.exec_()