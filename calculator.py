import sys
from functools import partial

import math

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QGridLayout, QLineEdit, QPushButton, QVBoxLayout
)


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(350,300)

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()

        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()

        buttons = {

            'sin':(0,0),
            'cos':(0,1),
            'tan':(0,2),
            'log':(0,3),
            'del':(0,4),
            '7':(1,0),
            '8':(1,1),
            '9':(1,2),
            '/':(1,3),
            'C':(1,4),
            '4':(2,0),
            '5':(2,1),
            '6':(2,2),
            '*':(2,3),
            '(':(2,4),
            '1':(3,0),
            '2':(3,1),
            '3':(3,2),
            '-':(3,3),
            ')':(3,4),
            '0':(4,0),
            '00':(4,1),
            '.':(4,2),
            '+':(4,3),
            '=':(4,4),
            
        }

        for btn, pos in buttons.items():
            self.buttons[btn] = QPushButton(btn)
            self.buttons[btn].setFixedSize(60,40)
            buttonsLayout.addWidget(self.buttons[btn],pos[0],pos[1])

        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self,text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText('')



class Controller():
    
    def __init__(self, model, view):
        self._view = view
        self._evaluate = model

        self._connectSignals()

    def _backspace(self,sub_exp):
        if self._view.displayText() == ERROR:
            self._view.clearDisplay()
        expression = self._view.displayText()[:-1]
        self._view.setDisplayText(expression)


    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self,sub_exp):

        if self._view.displayText() == ERROR:
            self._view.clearDisplay()
        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)
    
    def _connectSignals(self):
        for txt,btn in self._view.buttons.items():
            if txt not in {'=','C','del'}:
                btn.clicked.connect(partial(self._buildExpression,txt))
        
        self._view.buttons["del"].clicked.connect(self._backspace)
        self._view.buttons["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)

ERROR = "ERROR"

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def log(x):
    return math.log(x)

def evaluateExpression(expression):

        try:
            result = str(eval(expression))
        except Exception:
            result = ERROR
        return result

def main():
    calc = QApplication(sys.argv)
    calc.setStyle('Fusion')
    view = Calculator()
    view.show()

    model = evaluateExpression
    Controller(model,view)
    sys.exit(calc.exec_())

if __name__ == "__main__":
    main()

    