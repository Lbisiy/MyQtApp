import psycopg2
from psycopg2 import Error


class DbWorker:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.record = None

        self._db_name = "postgres"
        self._user_name = "postgres"
        self._password = "victory"
        self._host_name = "localhost"
        self._port_name = "5432"

        self._table_column1 = "name_note"
        self._table_column2 = "date"
        self._table_column3 = "note"

        self.connectDB()

    def connectDB(self) -> None:
        """
        Подключение к БД
        :return: None
        """
        try:
            self.connection = psycopg2.connect(
                                            database=self._db_name,
                                            user=self._user_name,
                                            password=self._password,
                                            host=self._host_name,
                                            port=self._port_name
                                            )
            self.cursor = self.connection.cursor()
        except (Exception, Error):
            print("Connection Error", Error)

    def createTableDB(self) -> None:
        """
        Создание таблицы в БД
        :return: None
        """
        try:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS public.requests (
                                            {self._table_column1} varchar(50), 
                                            {self._table_column2} varchar,
                                            {self._table_column3} varchar(200) 
                                                                            );"""
                                )
        except (Exception, Error):
            print("Connection Error", Error)
        finally:
            if self.cursor:
                self.connection.commit()

    def readTableDB(self, date_to_DB) -> None:
        """
        Получение данных о заметках из таблицы БД
        :return: None
        """
        try:
            query = f"""SELECT 
                            {self._table_column1}, 
                            {self._table_column2}, 
                            {self._table_column3} 
                            FROM public.requests 
                            WHERE date='{date_to_DB}';"""

            self.cursor.execute(query)
            self.record = self.cursor.fetchone()
        except(Exception, Error):
            print("Query error", Error)

    def deleteTableDB(self, signal) -> None:
        """
        Удаление записи из БД
        :param signal: информация о заметке, передаваемая дочерним окном
        :return: None
        """
        try:
            self.cursor.execute(f"""DELETE FROM public.requests 
                                    WHERE date='{signal[f"{self._table_column2}"]}'
                            ;""")
        except(Exception, Error):
            print("Query error", Error)
        finally:
            if self.cursor:
                self.connection.commit()

    def updateTableDB(self, signal) -> None:
        """
        Добавление записи в БД
        :param signal: информация о заметке, передаваемая дочерним окном
        :return: None
        """
        try:
            self.cursor.execute(f"""INSERT INTO public.requests(
                                            {self._table_column1}, 
                                            {self._table_column2}, 
                                            {self._table_column3}
                                                               )
                                            values(
                                            f'{signal[f"{self._table_column1}"]}',
                                            '{signal[f"{self._table_column2}"]}',
                                            '{signal[f"{self._table_column3}"]}'
                                                    )
                            ;""")
        except (Exception, Error):
            print("Connection Error", Error)
        finally:
            if self.cursor:
                self.connection.commit()

    def close_connection(self) -> None:
        """
        Закрытие подключения к БД
        :return: None
        """
        self.cursor.close()
        self.connection.close()
