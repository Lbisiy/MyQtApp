import time

from PySide6 import QtWidgets, QtGui

from ui.utilites.db_utility import DbWorker
from ui.widgets.calendar import Calendar
from ui.widgets.child_window import ChildWindow


class MyDelegate(QtWidgets.QItemDelegate):
    def createEditor(self, *args):
        return None


class MainWindow(QtWidgets.QWidget):
    """
    Основное окно с календарем и текстовым полем для вывода информации о заметке на конкретную дату
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.initUi()
        self.initDB()
        self.initSignals()

        self.record = None
        self.date = None
        self.date_to_DB = None

    def initUi(self) -> None:
        """
        Инициализация UI
        :return: None
        """
        self.setWindowTitle("Notepad")
        self.setFixedSize(480, 640)

        spacerCreateNote = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.pushButtonCreateNote = QtWidgets.QPushButton()
        self.pushButtonCreateNote.setText("Note")

        self.textEditNoteInfo = QtWidgets.QTableWidget(8, 1)
        self.textEditNoteInfo.setItemDelegateForColumn(0, MyDelegate())
        self.textEditNoteInfo.setColumnWidth(0, 200)
        self.textEditNoteInfo.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.textEditNoteInfo.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        layoutCreateNote = QtWidgets.QHBoxLayout()
        layoutCreateNote.addItem(spacerCreateNote)
        layoutCreateNote.addWidget(self.pushButtonCreateNote)

        layoutCalendar = QtWidgets.QHBoxLayout()
        self.calendar = Calendar()
        layoutCalendar.addWidget(self.calendar)

        layoutNoteInfo = QtWidgets.QHBoxLayout()
        layoutNoteInfo.addWidget(self.textEditNoteInfo)

        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addLayout(layoutCreateNote)
        layoutMain.addLayout(layoutCalendar)
        layoutMain.addLayout(layoutNoteInfo)

        self.setLayout(layoutMain)

    def initDB(self) -> None:
        """
        Подключение к БД и создание таблицы с данными о заметках
        :return: None
        """
        self.db_client = DbWorker()

        self.db_client.connectDB()
        if not self.db_client.cursor:
            QtWidgets.QMessageBox.warning(self, "Connection Error", "Connection to DB is failed")
        self.db_client.createTableDB()

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """
        self.calendar.clicked.connect(self.textEditNoteInfo.clear)
        self.calendar.clicked.connect(self.selectQueryDB)
        self.calendar.clicked.connect(self.showNoteInfo)

        self.calendar.activated.connect(self.selectQueryDB)
        self.calendar.activated.connect(self.openChildWindow)

        self.pushButtonCreateNote.clicked.connect(self.textEditNoteInfo.clear)
        self.pushButtonCreateNote.clicked.connect(self.textEditNoteInfo.clearSpans)
        self.pushButtonCreateNote.clicked.connect(self.selectQueryDB)
        self.pushButtonCreateNote.clicked.connect(self.showNoteInfo)
        self.pushButtonCreateNote.clicked.connect(self.openChildWindow)

    def selectQueryDB(self) -> None:
        """
        Получение данных о заметках из таблицы БД
        :return: None
        """
        self.date = self.calendar.selectedDate()
        self.date_to_DB = self.date.toString('MMMM d, yyyy')

        self.db_client.readTableDB(self.date_to_DB)

    def openChildWindow(self) -> None:
        """
        Вывод дочернего окна с информацией о заметке на выбранную дату, либо для удаления заметки
        :return: None
        """
        self.child_window = ChildWindow(self)
        self.child_window.installEventFilter(self)
        self.child_window.signal_to_main.connect(self.createQueryDB)
        self.child_window.lineEditNoteDate.setText(self.date_to_DB)

        if self.db_client.record is not None:
            note_name = self.db_client.record[0]
            note = self.db_client.record[2]

            self.child_window.lineEditNoteName.setText(note_name)
            self.child_window.textEditNoteText.setText(note)
        else:
            self.child_window.lineEditNoteName.setText("")
            self.child_window.textEditNoteText.setText("")

        self.child_window.exec()

    def showNoteInfo(self) -> None:
        """
         Отображение информации о заметках в нижнем поле с текстом
        :return: None
        """
        if self.db_client.record is not None:

            for i in range(len(self.db_client.record)):
                self.textEditNoteInfo.setItem(i, 0, QtWidgets.QTableWidgetItem(self.db_client.record[i]))

            self.textEditNoteInfo.setItem(4, 0, QtWidgets.QTableWidgetItem("Current date:"))
            self.textEditNoteInfo.setItem(5, 0, QtWidgets.QTableWidgetItem(time.ctime()))

    def createQueryDB(self, signal) -> None:
        """
        Добавление или удаление информации о заметке в БД
        :param signal: информация о заметке, передаваемая дочерним окном
        :return: None
        """
        if signal['name_note'] == "" and signal['note'] == "":

            self.db_client.deleteTableDB(signal)
            self.selectQueryDB()
            self.showNoteInfo()

        else:

            self.db_client.updateTableDB(signal)
            self.selectQueryDB()
            self.showNoteInfo()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Закрытие подключения к БД при закрытии основного окна
        :param event: событие закрытия окна
        :return: None
        """
        self.db_client.close_connection()


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    win = MainWindow()
    win.show()

    app.exec()

