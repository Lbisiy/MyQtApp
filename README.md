### Приложение для работы с заметками

### DEV-PYQT. Разработка оконных приложений Python c использованием Qt


#### Описание функционала:

1. Виджет-календарь с отображением добавленных заметок в таблице
2. Однократное нажатие на дату календаря - отображение привязанной к дате заметки
3. Двукратное нажатие - открытие дочернего окна с функцией добавления/удаления заметки
4. Нажатие на кнопку "Note" - открытие дочернего окна с функцией добавления/удаления заметки
4. Заметки хранятся в базе данных. За работу с базой данных отвечает

Состав пакета:
notepad.py - запуск приложения
main_window.py - главный виджет
child_window - дочернее окно для добавления/удаления заметки
calendar - виджит календарь
db_utility.py - утилита работы с БД
