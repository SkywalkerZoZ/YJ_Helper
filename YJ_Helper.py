import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from pathlib import Path
import recognizer
import calculater


class YJ_Helper(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.text_input = QLineEdit(self)
        self.recognize_button = QPushButton('recognize', self)
        self.recognize_button.clicked.connect(self.recognizeButtonClicked)

        self.text_output = QTextEdit(self)
        self.text_output.setReadOnly(True)

        self.calculate_button = QPushButton('calculate', self)
        self.calculate_button.clicked.connect(self.calculateButtonClicked)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        hbox.addWidget(self.text_input)
        hbox.addWidget(self.recognize_button)
        hbox.addWidget(self.calculate_button)

        vbox.addLayout(hbox)
        vbox.addWidget(self.text_output)

        self.setLayout(vbox)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def recognizeButtonClicked(self):
        screenshot=recognizer.get_screenshot()
        chars=recognizer.recognize_cards(screenshot)
        if len(chars)==0:
            self.text_output.setHtml('<font color="red">no target recognized</font>')
            return
        display_chars=' '.join(chars)
        # print(display_chars)
        self.text_input.setText(display_chars)
        self.text_output.clear()


    def calculateButtonClicked(self):
        display_chars = self.text_input.text().strip('\n ').split(' ')
        numbers=[]
        try:
            recognizer.char2number(display_chars,numbers)
        except KeyError as e:
            self.text_output.setHtml('<font color="red">invalid input</font>')
            return
        # print(numbers)
        best_solution_str,solution_str=calculater.match(numbers)
        self.text_output.setText(best_solution_str+solution_str)
        # print(best_solution_str+'\n'+solution_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YJ_Helper()
    # theme_file=Path("py_dracula_dark.qss")
    # if theme_file.exists():
    #     with theme_file.open() as theme_file:
    #         app.setStyleSheet(theme_file.read())
    # else:
    #     print(f"The theme file '{theme_file}' does not exist.")
    icon = QIcon('./img/zcp.ico')
    app.setWindowIcon(icon)
    ex.setWindowTitle('YJ Helper')
    ex.show()
    sys.exit(app.exec())
