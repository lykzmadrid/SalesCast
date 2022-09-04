import sys
import mysql.connector
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap

companyid = None
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
    def gobackregister(self):
        register = RegisterScreen()
        widget.addWidget(register)
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
            sql2 = "SELECT company_id FROM company_table WHERE username = %s"
            newname = (stringusername,)
            cur.execute(sql, newname)
            result_pass = cur.fetchone()
            cur.execute(sql2, newname)
            result_compid = cur.fetchone()
            newpass = str(result_pass[0])

            if stringpassword == newpass:
                print("Successfully  logged in")
                global companyid
                companyid = str(result_compid[0])
                print(companyid, "company id to sa login")
                self.gotomain()

            else:
                print("Invalid")
class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("MAIN.ui", self)
        self.addprodButton.clicked.connect(self.gotoaddproduct)
        self.addcategButton.clicked.connect(self.gotoaddcategory)
        self.loadproductdata()


    def gotoaddproduct(self):
        APS = AddProductScreen()
        widget2.addWidget(APS)
        widget2.show()
    def gotoaddcategory(self):
        ACS = AddCategoryScreen()
        widget3.addWidget(ACS)
        widget3.show()
    def loadproductdata(self):
        global companyid
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amorsolo31",
                database="php_db"
            )
            mycursor = mydb.cursor()
            sql = "SELECT * FROM product_table WHERE company_id = %s"
            strcomp = (companyid,)
            mycursor.execute(sql, strcomp)

            result = mycursor.fetchall()
            self.productTable.setColumnWidth(0, 250)
            self.productTable.setColumnWidth(1, 100)
            self.productTable.setColumnWidth(2, 350)
            self.productTable.setRowCount(len(result))
            print(companyid, result)
            tablerow = 0
            for row in result:
                print('row:',row)
                self.productTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                self.productTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.productTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                tablerow += 1
            mycursor.close()
            mydb.close()
        except Exception as e:
            print(e)

class AddProductScreen(QDialog):

    def __init__(self):
        super(AddProductScreen, self).__init__()
        loadUi("ADDPROD.ui", self)
        self.loadcategfunction()
        self.clearButton.clicked.connect(self.clearfunction)
        self.confirmButton.clicked.connect(self.addprodfunction)
        self.picButton.clicked.connect(self.addphotofunction)

    def clearfunction(self):
        self.prodnameTB.clear()
        self.sellpriceTB.clear()
        self.quantityTB.clear()

    def addprodfunction(self):
        strProdname = self.prodnameTB.text()
        strSellprice = self.sellpriceTB.text()
        strQuantity = self.quantityTB.text()
        strCateg = self.prodcategCBox.currentText()
        global companyid

        if len(strProdname) == 0 or len(strSellprice) == 0 or len(strQuantity) == 0:
            print("Incomplete selection")
        else:

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amorsolo31",
                database="php_db"
            )
            mycursor = mydb.cursor()
            sql2 = """INSERT INTO product_table (product_name, category, stock, price, company_id) VALUES (%s, %s, %s, %s, %s) """
            input_data = (strProdname, strCateg, strQuantity, strSellprice, companyid)
            mycursor.execute(sql2, input_data)
            mydb.commit()
            mydb.close()
            mycursor.close()

    def loadcategfunction(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Amorsolo31",
            database="php_db"
        )
        mycursor = mydb.cursor()
        sql = "SELECT category FROM category_table WHERE company_id = %s"
        strCompanyid = (companyid,)
        mycursor.execute(sql, strCompanyid)
        CBContents = [item[0] for item in mycursor.fetchall()]
        self.prodcategCBox.addItems(CBContents)
        mydb.close()
        mycursor.close()


    def addphotofunction(self):

        pic = QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'Image files (*.jpg *.gif)')
        imagepixmap = pic[0]
        pixmap = QPixmap(imagepixmap)
        if pixmap != None:
            print("ok may pic na")
        else:
            print("walang pic ha")

class AddCategoryScreen(QDialog):
    def __init__(self):
        super(AddCategoryScreen, self).__init__()
        loadUi("ADDCAT.ui", self)
        self.addcategoryconfirmButton.clicked.connect(self.addcategfunction)
        self.categclearButton.clicked.connect(self.categclearfunction)
        global companyid

    def addcategfunction(self):
        sCategory = self.categoryTBx.text()

        if len(sCategory) == 0:
            print("Please enter a category")
        else:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amorsolo31",
                database="php_db"
            )
            mycursor = mydb.cursor()
            sql = """INSERT INTO category_table (company_id, category) VALUES (%s, %s) """
            input_data = (companyid, sCategory)
            mycursor.execute(sql, input_data)
            mydb.commit()
            mydb.close()
            mycursor.close()
            self.categclearfunction()
    def categclearfunction(self):
        self.categoryTBx.clear()









app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget2 = QtWidgets.QStackedWidget()
widget3 = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.show()
app.exec()
