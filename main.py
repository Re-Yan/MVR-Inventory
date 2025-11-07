from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlRecord
from datetime import datetime
import sys, sqlite3


class search(QWidget):
    def __init__(self, label, buttonLabel, onButtonClick=None, parent=None):
        super().__init__()
        layout = QHBoxLayout()

        self.label = QLabel(label)

        self.resize(400, 250)
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

class tableView(QTableView):
    def __init__(self, model: QSqlTableModel, parent=None):
        super().__init__()

        self.setModel(model)

        self.isSortingEnabled(True)
        print("Custom TableVIew and Model created")
        




class contentWidget(QWidget):
    def __init__(self, model: QSqlTableModel, parent=None):
        super().__init__()

        self.setMaximumWidth(450)

        layout = QVBoxLayout()
    
        self.model = model
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
        
        record = self.model.record()
        record.setValue("sale_date", dateNow)
        record.setValue("part_name", inputText)

        if self.model.insertRecord(-1, record):
            if self.model.submitAll():
                print(f"Recorded Item {inputText} - {dateNow}")
                self.model.select() # Refresh the Model
                self.salesLog.clearInput()
            else:
                print("Failed to submit changes to DB")
        else:
            print("Failed to insert record into model")
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MVR Inventory")   

        # Creating Database Connection
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("salesDatabase.db")

        # ERROR Handling of DB Connection
        if not db.open():
            print("Unable to open database connection")
            sys.exit(1)
        print("DB Connection Successful")

        # Create Model Instance
        self.model = QSqlTableModel(db=db)
        self.model.setTable("sales")
        self.model.select()

        # Creating the actual QtableView Widget
        self.mainWidget = contentWidget(model=self.model)
        self.view = tableView(model=self.model)

        # Layout Arrangement
        main_layout = QHBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(self.mainWidget)
        main_layout.addStretch()
        main_layout.addWidget(self.view)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()