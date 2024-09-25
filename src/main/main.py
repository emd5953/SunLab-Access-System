import os
from dotenv import load_dotenv
import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QHeaderView
from PyQt5.uic import loadUi
import datetime
import firebase_admin
from firebase_admin import db, credentials

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase Admin using credentials and database URL from the .env file
cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
firebase_admin.initialize_app(cred, {
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
})


# Push Date and Time to Firebase
def pushDateTime(key, value, idnumber):
    db.reference("/logData/" + str(idnumber)).update({key: value})

# Push Access Data to Firebase
def pushAccessData(key, value, idnumber):
    db.reference("/labAccess/" + str(idnumber)).update({key: value})

# Verify Access from Firebase
def verifyAccess(idnumber):
    access_reference = db.reference("/labAccess/" + str(idnumber) + "/access").get()
    return access_reference

# Check if User is Faculty
def facultyAccess(idnumber):
    access_reference = db.reference("/labAccess/" + str(idnumber) + "/affiliation").get()
    return str(access_reference)

# Login Window Class
class LoginWindow(QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("src/ui/login.ui", self)
        self.setWindowTitle("Login")

        # Connect the access button to the login function
        self.accessButton.clicked.connect(self.loginToAdmin)

    # Function to handle the login logic
    def loginToAdmin(self):
        id_number = self.IDTextBox.text()
        in_radio = self.in_radio.isChecked()
        out_radio = self.out_radio.isChecked()
        admin_radio = self.admin_radio.isChecked()

        if id_number.isdigit() and len(id_number) == 9:
            if in_radio and verifyAccess(id_number) == "true":
                self.redLabel.setText("")
                self.greenLabel.setText("Card Accepted! Marked Entry")
                formatted_datetime = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                pushDateTime("datetime", str(formatted_datetime), id_number)

            elif out_radio and verifyAccess(id_number) == "true":
                self.redLabel.setText("")
                self.greenLabel.setText("Card Accepted! Marked Exit")
                formatted_datetime = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                pushDateTime("datetime", str(formatted_datetime), id_number)

            elif admin_radio and facultyAccess(id_number) == "faculty":
                self.redLabel.setText("")
                adminwindow = AdminWindow()
                widget.addWidget(adminwindow)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            else:
                self.redLabel.setText("Access Denied")

        else:
            self.redLabel.setText("Access Denied")
            self.IDTextBox.clear()

# Admin Window Class
class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi("src/ui/admin.ui", self)
        self.setWindowTitle("Admin Access Portal")
        header = self.studentTableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # Load data when the window opens
        self.loadData()

        # Connect various UI elements to their respective functions
        self.IDSearchTextBox.textChanged.connect(self.search_logData)
        self.IDSearchTextBox2.textChanged.connect(self.search_labAccess)
        self.refreshTableButton.clicked.connect(self.refreshTables)
        self.suspendAccess.clicked.connect(self.revoke_access)
        self.suspendAccess.clicked.connect(self.refreshTables)
        self.giveAccess.clicked.connect(self.give_access)
        self.giveAccess.clicked.connect(self.refreshTables)
        self.dateSelect.selectionChanged.connect(self.filterTable)

    # Load logData and labAccess data into the tables
    def loadData(self):
        data_reference = db.reference("/logData")
        access_reference = db.reference("/labAccess")
        log_data = data_reference.get()
        access_data = access_reference.get()

        if log_data:
            row = 0
            self.studentTableView.setRowCount(len(log_data.items()))
            for key, value in log_data.items():
                self.studentTableView.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
                col = 1
                for k, v in value.items():
                    self.studentTableView.setItem(row, col, QtWidgets.QTableWidgetItem(v))
                    col += 1
                row += 1

        if access_data:
            row = 0
            self.adminTableView.setRowCount(len(access_data.items()))
            for key, value in access_data.items():
                self.adminTableView.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
                col = 1
                for k, v in value.items():
                    self.adminTableView.setItem(row, col, QtWidgets.QTableWidgetItem(v))
                    col += 1
                row += 1

   # Search function for logData table
    def search_logData(self):
        search_term = self.IDSearchTextBox.text().lower()
        if search_term.isnumeric() or not search_term:
            for row in range(self.studentTableView.rowCount()):
               item = self.studentTableView.item(row, 0)  # Get the item in the first column
               if item is not None and item.text().lower().startswith(search_term):
                   self.studentTableView.setRowHidden(row, False)
               else:
                   self.studentTableView.setRowHidden(row, True)

    # Search function for labAccess table
    def search_labAccess(self):
        search_term = self.IDSearchTextBox2.text().lower()
        if search_term.isnumeric() or not search_term:
            for row in range(self.adminTableView.rowCount()):
                item = self.adminTableView.item(row, 0)  # Get the item in the first column
                if item is not None and item.text().lower().startswith(search_term):
                    self.adminTableView.setRowHidden(row, False)
                else:
                    self.adminTableView.setRowHidden(row, True)


    # Refresh the data in the tables
    def refreshTables(self):
        self.studentTableView.clearContents()
        self.adminTableView.clearContents()
        self.loadData()

    # Grant access to selected ID
    def give_access(self):
        selected_items = self.adminTableView.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            selected_col = selected_items[0].column()
            cell_data = self.adminTableView.item(selected_row, selected_col).text()
        pushAccessData("access", "true", cell_data)
        self.messageLabel.setStyleSheet("color: #2ecc71; font-size: 12pt; font-weight: bold;")
        self.messageLabel.setText("Access Granted")

    # Revoke access for selected ID
    def revoke_access(self):
        selected_items = self.adminTableView.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            selected_col = selected_items[0].column()
            cell_data = self.adminTableView.item(selected_row, selected_col).text()
        pushAccessData("access", "false", cell_data)
        self.messageLabel.setStyleSheet("color: #e74c3c; font-size: 12pt; font-weight: bold;")
        self.messageLabel.setText("Access Revoked")

    # Filter table by date and time
    def filterTable(self):
        allDayRadio = self.allDayRadio.isChecked()
        selected_date = self.dateSelect.selectedDate()
        formatted_date = selected_date.toString("MM/dd/yyyy")

        if not allDayRadio:
            time_data = self.timeData.text()
            self.studentTableView.clearContents()
            self.studentTableView.setRowCount(0)
            self.load_filtered_data(formatted_date, time_data)
        else:
            self.studentTableView.clearContents()
            self.studentTableView.setRowCount(0)
            self.load_filtered_data(formatted_date, None)

    # Load filtered data by date and optionally by time
    def load_filtered_data(self, formatted_date, time_data):
        data_reference = db.reference("/logData")
        log_data = data_reference.get()

        if log_data:
            filtered_rows = 0

            for key, value in log_data.items():
                date_item = value.get("datetime")
                if date_item:
                    date_parts, time_parts = date_item.split()
                    date_str = date_parts.strip()
                    time_str = time_parts.strip()
                    if date_str == formatted_date:
                        if not time_data or (time_data and self.is_time_after(time_str, time_data)):
                            filtered_rows += 1

            self.studentTableView.setRowCount(filtered_rows)

            row = 0
            for key, value in log_data.items():
                date_item = value.get("datetime")
                if date_item:
                    date_parts, time_parts = date_item.split()
                    date_str = date_parts.strip()
                    time_str = time_parts.strip()
                    if date_str == formatted_date:
                        if not time_data or (time_data and self.is_time_after(time_str, time_data)):
                            self.studentTableView.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
                            col = 1
                            for k, v in value.items():
                                self.studentTableView.setItem(row, col, QtWidgets.QTableWidgetItem(v))
                                col += 1
                            row += 1

    # Helper function to compare times
    def is_time_after(self, time_str, time_data):
        if not time_data:
            return True

        time_parts = time_str.split(":")
        specified_time_parts = time_data.split(":")

        if len(time_parts) >= 2 and len(specified_time_parts) >= 2:
            time_hour, time_minute = map(int, time_parts[:2])
            specified_hour, specified_minute = map(int, specified_time_parts[:2])

            if time_hour > specified_hour or (time_hour == specified_hour and time_minute >= specified_minute):
                return True

        return False

# Main Application
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    loginwindow = LoginWindow()
    widget.addWidget(loginwindow)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting Application")
