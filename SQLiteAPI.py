""" Модуль содержит класс для работы с базой данных """
import sqlite3
import os
from PyQt5.QtWidgets import QMessageBox, QWidget


class DB(QWidget):
    """
    Класс DB содержит содержит набор функций для создани БД SQLite и для работы с ней.
    Также содержит два словаря для заполнения БД данными по-умолчанию.
    """
    def __init__(self):
        """
        Конструктор инициализирует два словаря для сохранения в БД значений по-умолчанию
        """
        super(DB, self).__init__()
        self.db_file = os.path.join(os.getcwd(), "reminder.db")

       # Настройки по-умолчанию для текста
        self.font = {
            "font_id": 1,
            "font_size": 18,
            "font_family": "Sans-serif",
            "font_bold": 1,
            "font_italic": 0,
            "font_underline": 0,
            "font_strikeout": 0,
            "text_color": "#dce9ef"
        }

        # Настройки по-умолчанию общие
        self.settings = {
            "id_setting": 1,
            "main_text": "Здесь Ваш текст",
            "time_out": 60,
            "counter": 0,
            "time_dont_show_after": "21:00",
            "time_start_show_since": "09:00",
            "time_repeat_show_reminder": 1800
        }

    def init_db(self):
        """
        Функция init_db() создает базу данных и заполняет ее значениями по-умолчанию.
        Для этого она использует следующие функции класса DB:
            - create_db() - создает базу в случае ее отсутствия
            - self.check_default_settings() -  проверяет, есть ли в таблице setting запись с ID=1
            - set_default_settings() - если предыдущая функция вернула количество записей 0 -
            заполняет таблицы значениями по-умолчанию.
        """
        self.create_db()
        col_rows = self.check_default_settings()
        if col_rows == 0:
            self.set_default_settings()

    def create_connection(self):
        """
        Функция create_connection() создает базу данных и возращает объект подключения к БД.
        """

        try:
            con = sqlite3.connect(self.db_file)
            con.execute('pragma journal_mode=off')
            # con.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Ошибка подключения к базе данных", str(error), QMessageBox.Ok)
            return error
        return con

    def create_db(self):
        """
        Функция create_db() создает таблицы базы данных
        """
        connection = self.create_connection()
        cursor = connection.cursor()
        sql = """\
        CREATE TABLE IF NOT EXISTS setting (
            id_setting INTEGER PRIMARY KEY AUTOINCREMENT,
            main_text TEXT default "Здесь Ваш текст",
            time_out INTEGER default 60,
            counter INTEGER default 0,
            time_dont_show_after  TEXT default "21:00",
            time_start_show_since  TEXT default "09:00",
            time_repeat_show_reminder INTEGER default 1800
            );
        
        CREATE TABLE IF NOT EXISTS font (
            font_id INTEGER PRIMARY KEY AUTOINCREMENT,
            font_size REAL default 16,
            font_family TEXT default "Sans-serif",
            font_bold TEXT default 0, 
            font_italic  TEXT default 0,
            font_underline TEXT default 0,
            font_strikeout TEXT default 0,
            text_color TEXT default  "#000000"
        );
        """

        try:
            cursor.executescript(sql)
        except sqlite3.DatabaseError as error:
            return self.show_db_error(error)

    def check_default_settings(self):
        """
        Функция check_default_settings() делает запрос к базе данных и проверяет, есть ли в таблице setting
        запись с ID=1
        """
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            sql = "SELECT count(*) FROM setting WHERE id_setting=1"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]
        except sqlite3.DatabaseError as error:
            return self.show_db_error(error)

    def set_default_settings(self):
        """
        Функция set_default_settings() заполняет таблицы значениями по-умолчанию при инициализации приложения
        и при сбросе настроек
        """
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            sql_settings = """INSERT INTO setting (id_setting, main_text, time_out, counter, time_dont_show_after, time_start_show_since, time_repeat_show_reminder) 
                    VALUES (:id_setting, :main_text, :time_out, :counter, :time_dont_show_after, :time_start_show_since, :time_repeat_show_reminder)"""
            sql_font = """INSERT INTO font (font_id, font_size, font_family, font_bold, font_italic, font_underline, font_strikeout, text_color)
                    VALUES (:font_id, :font_size, :font_family, :font_bold, :font_italic, :font_underline, :font_strikeout, :text_color)"""
            cursor.execute(sql_settings, self.settings)
            cursor.execute(sql_font, self.font)
            connection.commit()
        except sqlite3.DatabaseError as error:
            return self.show_db_error(error)

    def reset_to_default_settings(self):
        """
        Функция reset_to_default_settings() возвращает записи в таблицах к значениям по-умолчанию
        """
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            sql_settings = """UPDATE setting SET main_text=:main_text, time_out=:time_out, counter=:counter, 
            time_dont_show_after=:time_dont_show_after,  time_start_show_since=:time_start_show_since, 
            time_repeat_show_reminder=:time_repeat_show_reminder                 
                    WHERE id_setting=:id_setting"""
            sql_font = """UPDATE font SET font_size=:font_size, font_family=:font_family, font_bold=:font_bold, 
                font_italic=:font_italic, font_underline=:font_underline, font_strikeout=:font_strikeout, text_color=:text_color
                    WHERE font_id=:font_id"""
            cursor.execute(sql_settings, self.settings)
            cursor.execute(sql_font, self.font)
            connection.commit()
        except sqlite3.DatabaseError as error:
            return self.show_db_error(error)

    # Получить парамнтры из базы данных
    def get_settings(self):
        """
        Функция get_settings() делает выборку из таблицы setting
        :return:  кортеж - выборка из бд
        """
        try:
            con = self.create_connection()
            cursor = con.cursor()
            sql_settings = "SELECT main_text, time_out, counter, time_dont_show_after, time_start_show_since, " \
                           "time_repeat_show_reminder from setting"
            cursor.execute(sql_settings)
            return cursor.fetchone()
        except sqlite3.DatabaseError as error:
            return self.show_db_error(error)

    # Получить настройки текста из базы данных
    def get_font_and_color_text(self):
        """
        Функция get_font_and_color_text() делает выборку из таблицы setting
        :return:  кортеж - выборка из бд
        """
        con = self.create_connection()
        cursor = con.cursor()
        try:
            sql_settings = "SELECT font_size, font_family, font_bold, font_italic, font_strikeout, text_color from font"
            cursor.execute(sql_settings)
            return cursor.fetchone()
        except sqlite3.DatabaseError as error:
            return self.show_db_error(error)

    # Увеличить или уменьшик счетчик в зависимости от переданного параметра и сохранить в базе данных
    def change_counter(self, counter):
        """
        Функция change_counter() получает обновленное значение счетчика и обновляет значение счетчика в БД.
        :param counter: обновленное значение счетчика
        """
        con = self.create_connection()
        cursor = con.cursor()
        try:
            sql = "UPDATE setting SET counter = ?"
            cursor.execute(sql, (counter,))
            con.commit()
        except sqlite3.DatabaseError as error:
            return self.show_db_error(error)

    def save_settings(self,changed_settings, changed_font_and_color):
        """
        Функция save_settings(changed_settings, changed_font_and_color) обновляет данные в БД
        :param changed_settings:
        :param changed_font_and_color:
        :return: None
        """
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            sql_settings = """UPDATE setting SET main_text=:main_text, time_out=:time_out, 
              time_dont_show_after=:time_dont_show_after,  time_start_show_since=:time_start_show_since, 
              time_repeat_show_reminder=:time_repeat_show_reminder 
               WHERE id_setting=1"""
            sql_font = """UPDATE font SET font_size=:font_size, font_family=:font_family, font_bold=:font_bold,
             font_italic=:font_italic, font_underline=:font_underline, font_strikeout=:font_strikeout, text_color=:text_color
             WHERE font_id=1"""
            cursor.execute(sql_settings, changed_settings)
            cursor.execute(sql_font, changed_font_and_color)
            connection.commit()
        except sqlite3.DatabaseError as error:
            self.show_db_error(error)

    def show_db_error(self, error):
        """
        Функция show_db_error(error) выводит окно с сообщением об ошибке при работе с базой данных
        :param error:
        :return: None
        """
        QMessageBox.critical(self, "Ошибка базы данных", str(error), QMessageBox.Ok)

