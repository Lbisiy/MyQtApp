from PySide6 import QtCore, QtWidgets


class Calendar(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация UI
        :return: None
        """
        self.setSelectedDate(QtCore.QDate.currentDate())
        self.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    win = Calendar()
    win.show()

    app.exec()
