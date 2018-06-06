"""

created 30.05.2018
"""

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QTableWidget, QCompleter
from PyQt5.Qt import QStringListModel


class Main_window(QWidget):
    def __init__(self):
        super(Main_window, self).__init__()
        layout = QGridLayout()

        line_edit = Line_edit(self)
        table = Table_widget(self)

        self.setLayout(layout)
        self.layout().addWidget(line_edit,1,1,1,1)
        self.layout().addWidget(table,2,1,10,1)
        self.resize(800,600)

class Mycompleter(QCompleter):
    def __init__(self, *args, **kwargs):
        super(Mycompleter, self).__init__(*args, **kwargs)

    def findDelimiter(self, text):
        delimiter = [',', ' ', ';']
        i = self.widget().cursorPosition() - 1
        j = i
        while i < len(text):
            if text[i] in delimiter:
                break
            else:
                i += 1
        while j > 0:
            if text[j] in delimiter:
                j = j + 1
                break
            else:
                j -= 1
        return j, i

    def pathFromIndex(self, QModelIndex):
        path = super(Mycompleter, self).pathFromIndex(QModelIndex)
        text = self.widget().text()
        j, i = self.findDelimiter(text)
        return text[0:j] + path + text[i:]

    def splitPath(self, p_str):
        j, i = self.findDelimiter(p_str)
        text = p_str[j:i]
        if text == "" or text == " ":
            print("returned - ")
            return ['-']
        else:
            return [text]

class Line_edit(QLineEdit):
    def __init__(self, parent):
        super(Line_edit, self).__init__()
        completer = Mycompleter()
        completer.setCompletionMode(3)
        completer.setCaseSensitivity(0)
        completer.setModel(QStringListModel(["hallo", "ich", "werde"]))
        self.setCompleter(completer)


class Table_widget(QTableWidget):
    def __init__(self, parent):
        super(Table_widget, self).__init__()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    exec = Main_window()
    exec.show()
    sys.exit(app.exec_())