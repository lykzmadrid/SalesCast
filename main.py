import sys
import mysql.connector

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap

global companyid
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
                password="4114077lykA.",
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
        global companyid
    def gotomain(self):
        main = MainScreen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def gobackregister(self):
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def loginfunction(self):
        global companyid
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
            strci = cur.fetchone()[0]
            newpass = str(result_pass[0])
            if stringpassword == newpass:
                print("Successfully  logged in")
                companyid = strci
                self.gotomain()
                print(companyid, "loginvar")
            else:
                print("Invalid")
class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("MAIN.ui", self)
        self.addprodButton.clicked.connect(self.gotoaddproduct)
        self.acsButton.clicked.connect(self.gotoaddcateg)
        self.loadproductstable()
        self.loadcategtable()
        self.loadsalestable()


    def gotoaddproduct(self):
        APS = AddProductScreen()
        widget2.addWidget(APS)
        widget2.show()
    def gotoaddcateg(self):
        ACS = AddCategoryScreen()
        widget3.addWidget(ACS)
        widget3.show()

    def loadproductstable(self):
        global companyid
        print(companyid)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Amorsolo31",
            database="php_db"
        )
        cur = mydb.cursor()
        sql = "SELECT product_id, product_photo, product_name, category, stock, price FROM product_table WHERE company_id = %s"
        strci = (companyid,)
        cur.execute(sql, strci)
        rows = cur.fetchall()
        tablerow=0
        self.ProductTable.setRowCount(len(rows))
        for row in rows:
            self.ProductTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ProductTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.ProductTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.ProductTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.ProductTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.ProductTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            tablerow+=1
    def loadcategtable(self):
        global companyid
        print(companyid)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Amorsolo31",
            database="php_db"
        )
        cur = mydb.cursor()
        sql = "SELECT company_id, category FROM category_table WHERE company_id = %s"
        strci = (companyid,)
        cur.execute(sql, strci)
        rows = cur.fetchall()
        tablerow=0
        self.categTable.setRowCount(len(rows))
        for row in rows:
            self.categTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.categTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            tablerow+=1
    def loadsalestable(self):
        global companyid
        print(companyid)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Amorsolo31",
            database="php_db"
        )
        cur = mydb.cursor()
        sql = "SELECT product_table.product_id, product_table.product_photo, product_table.product_name, product_table.category, sales_table.sold_quantity, sales_table.total_sold, sales_table.date FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s;"
        strci = (companyid,)
        cur.execute(sql, strci)
        rows = cur.fetchall()
        tablerow=0
        print(rows)
        self.salesTable.setRowCount(len(rows))
        for row in rows:
            self.salesTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.salesTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.salesTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.salesTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.salesTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.salesTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.salesTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            tablerow+=1

class AddCategoryScreen(QDialog):
    def __init__(self):
        super(AddCategoryScreen, self).__init__()
        loadUi("ADDCAT.ui", self)
        self.addcatconfirm.clicked.connect(self.addcategfunction)
    def addcategfunction(self):
        strCat = self.categTB.text()
        global companyid
        if len(strCat) == 0:
            print("Please enter a valid category name")
        else:
            sqlcon = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amorsolo31",
                database="php_db"
            )
            cur = sqlcon.cursor()
            cur.execute('INSERT INTO category_table(company_id, category) VALUES (%s, %s)', (companyid, strCat))
            sqlcon.commit()
            sqlcon.close()




class AddProductScreen(QDialog):

    def __init__(self):
        super(AddProductScreen, self).__init__()
        loadUi("ADDPROD.ui", self)
        self.loadcategory()
        self.clearButton.clicked.connect(self.clearfunction)
        self.confirmButton.clicked.connect(self.addprodfunction)
        self.picButton.clicked.connect(self.addphotofunction)

    def clearfunction(self):
        self.prodnameTB.clear()
        self.sellpriceTB.clear()
        self.quantityTB.clear()

    def addprodfunction(self):
        try:
            global companyid
            strProdname = self.prodnameTB.text()
            strSellprice = self.sellpriceTB.text()
            strQuantity = self.quantityTB.text()
            strCategory = self.categCB.currentText()

            if len(strProdname) == 0 or len(strSellprice) == 0 or len(strQuantity) == 0:
                print("Incomplete selection")
            else:
                sqlcon = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Amorsolo31",
                    database="php_db"
                )
                cur = sqlcon.cursor()
                cur.execute('INSERT INTO product_table(product_name, category, stock, price, company_id) VALUES (%s, %s, %s, %s, %s)', (strProdname, strCategory, strQuantity, strSellprice, companyid))
                sqlcon.commit()
                sqlcon.close()
        except Exception as e:
            print(e)
    def addphotofunction(self):

        pic = QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'Image files (*.jpg *.png)')

        imagepixmap = pic[0]
        pixmap = QPixmap(imagepixmap)
        print(pic)
        if pixmap != None:
            print("ok")
        else:
            print("pls pic")
    def loadcategory(self):
        try:
            global companyid
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amorsolo31",
                database="php_db"
            )
            cur = mydb.cursor()
            sql = "SELECT category FROM category_table WHERE company_id = %s"
            strci = (companyid,)
            cur.execute(sql, strci)
            categresult = cur.fetchall()
            for row in categresult:
                self.categCB.addItem(str(*row))

        except Exception as e:
            print(e)



app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget2 = QtWidgets.QStackedWidget()
widget3 = QtWidgets.QStackedWidget()
widget.show()
app.exec()
