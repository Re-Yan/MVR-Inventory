from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton
from datetime import datetime
import sys


class search(QWidget):
    def __init__(self, label, buttonLabel, onButtonClick=None, parent=None):
        super().__init__()
        layout = QHBoxLayout()

        self.label = QLabel(label)

        self.resize(400, 250)
        self.setWindowTitle("MVR Inventory System")
        self.setContentsMargins(20, 20, 20, 20)

        self.input = QLineEdit(self)
        self.input.returnPressed.connect(onButtonClick)

        self.searchButton = Button(f"{buttonLabel}")
        self.searchButton.clicked.connect(onButtonClick)
        

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.searchButton)
        self.setLayout(layout)

    def clearInput(self):
        self.input.clear()       
    
    def getText(self):
        return self.input.text()

class Button(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVR Inventory")

        centralWidget = QWidget()       
        main_layout = QVBoxLayout()
    

        self.itemSearch = search(label="Item Search: ", buttonLabel="Search", onButtonClick=self.searchItem)
        self.salesLog = search(label="Sales Log: ", buttonLabel="Enter", onButtonClick=self.logSales)

        main_layout.addWidget(self.itemSearch)
        main_layout.addWidget(self.salesLog)

        centralWidget.setLayout(main_layout)
        self.setCentralWidget(centralWidget)

    def searchItem(self):
        inputText = self.itemSearch.getText()
        print(f"searched for item: {inputText}")
        self.itemSearch.clearInput()
    
    def logSales(self):
        inputText = self.salesLog.getText()
        dateNow = datetime.today().date().isoformat()
        print(f"Recoded item: {inputText} on {dateNow}")
        self.salesLog.clearInput()





app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()