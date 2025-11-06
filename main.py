from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton
from datetime import datetime
import sys, sqlite3


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


class contentWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setMaximumWidth(450)

        layout = QVBoxLayout()
    

        self.itemSearch = search(label="Item Search: ", buttonLabel="Search", onButtonClick=self.searchItem)
        self.salesLog = search(label="Sales Log: ", buttonLabel="Enter", onButtonClick=self.logSales)

        layout.addWidget(self.itemSearch)
        layout.addWidget(self.salesLog)

        self.setLayout(layout)

    def searchItem(self):
        inputText = self.itemSearch.getText()
        print(f"searched for item: {inputText}")
        self.itemSearch.clear()
    
    def logSales(self):
        inputText = self.salesLog.getText()
        dateNow = datetime.today().date().isoformat()
        
        if not inputText:
            print("Sales Log Empty. Nothing to write")
            return
        
        try:
            conn = sqlite3.connect("salesDatabase.db")
            cursor = conn.cursor()

            sql_insert = "INSERT INTO sales (sale_date, part_name) VALUES (?, ?)"

            cursor.execute(sql_insert, (dateNow, inputText))

            conn.commit()
            print(f"Added item: {inputText} on {dateNow} in Database")
            self.salesLog.clearInput()
        
        except sqlite3.Error as e:
            print(f"Error connecting to Database: {e}")
        finally:
            if conn:
                conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MVR Inventory")   

        main_layout = QHBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(contentWidget())
        main_layout.addStretch()

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()