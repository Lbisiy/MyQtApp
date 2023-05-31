from PySide6 import QtWidgets, QtCore, QtGui


class ChildWindow(QtWidgets.QDialog):
    """
    Дочернее окно, выпадающее при нажатии двойным кликом на дату либо при нажатии на кнопку 'Note'
    """
    signal_to_main = QtCore.Signal(dict)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация UI
        :return: None
        """
        self.setWindowTitle("Note")
        self.setMinimumSize(300, 300)

        self.lineEditNoteName = QtWidgets.QLineEdit()
        self.lineEditNoteName.setPlaceholderText("Note name")

        self.lineEditNoteDate = QtWidgets.QLineEdit()
        self.lineEditNoteDate.setReadOnly(True)

        self.textEditNoteText = QtWidgets.QTextEdit()
        self.textEditNoteText.setPlaceholderText("Note")

        self.pushButtonDeleteNote = QtWidgets.QPushButton()
        spacerDeleteNoteLeft = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.pushButtonDeleteNote.setText("Delete Note")
        self.pushButtonDeleteNote.setMinimumSize(100, 30)
        spacerDeletNoteRight = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)

        layoutNoteName = QtWidgets.QHBoxLayout()
        layoutNoteName.addWidget(self.lineEditNoteName)
        layoutNoteDate = QtWidgets.QHBoxLayout()
        layoutNoteDate.addWidget(self.lineEditNoteDate)
        layoutNoteText = QtWidgets.QHBoxLayout()
        layoutNoteText.addWidget(self.textEditNoteText)
        layoutDeleteNote = QtWidgets.QHBoxLayout()
        layoutDeleteNote.addItem(spacerDeleteNoteLeft)
        layoutDeleteNote.addWidget(self.pushButtonDeleteNote)
        layoutDeleteNote.addItem(spacerDeletNoteRight)

        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addLayout(layoutNoteName)
        layoutMain.addLayout(layoutNoteDate)
        layoutMain.addLayout(layoutNoteText)
        layoutMain.addLayout(layoutDeleteNote)

        self.setLayout(layoutMain)

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """
        self.pushButtonDeleteNote.clicked.connect(self.deleteNote)

    def deleteNote(self) -> None:
        """
        Очистка формы дочернего окна
        :return: None
        """
        self.lineEditNoteName.clear()
        self.textEditNoteText.clear()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Передача сигнала с информацией, содержащейся в дочернем окне при закрытии дочернего окна
        :param event: закрытие окна
        :return: None
        """
        note_dict = {"name_note": self.lineEditNoteName.text(), "date": self.lineEditNoteDate.text(), "note": self.textEditNoteText.toPlainText()}
        self.signal_to_main.emit(note_dict)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    win = ChildWindow()
    win.show()

    app.exec()
