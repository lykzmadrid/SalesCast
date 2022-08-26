import sys
import mysql.connector
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QMainWindow


class WelcomeScreen(QDialog):

    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("WELCOME.ui", self)
        self.loginButton.clicked.connect(self.gotologin)
        self.registerButton.clicked.connect(self.gotoregister)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoregister(self):
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class RegisterScreen(QDialog):
    def __init__(self):
        super(RegisterScreen, self).__init__()
        loadUi("REGISTER.ui", self)
        self.registerButton2.clicked.connect(self.registerfunction)
        self.alreadyhaveButton.clicked.connect(self.gobacklogin)

    def registerfunction(self):
        stringFN = self.textboxFN.text()
        stringCN = self.textboxCN.text()
        stringEA = self.textboxEA.text()
        stringU = self.textboxU.text()
        stringP = self.textboxP.text()

        if len(stringFN) == 0 or len(stringCN) == 0 or len(stringEA) == 0 or len(stringU) == 0 or len(stringP) == 0:
            print("Please fill out all the necessary details")
        else:
            sqlcon = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amorsolo31",
                database="php_db"
            )
            cur = sqlcon.cursor()
            cur.execute(
                'INSERT INTO company_table(full_name, company_name, email, username, password) VALUES (%s, %s, %s, %s, %s)',
                (stringFN, stringCN, stringEA, stringU, stringP))
            sqlcon.commit()
            sqlcon.close()

    def gobacklogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("LOGIN.ui", self)
        self.loginbutton2.clicked.connect(self.loginfunction)
        self.donthaveButton.clicked.connect(self.gobackregister)

    def gotomain(self):
        main = MainScreen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def loginfunction(self):
        stringusername = self.usernameTextbox.text()
        stringpassword = self.passwordTextbox.text()

        if len(stringusername) == 0 or len(stringpassword) == 0:
            print("The username/password is empty")
        else:
            sqlcon = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amorsolo31",
                database="php_db"
            )
            cur = sqlcon.cursor()
            sql = "SELECT password FROM company_table WHERE username = %s"
            newname = (stringusername,)
            cur.execute(sql, newname)
            result_pass = cur.fetchone()
            newpass = str(result_pass[0])
            if stringpassword == newpass:
                print("Successfully  logged in")
            else:
                print("Invalid")

    def gobackregister(self):
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()


app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.show()
app.exec()
