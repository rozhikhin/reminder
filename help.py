import helpForm
import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
import sys

class HelpWindow(QWidget, helpForm.Ui_Form):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("Справка")

    def closeEvent(self, event):
        self.parent.t2 = threading.Timer(self.parent.interval, self.parent.hide_main_window)
        self.parent.t2.start()
        # pass
# if __name__ == "__main__":

    # app = QApplication(sys.argv)
    # help_window = HelpWindow()
    # # Чтобы исключить мелькание, нужно изначально сместить окно за рамки экрана
    # # mainWindow.move(mainWindow.width() * -3, 0)
    # # Показывать окно приложения только в определнное время суток
    # # mainWindow.not_show_window_from_to()
    # # Показать главное окно
    # help_window.show()
    # # Разместить окно в правом нижнем углу
    # # help_window.move_to_right_bottom_corner()
    # sys.exit(app.exec_())