import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QHeaderView
from PyQt5.uic import loadUi
import datetime
import firebase_admin
from firebase_admin import db, credentials


# Firebase initialization
credentials_path = "database/credentials.json"
firebase_credentials = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(firebase_credentials, {
    "databaseURL": "https://project-1-c445c-default-rtdb.firebaseio.com/"
})

# functions for pushing and retrieving data from Firebase

#updates log data for a user
def update_log_data(id_num, key, value):      
    db.reference(f"/logData/{id_num}").update({key: value})

#updates access data for a user
def update_access_data(id_num, key, value):
    db.reference(f"/labAccess/{id_num}").update({key: value})

#checks if user has access or not
def check_access_status(id_num):
    access_status = db.reference(f"/labAccess/{id_num}/access").get()
    return access_status

#checks user's affiliation
def check_user_affiliation(id_num):
    affiliation_status = db.reference(f"/labAccess/{id_num}/affiliation").get()
    return str(affiliation_status)


# Login Window Class
class UserLogin(QDialog):
    def __init__(self):
        super(UserLogin, self).__init__()
        loadUi("src/ui/login.ui", self)
        self.setWindowTitle("Login")
        self.accessButton.clicked.connect(self.authenticate_user)

    #authenticating user according to the button clicked
    def authenticate_user(self):
        user_id = self.IDTextBox.text()
        entry_checked = self.in_radio.isChecked()
        exit_checked = self.out_radio.isChecked()
        admin_checked = self.admin_radio.isChecked()
        
        #validating user id
        if user_id.isdigit() and len(user_id) == 9:
            if entry_checked and check_access_status(user_id) == "true":
                self.redLabel.setText("")
                self.greenLabel.setText("Entry Recorded!")
                current_time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                update_log_data(user_id, "datetime", str(current_time))
           
            #exit for valid users
            elif exit_checked and check_access_status(user_id) == "true":
                self.redLabel.setText("")
                self.greenLabel.setText("Exit Recorded!")
                current_time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                update_log_data(user_id, "datetime", str(current_time))

            #admin access for faculty
            elif admin_checked and check_user_affiliation(user_id) == "faculty":
                self.redLabel.setText("")
                admin_view = AdminAccessWindow()
                widget.addWidget(admin_view)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            #handle invalid access
            else:
                self.redLabel.setText("Access Denied")
        
        #handle invalid id formatting
        else:
            self.redLabel.setText("Access Denied")
            self.IDTextBox.clear()


# Admin Window Class
class AdminAccessWindow(QMainWindow):
    def __init__(self):
        super(AdminAccessWindow, self).__init__()
        loadUi("main/admin.ui", self)
        self.setWindowTitle("Admin Access Portal")
        header = self.studentTableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.refresh_data()
        self.IDSearchTextBox.textChanged.connect(self.filter_log_data)
        self.IDSearchTextBox2.textChanged.connect(self.filter_access_data)
        self.refreshTableButton.clicked.connect(self.refresh_data)
        self.suspendAccess.clicked.connect(self.revoke_access)
        self.giveAccess.clicked.connect(self.grant_access)
        self.dateSelect.selectionChanged.connect(self.apply_date_filter)
    
    #loading data from Firebase into tables
    def refresh_data(self):
        log_data = db.reference("/logData").get()
        access_data = db.reference("/labAccess").get()

        self.update_table(self.studentTableView, log_data)
        self.update_table(self.adminTableView, access_data)

    #updating specific tables with provided data
    def update_table(self, table_view, data):
        if data:
            row = 0
            table_view.setRowCount(len(data.items()))
            for key, value in data.items():
                table_view.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
                col = 1
                for k, v in value.items():
                    table_view.setItem(row, col, QtWidgets.QTableWidgetItem(v))
                    col += 1
                row += 1
    
    #filters log data based on search input 
    def filter_log_data(self):
        search_term = self.IDSearchTextBox.text().lower()
        self.filter_table(self.studentTableView, search_term)

    #filters access data based on search input
    def filter_access_data(self):
        search_term = self.IDSearchTextBox2.text().lower()
        self.filter_table(self.adminTableView, search_term)

    #filters rows in a table based on search input
    def filter_table(self, table, search_term):
        if search_term.isnumeric() or not search_term:
            for row in range(table.rowCount()):
                item = table.item(row, 0)
                table.setRowHidden(row, not item.text().lower().startswith(search_term))
    
    #function to grant access to a user
    def grant_access(self):
        selected = self.adminTableView.selectedItems()
        if selected:
            user_id = selected[0].text()
            update_access_data(user_id, "access", "true")
            self.messageLabel.setText("Access Granted")
    
    #function to revoke access to a user
    def revoke_access(self):
        selected = self.adminTableView.selectedItems()
        if selected:
            user_id = selected[0].text()
            update_access_data(user_id, "access", "false")
            self.messageLabel.setText("Access Revoked")
    
    #filter based on a selected date
    def apply_date_filter(self):
        selected_date = self.dateSelect.selectedDate().toString("MM/dd/yyyy")
        all_day_checked = self.allDayRadio.isChecked()
        time_filter = self.timeData.text() if not all_day_checked else None

        self.studentTableView.clearContents()
        self.studentTableView.setRowCount(0)
        self.filter_by_date(selected_date, time_filter)
    
    #filter date by date
    def filter_by_date(self, date_str, time_str=None):
        log_data = db.reference("/logData").get()
        if log_data:
            filtered_rows = [
                (key, value)
                for key, value in log_data.items()
                if value.get("datetime", "").startswith(date_str) and (not time_str or self.is_time_valid(value.get("datetime", ""), time_str))
            ]
            self.populate_table(self.studentTableView, filtered_rows)

    #validates if time in the log is greater than or equal to the filtered time
    def is_time_valid(self, datetime_str, time_str):
        date_part, time_part = datetime_str.split()
        return self.compare_times(time_part.strip(), time_str.strip())
    
    #compare two different times
    def compare_times(self, time1, time2):
        hour1, minute1 = map(int, time1.split(":"))
        hour2, minute2 = map(int, time2.split(":"))
        return hour1 > hour2 or (hour1 == hour2 and minute1 >= minute2)
    
    #populate a table with filtered time
    def populate_table(self, table, data):
        table.setRowCount(len(data))
        for row, (key, value) in enumerate(data):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
            for col, (k, v) in enumerate(value.items(), start=1):
                table.setItem(row, col, QtWidgets.QTableWidgetItem(v))


# Main Application
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login_view = UserLogin()
widget.addWidget(login_view)
widget.show()

try:
    sys.exit(app.exec_())
except Exception as e:
    print(f"Exiting application: {e}")
