from PySide6 import QtWidgets, QtCore, QtGui
import time

from ui.widgets.main_window import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    win = MainWindow()
    with open("ui/themes/DarkStyleTheme.qss", "r") as fh:
        win.setStyleSheet(fh.read())

    loading_window = QtGui.QPixmap('ui/themes/loading.gif')
    loading_window = QtWidgets.QSplashScreen(loading_window, QtCore.Qt.WindowStaysOnTopHint)
    loading_window.setMask(loading_window.mask())
    loading_window.show()
    app.processEvents()
    time.sleep(3)
    loading_window.close()

    win.show()

    app.exec()
