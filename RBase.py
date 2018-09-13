'''
Модуль RBase содержит класс RBase
'''
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QColor

class RBase:
    '''
    Класс RBase содержит функциональность, которая является общей для других классов
    '''
    def add_text_to_text_edit(self, text_edit, message):
        """
        Функция add_text_to_text_edit(text_edit, message) разивает текст по переносу строки и поочередно добавляет его
        к элементу QTextEdit, применяя к каждой строке центрирование текста по центру
        """
        message = message.split('\n')
        text_edit.setText('')
        for line in message:
            text_edit.append(line)
            text_edit.setAlignment(QtCore.Qt.AlignCenter)

    def set_font_to_text_edit(self, text_edit, size, family, bold, italic, strikeout, color):
        """
        Функция set_font_and_color() получает настройки шрифта и цвет текста из базы и применяет их к компоненту QTextEdit
        """
        font = QFont()
        font.setPointSizeF(size)
        font.setFamily(family)
        font.setBold(int(bold))
        font.setItalic(int(italic))
        font.setStrikeOut(int(strikeout))
        text_edit.setFont(font)
        text_edit.setStyleSheet("QTextEdit {background-color:  #00356a}")
        text_edit.setTextColor(QColor(color))

    # Если выделить текст и затем устанавливать цвет, то вылетает с ошибкой.
    # Для этого сначала снимаем выделение с текста
    def deselect_text(self, text_edit):
        '''
        Функция deselect_text(text_edit) снимает выделение с текста в QTextEdit
        :param text_edit:
        :return:
        '''
        cursor = text_edit.textCursor()
        cursor.clearSelection()
        text_edit.setTextCursor(cursor)