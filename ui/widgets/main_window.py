import time

import psycopg2
from psycopg2 import Error

from PySide6 import QtWidgets, QtGui, QtCore

from ui.widgets.calendar import Calendar
from ui.widgets.child_window import ChildWindow



class MainWindow(QtWidgets.QWidget):
    """
    Основное окно с календарем и текстовым полем для вывода информации о заметке на конкретную дату
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.calendar = Calendar()
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
        self.textEditNoteInfo = QtWidgets.QTextEdit()
        #self.textEditNoteInfo = QtWidgets.QTableView()  # TODO

        layoutCreateNote = QtWidgets.QHBoxLayout()
        layoutCreateNote.addItem(spacerCreateNote)
        layoutCreateNote.addWidget(self.pushButtonCreateNote)

        layoutCalendar = QtWidgets.QHBoxLayout()
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
        try:
            self.connection = psycopg2.connect(
                                            database="postgres",
                                            user="postgres",
                                            password="victory",
                                            host="localhost",
                                            port="5432"
                                            )
            self.cursor = self.connection.cursor()

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS public.requests (
                                                                            name_note varchar(50), 
                                                                            date varchar,
                                                                            note varchar(200) 
                                                                            );"""
                                )

        except (Exception, Error):
            print("Connection Error", Error)
        finally:
            if self.connection:
                self.connection.commit()

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """
        self.pushButtonCreateNote.clicked.connect(self.textEditNoteInfo.clear)  # TODO
      #  self.pushButtonCreateNote.clicked.connect(self.textEditNoteInfo.clearSpans)
        self.pushButtonCreateNote.clicked.connect(self.selectQueryDB)
        self.pushButtonCreateNote.clicked.connect(self.showNoteInfo)
        self.pushButtonCreateNote.clicked.connect(self.openChildWindow)
        self.calendar.clicked.connect(self.textEditNoteInfo.clear)
        self.calendar.clicked.connect(self.selectQueryDB)
        self.calendar.clicked.connect(self.showNoteInfo)
        self.calendar.activated.connect(self.selectQueryDB)
        self.calendar.activated.connect(self.openChildWindow)

    def selectQueryDB(self) -> None:
        """
        Получение данных о заметках из таблицы БД
        :return: None
        """
        self.date = self.calendar.selectedDate()
        self.date_to_DB = self.date.toString('MMMM d, yyyy')

        try:
            query = f"""SELECT 
                            name_note, 
                            date, 
                            note 
                            FROM public.requests 
                            WHERE date='{self.date_to_DB}';"""

            self.cursor.execute(query)
            self.record = self.cursor.fetchone()
        except(Exception, Error):
            print("Query error", Error)

    def showNoteInfo(self) -> None:
        """
         Отображение информации о заметках в нижнем поле с текстом
        :return: None
        """
        if self.record is not None:
            self.textEditNoteInfo.clear()
            for i in range(len(self.record)):
                self.textEditNoteInfo.append(self.record[i])

            self.textEditNoteInfo.append("")
            self.textEditNoteInfo.append("-----------------------")
            self.textEditNoteInfo.append(f"Current date: {time.ctime()}")

        else:
            self.textEditNoteInfo.setText("Note is not created")

    def openChildWindow(self) -> None:
        """
        Вывод дочернего окна с информацией о заметке на выбранную дату, либо для удаления заметки
        :return: None
        """

        child_window = ChildWindow(self)
        child_window.signal_to_main.connect(self.createQueryDB)
        child_window.lineEditNoteDate.setText(self.date_to_DB)
        if self.record is not None:
            note_name = self.record[0]
            note = self.record[2]

            child_window.lineEditNoteName.setText(note_name)
            child_window.textEditNoteText.setText(note)

        else:
            child_window.lineEditNoteName.setText("")
            child_window.textEditNoteText.setText("")

        child_window.exec()

    def createQueryDB(self, signal) -> None:
        """
        Добавление или удаление информации о заметке в БД
        :param signal: информация о заметке, передаваемая дочерним окном
        :return: None
        """
        if signal['name_note'] == "" and signal['note'] == "":
            self.cursor.execute(f"""DELETE FROM public.requests 
                                    WHERE date='{signal["date"]}'
                            ;""")
            self.selectQueryDB()
            self.showNoteInfo()

        else:
            self.cursor.execute(f"""INSERT INTO public.requests(
                                                name_note,
                                                date,
                                                note
                                                               )
                                                values(
                                                '{signal['name_note']}',
                                                '{signal['date']}',
                                                '{signal['note']}'
                                                     )
                            ;""")

            self.selectQueryDB()
            self.showNoteInfo()

        self.connection.commit()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Закрытие подключения к БД при закрытии основного окна
        :param event: событие закрытия окна
        :return: None
        """
        self.cursor.close()
        self.connection.close()

    def paintCell(self) -> None:
        painter = QtGui.QPainter(QtGui.QPaintDevice())

        rect = QtCore.QRect(QtCore.QPoint(5, 5), QtCore.QSize(5, 5))

        date = self.calendar.selectedDate()
        self.calendar.paintCell(self, painter, rect, date)

        painter.setBrush(QtGui.QColor(0, 0, 255, 0))

        painter.setPen(QtGui.QColor(255, 0, 0, 0))
        painter.drawRect(rect)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    win = MainWindow()
    win.show()

    app.exec()

