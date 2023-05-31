from PySide6 import QtCore, QtGui, QtWidgets


class Calendar(QtWidgets.QCalendarWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.availableDates = []
        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """
        Доинициализация UI
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
