

from prophet import Prophet
n = Prophet(stan_backend='CMDSTANPY')
n.stan_backend.get_type()
import cmdstanpy
import sys
import mysql.connector
import pandas as pd
import numpy as np
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from math import sqrt
import smtplib
import math, random
from PyQt5.QtWidgets import QMessageBox
from statsmodels.tools.eval_measures import rmse
import ICONS_rc
from datetime import datetime
from fpdf import FPDF
from PyQt5.QtCore import QDate
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, mean_absolute_error
from prophet import Prophet
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QMainWindow, QFileDialog, QLabel, QDateEdit
from PyQt5.QtGui import QPixmap
from datetime import date
global companyid, SortVar, binarydata, pDeleteID, sDeleteID, SelectedPID, SelectedSID, SelectedRID, SelectedOID, SelectedNID, SelectedNID2, SelectedOID, SelectedDID
companyid = None
SortVar = 0
binarydata = None
pDeleteID = None
sDeleteID = None
rdeleteID = None
odeleteID = None
SelectedPID = None
SelectedSID = None
SelectedRID = None
SelectedNID = None
SelectedNID2 = None
SelectedOID = None
arrayvar = None
SelectedDID = None
class PDF3(FPDF):
    def header(self):
        # Logo
        global name
        #self.image('fox_face.png', 10, 8, 25)
        # font
        self.set_font('helvetica', 'B', 12)
        # Padding
        # Title
        self.cell(30, 8, 'SALESCAST GENERATE REFUND ORDER FOR ' + name, ln=1, align='L')
        # Line break
        today = date.today()
        d2 = today.strftime("%B %d, %Y")
        d2 = str(d2)
        self.cell(30,8,'Date: ' + d2, ln=1,align='L')

        self.ln(20)

    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # set font
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def create_table(self, table_data, title='', data_size=10, title_size=12, align_data='L', align_header='L',
                     cell_width='even', x_start='x_default', emphasize_data=[], emphasize_style=None,
                     emphasize_color=(0, 0, 0)):

        default_style = self.font_style
        if emphasize_style == None:
            emphasize_style = default_style

        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.epw / len(data[
                                               0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])):  # for every row
                    longest = 0
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4)  # add 4 for padding
                col_width = col_widths

                ### compare columns

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        # Convert dict to lol
        # Why? because i built it with lol first and added dict func after
        # Is there performance differences?
        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.font_size * 2.5

        col_width = get_col_widths()
        self.set_font(size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else:  # need to multiply cell width by number of cells to get table width
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from pdf width and divide by 2 (margins)
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than pdf width

            center_table = margin_width / 2  # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.set_x(self.l_margin)

        # TABLE CREATION #

        # add title
        if title != '':
            self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
            self.ln(line_height)  # move cursor back to the left margin

        self.set_font(size=data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if not isinstance(col_width, list):
            if x_start:
                self.set_x(x_start)
            for datum in header:
                self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3,
                                max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height)  # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left, y1, x_right, y1)
            self.line(x_left, y2, x_right, y2)

            for row in data:
                if x_start:  # not sure if I need this
                    self.set_x(x_start)
                for datum in row:
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)
                        self.set_text_color(0, 0, 0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)  # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height)  # move cursor back to the left margin

        else:
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3,
                                max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height)  # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left, y1, x_right, y1)
            self.line(x_left, y2, x_right, y2)

            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)
                        self.set_text_color(0, 0, 0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)  # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height)  # move cursor back to the left margin
        y3 = self.get_y()
        self.line(x_left, y3, x_right, y3)

class PDF2(FPDF):
    def header(self):
        # Logo
        global name
        #self.image('fox_face.png', 10, 8, 25)
        # font
        self.set_font('helvetica', 'B', 12)
        # Padding
        # Title
        self.cell(30, 8, 'SALESCAST GENERATE ORDER REPORT FOR ' + name, ln=1, align='L')
        # Line break
        today = date.today()
        d2 = today.strftime("%B %d, %Y")
        d2 = str(d2)
        self.cell(30,8,'Date: ' + d2, ln=1,align='L')

        self.ln(20)

    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # set font
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def create_table(self, table_data, title='', data_size=10, title_size=12, align_data='L', align_header='L',
                     cell_width='even', x_start='x_default', emphasize_data=[], emphasize_style=None,
                     emphasize_color=(0, 0, 0)):
        """
        table_data:
                    list of lists with first element being list of headers
        title:
                    (Optional) title of table (optional)
        data_size:
                    the font size of table data
        title_size:
                    the font size fo the title of the table
        align_data:
                    align table data
                    L = left align
                    C = center align
                    R = right align
        align_header:
                    align table data
                    L = left align
                    C = center align
                    R = right align
        cell_width:
                    even: evenly distribute cell/column width
                    uneven: base cell size on lenght of cell/column items
                    int: int value for width of each cell/column
                    list of ints: list equal to number of columns with the widht of each cell / column
        x_start:
                    where the left edge of table should start
        emphasize_data:
                    which data elements are to be emphasized - pass as list
                    emphasize_style: the font style you want emphaized data to take
                    emphasize_color: emphasize color (if other than black)

        """
        default_style = self.font_style
        if emphasize_style == None:
            emphasize_style = default_style

        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.epw / len(data[
                                               0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])):  # for every row
                    longest = 0
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4)  # add 4 for padding
                col_width = col_widths

                ### compare columns

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        # Convert dict to lol
        # Why? because i built it with lol first and added dict func after
        # Is there performance differences?
        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.font_size * 2.5

        col_width = get_col_widths()
        self.set_font(size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else:  # need to multiply cell width by number of cells to get table width
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from pdf width and divide by 2 (margins)
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than pdf width

            center_table = margin_width / 2  # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.set_x(self.l_margin)

        # TABLE CREATION #

        # add title
        if title != '':
            self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
            self.ln(line_height)  # move cursor back to the left margin

        self.set_font(size=data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if not isinstance(col_width, list):
            if x_start:
                self.set_x(x_start)
            for datum in header:
                self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3,
                                max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height)  # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left, y1, x_right, y1)
            self.line(x_left, y2, x_right, y2)

            for row in data:
                if x_start:  # not sure if I need this
                    self.set_x(x_start)
                for datum in row:
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)
                        self.set_text_color(0, 0, 0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)  # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height)  # move cursor back to the left margin

        else:
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3,
                                max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height)  # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left, y1, x_right, y1)
            self.line(x_left, y2, x_right, y2)

            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)
                        self.set_text_color(0, 0, 0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)  # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height)  # move cursor back to the left margin
        y3 = self.get_y()
        self.line(x_left, y3, x_right, y3)
class PDF(FPDF):
    def header(self):
        global companyname, pdfpname


        today = date.today()
        d2 = today.strftime("%B %d, %Y")
        d2 = str(d2)
        # Logo
        # self.image('fox_face.png', 10, 8, 25)
        # font
        self.set_font('Times', 'B', size=10)
        # Padding
        # Title
        company_name = companyname
        self.cell(30, 8, 'SalesCast Report for ' + company_name, align='L')
        # Line break
        current_date = d2
        self.cell(0, 8, 'Date: ' + current_date, ln=1, align='R')
        product_name2 = "Coke 8oz"
        self.cell(30, 8, 'Product Name: ' + product_name2, ln=1, align='L')
        self.ln(20)



    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # set font
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def create_table(self, table_data, title='', data_size=10, title_size=12, align_data='L', align_header='L',
                     cell_width='even', x_start='x_default', emphasize_data=[], emphasize_style=None,
                     emphasize_color=(0, 0, 0)):

        default_style = self.font_style
        if emphasize_style == None:
            emphasize_style = default_style

        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.epw / len(data[
                                               0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])):  # for every row
                    longest = 0
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4)  # add 4 for padding
                col_width = col_widths

                ### compare columns

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        # Convert dict to lol
        # Why? because i built it with lol first and added dict func after
        # Is there performance differences?
        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.font_size * 2.5

        col_width = get_col_widths()
        self.set_font(size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else:  # need to multiply cell width by number of cells to get table width
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from pdf width and divide by 2 (margins)
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than pdf width

            center_table = margin_width / 2  # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.set_x(self.l_margin)

        # TABLE CREATION #

        # add title
        if title != '':
            self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
            self.ln(line_height)  # move cursor back to the left margin

        self.set_font(size=data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if not isinstance(col_width, list):
            if x_start:
                self.set_x(x_start)
            for datum in header:
                self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3,
                                max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height)  # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left, y1, x_right, y1)
            self.line(x_left, y2, x_right, y2)

            for row in data:
                if x_start:  # not sure if I need this
                    self.set_x(x_start)
                for datum in row:
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)
                        self.set_text_color(0, 0, 0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)  # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height)  # move cursor back to the left margin

        else:
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3,
                                max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height)  # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left, y1, x_right, y1)
            self.line(x_left, y2, x_right, y2)

            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)
                        self.set_text_color(0, 0, 0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3,
                                        max_line_height=self.font_size)  # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height)  # move cursor back to the left margin
        y3 = self.get_y()
        self.line(x_left, y3, x_right, y3)
class WelcomeScreen(QDialog):

    def __init__(self):
        try:
            super(WelcomeScreen, self).__init__()
            loadUi("WELCOME.ui", self)
            self.loginButton.clicked.connect(self.gotologin)
            self.registerButton.clicked.connect(self.gotoregister)
        except Exception as e:
            print(e)

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
        #self.ADButton.clicked.connect(self.attachdatasetfunction)

    def attachdatasetfunction(self):
        try:
            csv = QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'CSV files (*.csv)')

            filename = csv[0]
            print(csv, "ito yung csv")
            print(filename, "ito yung filename")
            scsv = str(filename)

            train_size = int(len(csv) * .80)
            train, test = csv[0:train_size], csv[train_size:len(csv)]
            df = train
            csvread2 = pd.read_csv(scsv)
            csvread2.dropna(inplace=True)
            csvread2.reset_index(drop=True, inplace=True)
            print(csvread2)
            with open(filename, 'rb', encoding='utf-8') as file:
                csvread3 = file.read()
        except Exception as e:
            print(e)

    def registerfunction(self):

        stringFN = self.textboxFN.text()
        stringCN = self.textboxCN.text()
        stringEA = self.textboxEA.text()
        stringU = self.textboxU.text()
        stringP = self.textboxP.text()
        try:
            if len(stringFN) == 0 or len(stringCN) == 0 or len(stringEA) == 0 or len(stringU) == 0 or len(stringP) == 0:
                print("Please fill out all the necessary details")
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Critical)
                msgbox.setText("Please complete all the fields!")
                msgbox.setWindowTitle("Error!")
                msgbox.exec_()
            else:
                sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur = sqlcon.cursor()
                cur.execute(
                    'INSERT INTO company_table(full_name, company_name, email, username, password) VALUES (%s, %s, %s, %s, %s)',
                    (stringFN, stringCN, stringEA, stringU, stringP))
                sqlcon.commit()
                sqlcon.close()
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setText("Account Created!")
                msgbox.setWindowTitle("Success!")
                msgbox.exec_()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Please complete all the fields!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
    def gobacklogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("LOGIN.ui", self)
        self.send_otp.clicked.connect(self.generateOTP)
        self.loginbutton2.clicked.connect(self.loginfunction)
        self.donthaveButton.clicked.connect(self.gobackregister)
        global companyid
    def generateOTP(self):
        global OTP
        digits = "0123456789"
        OTP = ""

        for i in range(4):
            OTP += digits[math.floor(random.random()* 10)]
        self.sendOTP()

    def sendOTP(self):
        try:
            global OTP, stringusername
            print(OTP, "Eto yung OTP")
            otps = self.otpTextbox.text()
            stringusername = self.usernameTextbox.text()
            sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = sqlcon.cursor()
            sql= "SELECT email FROM company_table WHERE username = %s"
            email = (stringusername,)
            cur.execute(sql, email)
            newemail = cur.fetchone()[0]
            stremail = str(newemail)

            sender_email = "sales.cast00@gmail.com"
            sender_password = "uoowwijobxdigiiy"
            print(stremail)
            rec_email = stremail
            message = "Login has been attempted, your OTP is", OTP
            message = str(message)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            print("login success")
            server.sendmail(sender_email, rec_email, message)
            print("Email has been sent to: ", rec_email)
            server.close()
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("OTP has been sent to your email!")
            msgbox.setWindowTitle("Sent!")
            msgbox.exec_()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("username does not exist!")
            msgbox.setWindowTitle("Not found!")
            msgbox.exec_()
            print(e)



    def gotomain(self):
        main = MainScreen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def gobackregister(self):
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def loginfunction(self):
        global companyid, OTP
        try:
            stringusername = self.usernameTextbox.text()
            stringpassword = self.passwordTextbox.text()
            otps = self.otpTextbox.text()
            if len(stringusername) == 0 or len(stringpassword) == 0 or len(otps) == 0:
                print("The username/password/OTP is empty")
            else:
                sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur = sqlcon.cursor()
                sql = "SELECT password FROM company_table WHERE username = %s"
                sql2 = "SELECT company_id FROM company_table WHERE username = %s"
                sql3 = "SELECT email FROM company_table WHERE username = %s"
                newname = (stringusername,)
                cur.execute(sql, newname)
                result_pass = cur.fetchone()
                cur.execute(sql2, newname)

                strci = cur.fetchone()[0]
                newpass = str(result_pass[0])

                if stringpassword == newpass and str(OTP) == str(self.otpTextbox.text()):
                    print("Successfully  logged in")
                    self.usernameTextbox.clear()
                    self.passwordTextbox.clear()
                    self.otpTextbox.clear()
                    companyid = strci
                    self.gotomain()
                    print(companyid, "loginvar")

                else:
                    self.passwordTextbox.clear()
                    msgbox = QMessageBox()
                    msgbox.setIcon(QMessageBox.Critical)
                    msgbox.setText("Username, password or OTP do not match!")
                    msgbox.setWindowTitle("Error!")
                    msgbox.exec_()
                    print("Wrong username/password")

        except Exception as e:
            print(e)
class MainScreen(QDialog):
    def __init__(self):
        try:

            super(MainScreen, self).__init__()
            loadUi("MAIN.ui", self)
            self.addprodButton.clicked.connect(self.gotoaddproduct)
            self.acsButton.clicked.connect(self.gotoaddcateg)
            self.addsalesButton.clicked.connect(self.gotoaddsales)
            self.changecsv.clicked.connect(self.addcsv)
            self.runbutton.clicked.connect(self.processcsv)
            self.ProductTable.clicked.connect(self.highlightproductdeletefunction)
            self.salesTable.clicked.connect(self.highlightsalesdeletefunction)
            self.loadproductstable()
            self.pDeleteButton.clicked.connect(self.productdeletefunction)
            self.sDeleteButton.clicked.connect(self.salesdeletefunction)
            self.fclearbutton.clicked.connect(self.forecastclearfunction)
          #  self.loadcategtable()
            self.loaddashboard()
            self.loaddashboardtable()
            self.loadsalestable()
            self.confirmreplace.clicked.connect(self.replacecsvfunction)
            #self.loadcsvfromdb()
            self.stb.textChanged.connect(self.searchfunction)
            self.ctcb.currentTextChanged.connect(self.searchfunction2)
            self.selbutton.clicked.connect(self.selfunction)
            self.productstextbox.textChanged.connect(self.productsearchfunction)
            self.salestextbox.textChanged.connect(self.salessearchfunction)
            self.RDPbutton.clicked.connect(self.gotorundynamicpricing)
            self.sortbutton.clicked.connect(self.gotosortsales)
            self.pEditButton.clicked.connect(self.gotoproductedit)
            self.sEditButton.clicked.connect(self.gotosalesedit)
            self.sortcheck.stateChanged.connect(self.sortcheckfunction)
            self.Exportsalesbutton.clicked.connect(self.gotoexportsales)
            self.refundTable.clicked.connect(self.highlightrefunddeletefunction)
            self.orderTable.clicked.connect(self.highlightorderdeletefunction)
            self.rDeleteButton.clicked.connect(self.refunddeletefunction)
            self.oDeleteButton.clicked.connect(self.orderdeletefunction)
            self.loadrefundTable()
            self.loadorderTable()
            self.loaddefectTable()
            self.refundtextbox.textChanged.connect(self.refundsearchfunction)
            #self.editrefundbutton.clicked.connect(self.gotoeditrefundscreen)
            #self.editorderBTN.clicked.connect(self.ordereditfunction)
            self.printbtn.clicked.connect(self.printfunction)
            self.VAButton.clicked.connect(self.gotoviewaccuracy)
            self.logout.clicked.connect(self.gotowelcomescreen)
            self.notifbutt.clicked.connect(self.gotonotifscreen)
            self.tabw.currentChanged.connect(self.refresh)
            #self.addreturnbtn.clicked.connect(self.gotoaddrefund)
            self.dataload()
            self.userbutt.clicked.connect(self.gotouseredit)
            self.purchase_order.clicked.connect(self.exportprintPO)

            self.ORbtn.clicked.connect(self.orderreceivedfunction)
            self.addorder_btn.clicked.connect(self.gotoaddorder)
            self.showpredictionrange()
            self.predBTN.clicked.connect(self.updatedpredRange)
            self.transferBTN.clicked.connect(self.transferOrder)
            self.ref_form_2.clicked.connect(self.generaterefundform)
            self.addDefectBTN.clicked.connect(self.deforderfunc)
            self.reb.clicked.connect(self.gotonewrefund)
            self.RFBTN.clicked.connect(self.refundcompleted)
            self.defectTable.clicked.connect(self.highlightdefectfunction)
        except Exception as e:
            print(e)
    def refundcompleted(self):
        try:
            stat = "Completed"
            global companyid, SelectedDID
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port=21290
            )
            cur = mydb.cursor()
            sql = "UPDATE defective_table SET status = %s WHERE company_id = %s AND defective_id = %s"
            strci = (stat, companyid, SelectedDID)
            cur.execute(sql, strci)
            mydb.commit()
            mydb.close()
            self.loaddefectTable()
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Items received!")
            msgbox.setWindowTitle("Success!")
            msgbox.exec_()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Error! Please check console for more info")
            msgbox.setWindowTitle("ERROR!")
            msgbox.exec_()
            print(e)
    def gotonewrefund(self):
        NRS = NewRefundScreen()
        widget16.addWidget(NRS)
        widget16.show()
    def deforderfunc(self):
        global companyid, SelectedOID
        try:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            cur2 = mydb.cursor()
            cur3 = mydb.cursor()
            cur4 = mydb.cursor()
            cur5 = mydb.cursor()
            cur6 = mydb.cursor()
            cur7 = mydb.cursor()


            sql2 = "SELECT product_id FROM order_table WHERE company_id = %s AND order_id = %s"
            strci2 = (companyid, SelectedOID)
            cur2.execute(sql2, strci2)
            prodid = cur2.fetchone()[0]

            sql3 = "SELECT price FROM product_table WHERE company_id = %s AND product_id = %s"
            strci3 = (companyid, prodid)
            cur3.execute(sql3, strci3)
            baseprice = cur3.fetchone()[0]
            basepricex = float(baseprice)
            sql4 = "SELECT stock FROM product_table WHERE company_id = %s AND product_id = %s"
            strci4 = (companyid, prodid)
            cur4.execute(sql4, strci4)
            stock = cur4.fetchone()[0]
            stockx = float(stock)
            defquan = float(self.orderbox_2.text())

            sql5 = "SELECT order_quantity FROM order_table WHERE company_id = %s AND order_id = %s"
            strci5 = (companyid, SelectedOID)
            cur5.execute(sql5, strci5)
            orquan = cur5.fetchone()[0]
            orquanx = float(orquan)


            deftotal = defquan * basepricex
            if defquan == 0:
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Critical)
                msgbox.setText("You have not inputted any amount on defective items!")
                msgbox.setWindowTitle("Not found!")
                msgbox.exec_()
            else:
                if defquan <= orquanx:
                    defdesc = "Defective"
                    cur7.execute(
                        'INSERT INTO defective_table(company_id, order_id, product_id, base_price, def_quantity, def_total, def_desc) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (companyid, SelectedOID, prodid, baseprice, str(defquan), deftotal, defdesc))

                    sql6 = "UPDATE order_table SET order_defective = %s WHERE company_id = %s AND order_id = %s;"
                    strci6 = (str(defquan), companyid, SelectedOID)
                    cur6.execute(sql6, strci6)

                    mydb.commit()
                    mydb.close()
                else:
                    msgbox = QMessageBox()
                    msgbox.setIcon(QMessageBox.Critical)
                    msgbox.setText("Defective items is higher than order quantity!")
                    msgbox.setWindowTitle("Not found!")
                    msgbox.exec_()
            self.loadorderTable()
            self.loaddefectTable()
            self.addDefectBTN.setEnabled(False)
            self.orderbox_2.setEnabled(False)
        except Exception as e:
            print(e)
    def generaterefundform(self):
        try:
            print("Test1")
            global companyid, name
            status = 'Pending'
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT product_id FROM defective_table WHERE company_id = %s AND status = %s"
            strci = (companyid, status)
            cur.execute(sql, strci)
            xnop = cur.fetchall()
            xnopt = [i[0] for i in xnop]
            nopt = []
            print("Test2")
            cur7 = mydb.cursor()
            for y in xnopt:
                sql7 = "SELECT product_name FROM product_table WHERE company_id = %s AND product_id = %s"
                strci7 = (companyid, y)
                cur7.execute(sql7, strci7)
                nop = cur7.fetchone()[0]
                nopt.append(nop)
            print("Test3")
            cur2 = mydb.cursor()
            sql2 = "SELECT order_id FROM defective_table WHERE company_id = %s AND status = %s;"
            strci2 = (companyid, status)
            cur2.execute(sql2, strci2)
            oid = cur2.fetchall()
            oidt = [i[0] for i in oid]
            print("oidt", oidt)
            aopd = []
            aordx = []
            for x in oidt:

                cur3 = mydb.cursor()
                sql3 = "SELECT order_placedate FROM order_table WHERE company_id = %s AND order_id = %s;"
                strci3 = (companyid, x)
                cur3.execute(sql3, strci3)
                opd = str(cur3.fetchone()[0])
                aopd.append(opd)

                cur4 = mydb.cursor()
                sql4 = "SELECT order_receivedate FROM order_table WHERE company_id = %s AND order_id = %s;"
                strci4 = (companyid, x)
                cur4.execute(sql4, strci4)
                ordx = str(cur4.fetchone()[0])
                aordx.append(ordx)
            print("aopd, aordx", aopd, aordx)
            cur5 = mydb.cursor()
            sql5 = "SELECT def_quantity FROM defective_table WHERE company_id = %s AND status = %s;"
            strci5 = (companyid, status)
            cur5.execute(sql5, strci5)
            qty = cur5.fetchall()
            qtyt = [i[0] for i in qty]
            qtytx = []
            for c in qtyt:
                qtytx.append(str(c))

            print("qtyt", qtyt)
            cur6 = mydb.cursor()
            sql6 = "SELECT def_desc FROM defective_table WHERE company_id = %s AND status = %s;"
            strci6 = (companyid, status)
            cur6.execute(sql6, strci6)
            dcn = cur6.fetchall()
            dcnt = [i[0] for i in dcn]



            Purchase_Name = nopt
            Order_Place_Date = aopd
            Order_Receive_Date = aordx
            Quantity = qtytx
            Description = dcnt
            name = "Aidan Ali"
            pdf = PDF3()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Times", size=10)
            data_as_dict = {"Product Name": Purchase_Name, "Order Place Date": Order_Place_Date,
                            "Order Receive Date": Order_Receive_Date, "Quantity": Quantity, "Description": Description}
            pdf.create_table(table_data=data_as_dict, title='Table of Items', cell_width='even')
            pdf.ln()


            pdf.set_font("Times", size=12, style='U')
            pdf.cell(180, 8, name, ln=1, align='R')
            pdf.set_font("Times", size=10)
            pdf.cell(180, 8, 'Sign here ', ln=1, align='R')
            pdf.output('refund_order.pdf')
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Refund Form has been Generated!")
            msgbox.setWindowTitle("Sent!")
            msgbox.exec_()
        except Exception as e:
            print(e)
    def orderreceivedfunction(self):
        global companyid, SelectedOID
        rstr = "Received"
        try:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "UPDATE order_table SET order_status = %s WHERE company_id = %s AND order_id = %s;"
            strci = (rstr, companyid, SelectedOID)
            cur.execute(sql, strci)
            '''
            today = date.today()
            d2 = today.strftime("%Y-%m-%d")
            cur2 = mydb.cursor()
            sql2 = "UPDATE order_table SET order_receivedate = %s WHERE company_id = %s AND order_id = %s;"
            strci2 = (d2, companyid, SelectedOID)
            cur2.execute(sql2, strci2)

            cur3 = mydb.cursor()
            sql3 = "SELECT order_quantity FROM order_table WHERE company_id = %s AND order_id = %s;"
            strci3 = (companyid, SelectedOID)
            cur3.execute(sql3, strci3)
            istock = cur3.fetchone()[0]

            cur5 = mydb.cursor()
            sql5 = "SELECT product_id FROM order_table WHERE company_id = %s AND order_id = %s;"
            strci5 = (companyid, SelectedOID)
            cur5.execute(sql5, strci5)
            proid = cur5.fetchone()[0]


            cur4 = mydb.cursor()
            sql4 = "SELECT stock FROM product_table WHERE company_id = %s AND product_id = %s;"
            strci4 = (companyid, proid)
            cur4.execute(sql4, strci4)
            iistock = cur4.fetchone()[0]

            totalstock = float(istock) + float(iistock)

            cur6 = mydb.cursor()
            sql6 = "UPDATE product_table SET stock = %s WHERE company_id = %s AND product_id = %s;"
            strci6 = (totalstock, companyid, proid)
            cur6.execute(sql6, strci6)
            '''

            mydb.commit()
            mydb.close()
            self.loadorderTable()
            self.ORbtn.setEnabled(False)


        except Exception as e:
            print(e)
    def dataload(self):
        try:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT sales_id FROM sales_table WHERE company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            salesss = int(cur.fetchone()[0])

            if salesss > 0:
                self.lineEdit_12.setText("Data Loaded")
        except Exception as e:
            print(e)
    def refresh(self):
        self.loaddashboardtable()
        self.loadproductstable()
        self.loadrefundTable()
        self.loadsalestable()
        self.loadorderTable()
        self.loaddefectTable()
        self.loadorderTable()
        self.loaddashboard()

    def printfunction(self):
        global m, forecast, price_elasticity, mape, model, rmse, rmean, companyid, companyname, pdfpname, result, test, tresult, rmse_reg, mse_reg, mae_reg, mape_reg, unique_x, mean_per_price, result
        try:
            Fr = str(self.intervalCB.currentText())
            Pr = str(self.PredRTB.text())
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT company_name FROM company_table WHERE company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            companyname = cur.fetchone()[0]
            companyname = str(companyname)

            pdfpname = str(self.selectedpTB.text())

            ADate = sales_prediction['Date'].to_list()
            for i in range(len(ADate)):
                ADate[i] = str(ADate[i])

            AVolume = sales_prediction['Anticipated Volume'].to_list()
            for i in range(len(ADate)):
                if AVolume[i] > 0:
                    AVolume[i] = str(AVolume[i])
                else:
                    AVolume[i] = "0"
            APrice = sales_prediction['Anticipated Price'].to_list()
            for i in range(len(APrice)):
                if float(AVolume[i]) > 0:
                    APrice[i] = str(APrice[i])
                else:
                    APrice[i] = "0"
            data_as_dict = {"Date": ADate,
                            "Anticipated Volume": AVolume,
                            "Anticipated Price": APrice

                            }
            pdf = PDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Times", size=14, style="B")
            pdf.cell(0, 8, "SalesCast Report", ln=1, align='C')
            pdf.cell(30, 8, '      ', ln=1)
            pdf.cell(30, 8, '      ', ln=1)

            pdf.set_font("Times", size=12, style="B")
            pdf.cell(30, 8, "I. Prediction Output", ln=1)

            pdf.set_font("Times", size=12)
            freq_key_full = Fr
            pdf.cell(30, 8, 'Frequency: ' + freq_key_full)
            pdf.cell(0, 8, "Number of periods predicted: " + str(Pr), align='R', ln=1)
            last_record_date = '2017-12-26'
            pdf.cell(30, 8, 'Last recorded date: ' + last_record_date, ln=1)
            pdf.cell(30, 8, '      ', ln=1)
            pdf.set_font("Times", size=10)
            pdf.cell(0, 8, 'Table 1. Expected number of  stocks and suggested prices', align='C', ln=1)
            pdf.create_table(table_data=data_as_dict, title_size=11, cell_width='even', align_data='C',
                             align_header='C')
            pdf.ln()

            pdf.cell(30, 8, '      ', ln=1)
            pdf.cell(30, 8, '      ', ln=1)
            pdf.set_font("Times", size=12, style="B")
            pdf.cell(30, 8, "II. Price Elasticity of Demand", ln=1)
            pdf.set_font("Times", size=12)
            pdf.cell(30, 8, f"Price Elasticity of Demand(PED) Value: ", )
            pdf.set_font("Times", size=12, style="BI")
            pdf.cell(60, 8, f"{round(price_elasticity, 4)}", align='R', ln=1)
            pdf.set_font("Times", size=12)
            pe_legend = ["Inelastic", "Negative Elastic", "Positive Elastic"]
            pe_short_interpret = ["-1 < PED < 1", "PED < -1", "PED > 1"]
            pe_interpret = ["Price does not affect demand",
                            "Price affects demand, where as price increase, demand is expected to decrease",
                            "Price affects demand, where as price increase, demand is expected to increase"]
            price_elasticity_interpretation = {"PED Classification": pe_legend, "PED Value": pe_short_interpret,
                                               "Interpretation": pe_interpret}
            pdf.set_font("Times", size=10)
            pdf.cell(0, 8, 'Table 2. Interpretation for PED Value', align='C', ln=1)
            pdf.create_table(table_data=price_elasticity_interpretation, title_size=11)
            pdf.ln()

            pdf.cell(30, 8, '      ', ln=1)
            pdf.cell(30, 8, '      ', ln=1)
            pdf.set_font("Times", size=12, style="B")
            pdf.cell(30, 8, "III. Prophet Analysis", ln=1)

            pdf.image("prophetplot.png", w=200)
            pdf.ln
            pdf.set_font("Times", size=10)
            pdf.cell(0, 8, "Figure 1. Prophet Plot Diagram shows the trend of sales(y) and date(ds).", align='C', ln=1)

            # x-----------------------------------------------------
            pdf.set_font("Times", size=12, style="BI")
            pdf.cell(30, 8, "      3.1. Error Metric Evaluation", ln=1)

            pdf.set_font("Times", size=12)
            pdf.cell(30, 8, "            3.1.1. Root Mean Squared Error", ln=1)

            pdf.set_font("Times", size=11)
            mean_value = round(test['sold_quantity'].mean(), 2)
            percent_rmse_mean = round((rmse / mean_value) * 100, 2)

            pdf.cell(30, 8, f"                Mean Value of Dataset: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"{mean_value}", align='R', ln=1)

            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                Root Mean Squared Error: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"{round(rmse, 2)}", align='R', ln=1)

            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                RMSE - Mean Value Percentage: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"     {percent_rmse_mean}%", align='R', ln=1)
            rmse_value = ["5% - 10%", "11% - 25%", " >26% "]
            rmse_interpretation = ["Very accurate model", "Acceptable", "Not Acceptable"]
            rmse_dict = {"Percent Value": rmse_value, "Interpretation": rmse_interpretation}
            pdf.create_table(table_data=rmse_dict, title_size=11,
                             title="Table 3.1 RMSE - Mean Value Percentage Interpretation")
            pdf.ln()
            pdf.cell(30, 8,
                     "           **RMSE is scale dependent to the mean value of dataset. The lower the RMSE the more accurate the model is.",
                     ln=1)

            pdf.set_font("Times", size=12)
            pdf.cell(30, 8, "            3.1.2. Mean Squared Error", ln=1)
            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                Mean Squared Error: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"                {round(rmse * rmse, 2)}", align='R', ln=1)
            pdf.set_font("Times", size=10)

            pdf.cell(30, 8, '      ', ln=1)
            pdf.cell(30, 8, '      ', ln=1)
            pdf.cell(30, 8,
                     "                 **Mean squared error shows the measures how close a regression line is to a set of data points.",
                     ln=1)
            pdf.cell(30, 8, "                 **Mainly used to evaluate two or more models", ln=1)

            pdf.cell(30, 8, '      ', ln=1)

            pdf.set_font("Times", size=12)
            pdf.cell(30, 8, "           3.1.3. Mean Absolute Percentage Error", ln=1)
            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                Mean Absolute Percentage Error: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"                {round(mape, 2)}%", align='R', ln=1)
            pdf.set_font("Times", size=11)
            pdf.create_table(table_data=rmse_dict, title_size=11, title="Table 3.2 MAPE Interpretation")
            pdf.ln()
            pdf.cell(30, 8, "                 **MAPE measures accuracy of a forecast system in percentage.", ln=1)

            pdf.set_font("Times", size=12)
            pdf.cell(30, 8, "           3.1.4. Mean Absolute Error", ln=1)
            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                Mean Absolute Error: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"  {round(mae, 2)}", align='R', ln=1)
            pdf.set_font("Times", size=10)
            pdf.cell(30, 8,
                     f"               **Mean Absolute Error(MAE) is the average of all absolute errors. You may refer to the MAPE Interpretation.",
                     ln=1)

            pdf.set_font("Times", size=12, style="B")
            # --------------------------------------------------x
            pdf.cell(30, 8, '      ', ln=1)
            pdf.cell(30, 8, '      ', ln=1)
            pdf.cell(30, 8, "IV. Regression Analysis", ln=1)

            pdf.set_font("Times", size=12, style="BI")
            pdf.cell(30, 8, "      4.1. Initial Regression Analysis", ln=1)

            pdf.image("Initial Regression.png", w=190)
            pdf.ln
            pdf.set_font("Times", size=10)
            pdf.cell(0, 8, "Figure 2. Initial Regression Analysis where x are the prices and y are the sales",
                     align='C', ln=1)
            pdf.cell(30, 8, '      ', ln=1)

            p_value_placeholder = tresult
            p_value_interpretation = "REJECTED"
            if p_value_placeholder > 0.05:
                p_value_interpretation = "ACCEPTED"
            p_value_placeholder = str(p_value_placeholder)

            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                P_Value: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"  {p_value_placeholder}", align='R', ln=1)
            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                Interpretation: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"  {p_value_interpretation}", align='R', ln=1)
            pdf.set_font("Times", size=10)

            pdf.cell(30, 8,
                     "                 **A P-value that is REJECTED means that the values of the dataset is perfectly linear.",
                     ln=1)
            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, '      ', ln=1)

            pdf.cell(30, 8, "                 OLS Regression Summary", ln=1)
            pdf.cell(30, 8, '      ', ln=1)
            pdf.multi_cell(0, 5, str(result.summary()))
            pdf.ln()

            # ----------------------------------------------------------x
            pdf.set_font("Times", size=12, style="BI")
            pdf.cell(30, 8, "      4.2. Final Regression Analysis", ln=1)

            pdf.image("Final Regression.png", w=190)
            pdf.ln
            pdf.set_font("Times", size=10)
            pdf.cell(0, 8, "Figure 3. Final Regression Analysis where x are the prices and y are the sales", align='C',
                     ln=1)
            unique_x2 = []
            for row in unique_x:
                unique_x2.append(str(row))
            unique_x = unique_x2

            mean_per_price2 = []
            for row2 in mean_per_price:
                mean_per_price2.append(str(row2))
            mean_per_price = mean_per_price2

            fin_reg_table = {"x-value": unique_x2, "y-value": mean_per_price2}
            pdf.create_table(table_data=fin_reg_table, title="Price - Average Sales Table")

            pdf.set_font("Times", size=12, style="BI")
            pdf.cell(30, 8, "      4.3. Error Metric Evaluation", ln=1)

            pdf.set_font("Times", size=12)
            pdf.cell(30, 8, "            4.1.1 Root Mean Squared Error", ln=1)

            pdf.set_font("Times", size=11)
            mean_value = round(test['selling_price'].mean(), 2)
            percent_rmse_mean = round((rmse_reg / mean_value) * 100, 2)

            pdf.cell(30, 8, f"                Mean Value of Dataset: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"{mean_value}", align='R', ln=1)

            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                Root Mean Squared Error: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"{round(rmse_reg, 2)}", align='R', ln=1)

            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                RMSE - Mean Value Percentage: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"     {percent_rmse_mean}%", align='R', ln=1)
            rmse_value = ["5% - 10%", "11% - 25%", " >26% "]
            rmse_interpretation = ["Very accurate model", "Acceptable", "Not Acceptable"]
            rmse_dict = {"Percent Value": rmse_value, "Interpretation": rmse_interpretation}
            pdf.create_table(table_data=rmse_dict, title_size=11,
                             title="Table 3.1 RMSE - Mean Value Percentage Interpretation")
            pdf.ln()
            pdf.cell(30, 8,
                     "           **RMSE is scale dependent to the mean value of dataset. The lower the RMSE the more accurate the model is.",
                     ln=1)

            pdf.set_font("Times", size=12)
            pdf.cell(30, 8, "            4.1.1 Mean Squared Error", ln=1)
            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                Mean Squared Error: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"                {round(mse_reg, 2)}", align='R', ln=1)
            pdf.set_font("Times", size=10)

            pdf.cell(30, 8, '      ', ln=1)
            pdf.cell(30, 8, '      ', ln=1)
            pdf.cell(30, 8,
                     "                 **Mean squared error shows the measures how close a regression line is to a set of data points.",
                     ln=1)
            pdf.cell(30, 8, "                 **Mainly used to evaluate two or more models", ln=1)

            pdf.cell(30, 8, '      ', ln=1)

            pdf.set_font("Times", size=12)
            pdf.cell(30, 8, "           4.1.3 Mean Absolute Percentage Error", ln=1)
            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                Mean Absolute Percentage Error: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"                {round(mape_reg, 2)}%", align='R', ln=1)
            pdf.set_font("Times", size=11)
            pdf.create_table(table_data=rmse_dict, title_size=11, title="Table 3.2 MAPE Interpretation")
            pdf.ln()
            pdf.cell(30, 8, "                 **MAPE measures accuracy of a forecast system in percentage.", ln=1)

            pdf.set_font("Times", size=12)
            pdf.cell(30, 8, "           3.1.4. Mean Absolute Error", ln=1)
            pdf.set_font("Times", size=11)
            pdf.cell(30, 8, f"                Mean Absolute Error: ")
            pdf.set_font("Times", size=11, style='B')
            pdf.cell(60, 8, f"  {round(mae_reg, 2)}", align='R', ln=1)
            pdf.set_font("Times", size=10)
            pdf.cell(30, 8,
                     f"               **Mean Absolute Error(MAE) is the average of all absolute errors. You may refer to the MAPE Interpretation.",
                     ln=1)

            pdf.set_font("Times", size=12, style="B")

            # pdf.image("ProphetGraph.jpg",4,90,175,160,"PNG")

            pdf.output('table_class.pdf')

            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Report has been created")
            msgbox.setWindowTitle("Success!")
            msgbox.exec_()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Run forecast first before running dynamic pricing!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
    def highlightrefunddeletefunction(self):
        global rdeleteID, SelectedRID
        try:
            rcell = self.refundTable.selectedItems()[0]
            rdeleteID = rcell.text()
            SelectedRID = rdeleteID
            print(rdeleteID)
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("No item is selected")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
    def loadrefundTable(self):
        try:
            self.refundTable.setRowCount(0);
            global companyid, SortVarrefund, rawr3
            if SortVar == 0:
                mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur = mydb.cursor()
                sql = "SELECT refund_table.refund_id, product_table.product_photo, product_table.product_name, product_table.category, refund_table.sales_id, refund_table.sold_quantity, refund_table.total_sold, refund_table.date, refund_table.description FROM refund_table INNER JOIN product_table ON refund_table.product_id = product_table.product_id WHERE refund_table.company_id = %s;"
                strci = (companyid,)
                cur.execute(sql, strci)
                rows = cur.fetchall()
                tablerow = 0
                self.refundTable.setRowCount(len(rows))
                for row in rows:
                    if row[1] == None:
                        self.refundTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                        self.refundTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                        self.refundTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                        self.refundTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                        self.refundTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                        self.refundTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                        self.refundTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                        self.refundTable.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
                        self.refundTable.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))

                        tablerow += 1
                    else:
                        self.refundTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                        image = row[1]
                        pixmap2 = QtGui.QPixmap()
                        pixmap2.loadFromData(image, 'jpg')
                        label2 = QLabel()
                        label2.setScaledContents(True)
                        label2.setPixmap(pixmap2)
                        self.refundTable.setCellWidget(tablerow, 1, label2)
                        self.refundTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                        self.refundTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                        self.refundTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                        self.refundTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                        self.refundTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                        self.refundTable.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
                        self.refundTable.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))
                        tablerow += 1
            else:
                try:
                    tablerow = 0
                    self.refundTable.setRowCount(len(rawr3))
                    for row in rawr3:
                        if row[1] == None:
                            self.refundTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                            self.refundTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                            self.refundTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                            self.refundTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                            self.refundTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                            self.refundTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                            self.refundTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                            self.refundTable.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
                            tablerow += 1
                        else:
                            self.refundTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                            image = row[1]
                            pixmap2 = QtGui.QPixmap()
                            pixmap2.loadFromData(image, 'jpg')
                            label2 = QLabel()
                            label2.setScaledContents(True)
                            label2.setPixmap(pixmap2)
                            self.refundTable.setCellWidget(tablerow, 1, label2)
                            self.refundTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                            self.refundTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                            self.refundTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                            self.refundTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                            self.refundTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                            self.refundTable.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
                            tablerow += 1
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
    def refunddeletefunction(self):
        global rdeleteID, companyid
        try:

            ISDEL = int(rdeleteID)
            print(ISDEL, "IPDEL CHECK")
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "DELETE FROM refund_table WHERE refund_id = %s AND company_id = %s;"
            strci = (ISDEL, companyid)
            cur.execute(sql, strci)
            mydb.commit()
            mydb.close()
            self.loadrefundTable()
        except Exception as e:
            print(e)
    def refundsearchfunction(self):
        global companyid
        self.refundTable.setRowCount(0);
        pstrsearch = self.refundtextbox.text()
        try:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            pcur = mydb.cursor()
            pstrsearch = "%" + pstrsearch + "%"
            psql = "SELECT product_table.product_id, product_table.product_photo, product_table.product_name, product_table.category, refund_table.sold_quantity, refund_table.total_sold, refund_table.date, refund_table.description FROM refund_table INNER JOIN product_table ON refund_table.product_id = product_table.product_id WHERE refund_table.company_id = %s AND product_table.product_name LIKE %s;"
            pstrci = (companyid, pstrsearch)
            pcur.execute(psql, pstrci)
            presult = pcur.fetchall()
            tablerow = 0
            self.refundTable.setRowCount(len(presult))
            for row in presult:
                if row[1] == None:
                    self.refundTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.refundTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.refundTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.refundTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.refundTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.refundTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.refundTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.refundTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[7])))
                    tablerow += 1
                else:
                    self.refundTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    image = row[1]
                    pixmap2 = QtGui.QPixmap()
                    pixmap2.loadFromData(image, 'jpg')
                    label2 = QLabel()
                    label2.setScaledContents(True)
                    label2.setPixmap(pixmap2)
                    self.refundTable.setCellWidget(tablerow, 1, label2)
                    self.refundTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.refundTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.refundTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.refundTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.refundTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.refundTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[7])))
                    tablerow += 1
        except Exception as e:
            print(e)
    def highlightorderdeletefunction(self):
        global odeleteID, SelectedOID
        try:
            ocell = self.orderTable.selectedItems()[0]
            odeleteID = ocell.text()
            SelectedOID = odeleteID
            print(odeleteID)
            testx = 0

            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )

            cur = mydb.cursor()
            sql = "SELECT order_status FROM order_table WHERE order_id = %s AND company_id = %s;"
            strci = (SelectedOID, companyid)
            cur.execute(sql, strci)
            result = cur.fetchone()[0]
            sresult = str(result)
            print(sresult)

            cur2 = mydb.cursor()
            sql2 = "SELECT order_defective FROM order_table WHERE order_id = %s and company_id = %s"
            strci2 = (SelectedOID, companyid)
            cur2.execute(sql2, strci2)
            try:
                test = cur2.fetchone()[0]
                testx = float(test)
            except Exception as e:
                print(e)
                testx = 0

            if sresult == "Pending":
                self.ORbtn.setEnabled(True)
                self.transferBTN.setEnabled(False)
                self.addDefectBTN.setEnabled(False)

            elif sresult == "Received":

                self.transferBTN.setEnabled(True)
                if testx == 0:
                    self.addDefectBTN.setEnabled(True)
                    self.orderbox_2.setEnabled(True)
                else:
                    self.addDefectBTN.setEnabled(False)
                    self.orderbox_2.setEnabled(False)
                self.ORbtn.setEnabled(False)
            else:
                self.ORbtn.setEnabled(False)
                self.transferBTN.setEnabled(False)
                self.addDefectBTN.setEnabled(False)
                self.orderbox_2.setEnabled(False)
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("No item is selected")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
    def highlightdefectfunction(self):
        global ddeleteID, SelectedDID
        try:
            dcell = self.defectTable.selectedItems()[0]
            ddeleteID = dcell.text()
            SelectedDID = ddeleteID
            print(ddeleteID)
            testx = 0

            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )

            cur = mydb.cursor()
            sql = "SELECT status FROM defective_table WHERE defective_id = %s AND company_id = %s;"
            strci = (SelectedDID, companyid)
            cur.execute(sql, strci)
            result = cur.fetchone()[0]
            sresult = str(result)
            print(sresult)

            if sresult == "Pending":
                self.RFBTN.setEnabled(True)
            else:
                self.RFBTN.setEnabled(False)

        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("No item is selected")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
    def loadorderTable(self):
        try:
            self.orderTable.setRowCount(0);
            global companyid, SortVarrefund, rawr4
            if SortVar == 0:
                mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur = mydb.cursor()
                sql = "SELECT order_table.order_id, product_table.product_name, order_table.order_placedate, order_table.order_receivedate, order_table.order_quantity, order_table.order_defective, order_table.order_status FROM product_table INNER JOIN order_table ON product_table.product_id = order_table.product_id WHERE order_table.company_id = %s;"
                strci = (companyid,)
                cur.execute(sql, strci)
                rows = cur.fetchall()
                tablerow = 0
                self.orderTable.setRowCount(len(rows))
                for row in rows:
                        self.orderTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                        self.orderTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                        self.orderTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                        self.orderTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                        self.orderTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                        self.orderTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                        self.orderTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))

                        tablerow += 1
            else:
                try:
                    tablerow = 0
                    self.orderTable.setRowCount(len(rawr4))
                    for row in rawr4:
                            self.orderTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                            self.orderTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                            self.orderTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                            self.orderTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                            self.orderTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                            self.orderTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                            self.orderTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                            tablerow += 1

                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
    def orderdeletefunction(self):
        global odeleteID, companyid
        try:

            ISDEL = int(odeleteID)
            print(ISDEL, "IPDEL CHECK")
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "DELETE FROM order_table WHERE order_id = %s AND company_id = %s;"
            strci = (ISDEL, companyid)
            cur.execute(sql, strci)
            mydb.commit()
            mydb.close()
            self.loadorderTable()
        except Exception as e:
            print(e)
    '''
    def ordereditfunction(self):
        global companyid, SelectedOID
        try:

            oquantity = self.orderbox.text()
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "UPDATE order_table SET order_quantity = %s WHERE company_id = %s AND order_id = %s;"
            strci = (oquantity, companyid, SelectedOID)
            cur.execute(sql, strci)
            mydb.commit()
            mydb.close()
            self.loadorderTable()

        except Exception as e:
            print(e)
    '''
    def transferOrder(self):
        global companyid, SelectedOID
        trnsf = "Completed"
        TransfStocks = 0
        try:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "UPDATE order_table SET order_status = %s WHERE company_id = %s AND order_id = %s;"
            strci = (trnsf, companyid, SelectedOID)
            cur.execute(sql, strci)



            cur2 = mydb.cursor()
            sql2 = "SELECT order_table.order_quantity FROM product_table INNER JOIN order_table ON product_table.product_id = order_table.product_id WHERE order_table.company_id = %s AND order_table.order_id = %s;"
            strci2 = (companyid, SelectedOID)
            cur2.execute(sql2, strci2)
            Oquanty = cur2.fetchone()[0]
            print(Oquanty)

            cur3 = mydb.cursor()
            sql3 = "SELECT order_table.product_id FROM product_table INNER JOIN order_table ON product_table.product_id = order_table.product_id WHERE order_table.company_id = %s AND order_table.order_id = %s;"
            strci3 = (companyid, SelectedOID)
            cur3.execute(sql3, strci3)
            Oprod = cur3.fetchone()[0]
            print(Oprod)

            cur4 = mydb.cursor()
            sql4 = "SELECT product_table.stock FROM product_table INNER JOIN order_table ON product_table.product_id = order_table.product_id WHERE order_table.company_id = %s AND order_table.order_id = %s;"
            strci4 = (companyid, SelectedOID)
            cur4.execute(sql4, strci4)
            ProdStock = cur4.fetchone()[0]
            print(ProdStock)

            TransfStocks = float(Oquanty) + float(ProdStock)
            print(TransfStocks)

            cur5 = mydb.cursor()
            sql5 = "UPDATE product_table SET stock = %s WHERE company_id = %s AND product_id = %s;"
            strci5 = (TransfStocks, companyid, Oprod)
            cur5.execute(sql5, strci5)

            mydb.commit()
            mydb.close()
            self.highlightorderdeletefunction()
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Items has been added to Inventory!")
            msgbox.setWindowTitle("Success!")
            msgbox.exec_()
        except Exception as e:
            print(e)
    def loaddefectTable(self):
        try:
            self.defectTable.setRowCount(0);
            global companyid, rawr5
            #if SortVar == 0:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
            cur = mydb.cursor()
            sql = "SELECT defective_table.defective_id, defective_table.order_id, defective_table.refund_id, product_table.product_name, defective_table.base_price, defective_table.def_quantity, defective_table.def_total, defective_table.def_desc, defective_table.status FROM defective_table INNER JOIN product_table ON defective_table.product_id = product_table.product_id WHERE defective_table.company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            rows = cur.fetchall()
            tablerow = 0
            self.defectTable.setRowCount(len(rows))
            for row in rows:
                    self.defectTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.defectTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.defectTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    self.defectTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    self.defectTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.defectTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.defectTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.defectTable.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
                    self.defectTable.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))
                    tablerow += 1
        except Exception as e:
            print(e)
    def sortcheckfunction(self):
        global SortVar
        try:
            if self.sortcheck.isChecked() == True:
                SortVar = 1
                self.loadsalestable()
            else:
                SortVar = 0
                self.loadsalestable()
        except Exception as e:
            print(e)

    def gotoaddorder(self):
        try:
            AOS = AddOrderScreen()
            widget15.addWidget(AOS)
            widget15.show()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)

    def gotoviewaccuracy(self):
        try:
            global mape
            if mape is None:
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Critical)
                msgbox.setText("Run forecast first before running dynamic pricing!")
                msgbox.setWindowTitle("Error!")
                msgbox.exec_()
            else:
                VAC = ViewAccuracyScreen()
                widget11.addWidget(VAC)
                widget11.show()

        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Run forecast first before running dynamic pricing!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
    def gotoeditrefundscreen(self):
        if SelectedRID == 0 or SelectedRID is None:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("No product is selected!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print("Wrong username/password")
        else:
            ERS = EditRefundScreen()
            widget10.addWidget(ERS)
            widget10.show()
    def gotouseredit(self):
        UEDS = UserEditScreen()
        widget14.addWidget(UEDS)
        widget14.show()
    def gotoexportsales(self):
        EXS = ExportSalesScreen()
        widget9.addWidget(EXS)
        widget9.show()
    def gotowelcomescreen(self):
        try:
            global companyid
            companyid = None
            self.deleteLater()
            '''widget.hide()
            WS = WelcomeScreen()
            widget12.addWidget(WS)
            widget12.show() '''
            widget.setCurrentIndex(widget.currentIndex() - 1)
        except Exception as e:
            print(e)

    def gotonotifscreen(self):
        NTF = NotificationScreen()
        widget12.addWidget(NTF)
        widget12.show()
    def gotoproductedit(self):
        global SelectedPID
        try:
            if SelectedPID == 0 or SelectedPID is None:

                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Critical)
                msgbox.setText("No product is selected!")
                msgbox.setWindowTitle("Error!")
                msgbox.exec_()
                print("Wrong username/password")
            else:
                PE = EditProductScreen()
                widget7.addWidget(PE)
                widget7.show()
        except Exception as e:
            print(e)

    def gotosalesedit(self):
        global SelectedSID
        if SelectedSID == 0 or SelectedSID is None:

            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("No product is selected!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print("Wrong username/password")
        else:
            SE = EditSalesScreen()
            widget8.addWidget(SE)
            widget8.show()

    def gotosortsales(self):
        SSS = SortSalesScreen()
        widget6.addWidget(SSS)
        widget6.show()

    def gotoaddrefund(self):
        ARS = AddRefundScreen()
        widget13.addWidget(ARS)
        widget13.show()
    def gotorundynamicpricing(self):
        try:
            global mape
            if mape is None:
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Critical)
                msgbox.setText("Run forecast first before running dynamic pricing!")
                msgbox.setWindowTitle("Error!")
                msgbox.exec_()
            else:
                RDP = RunDynamicPricingScreen()
                widget5.addWidget(RDP)
                widget5.show()

        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Run forecast first before running dynamic pricing!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
    def gotoaddproduct(self):
        APS = AddProductScreen()
        widget2.addWidget(APS)
        widget2.show()
    def gotoaddcateg(self):
        ACS = AddCategoryScreen()
        widget3.addWidget(ACS)
        widget3.show()
    def gotoaddsales(self):
        try:
            ASS = AddSalesScreen()
            widget4.addWidget(ASS)
            widget4.show()
        except Exception as e:
            print(e)
    def loadproductstable(self):
        self.ProductTable.setRowCount(0);
        try:
            global companyid
            print(companyid)
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT product_id, product_photo, product_name, category, stock, price, exp_numdate, exp_valstock FROM product_table WHERE company_id = %s"
            strci = (companyid,)
            cur.execute(sql, strci)
            rows = cur.fetchall()
            tablerow=0
            self.ProductTable.setRowCount(len(rows))

            for row in rows:
                if row[1] == None:
                    self.ProductTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.ProductTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.ProductTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.ProductTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.ProductTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.ProductTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.ProductTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.ProductTable.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
                else:
                    self.ProductTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    image = row[1]
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(image, 'jpg')
                    label = QLabel()
                    label.setScaledContents(True)
                    label.setPixmap(pixmap)
                    self.ProductTable.setCellWidget(tablerow, 1, label)
                    self.ProductTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.ProductTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.ProductTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.ProductTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.ProductTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.ProductTable.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
                tablerow+=1
        except Exception as e:
            print(e)

    def addcsv(self):
        global companyid
        try:
            csv = QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'CSV files (*.csv)')

            filename = csv[0]

            print(csv, "ito yung csv")
            print(filename, "ito yung filename")
            scsv = str(filename)
            global csvread
            train_size = int(len(csv) * .80)
            train, test = csv[0:train_size], csv[train_size:len(csv)]
            df = train
            csvread = pd.read_csv(scsv)
            csvread.dropna(inplace=True)
            csvread.reset_index(drop=True, inplace=True)
            print(csvread)

            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT product_id, product_name FROM product_table WHERE company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            rows = cur.fetchall()
            print(rows, "eto yung pname ")
            result = list(map(list, zip(*rows)))
            prid, prn = result

            print(prid, "prodid")
            print(prn, "prn")
            product_table = {'product_id': prid, 'product_name': prn}
            df = pd.DataFrame(data=product_table)
            print(df)
            # extract product_id:product_name association and put into dictionary
            prodDict = df.set_index('product_id').to_dict()['product_name']

            # extract product_name from CSV and put into array
            prod_name_col = csvread['product_name'].to_numpy()

            # get list of primary keys instatiate array for prod_id
            prodDict_keys = prodDict.keys()
            prodDict_keys = list(prodDict_keys)
            prod_id = []

            # for loop to add product_id
            for i in range(len(prod_name_col)):
                for j in range(len(prodDict_keys)):
                    if prod_name_col[i] == prodDict[prodDict_keys[j]]:
                        prod_id.append(prodDict_keys[j])

            # insert product_id column
            csvread.insert(loc=0, column='product_id', value=prod_id)

            # print updated CSV
            print(csvread)

        except Exception as e:
            print(e)

    def replacecsvfunction(self):
        global csvread, companyid
        try:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            #cur2 = mydb.cursor()
            for row in csvread.itertuples():
                sql = """INSERT INTO sales_table (company_id, product_id, date, sold_quantity, selling_price, total_sold) VALUES (%s,%s,%s,%s,%s,%s)"""

                cur.execute(sql,
                            (companyid, row.product_id, row.date, row.sold_quantity, row.selling_price, row.total_sold))
                mydb.commit()
            #sql2 = "DELETE FROM sales_table WHERE sold_quantity = 0 AND company_id = %s;"
            strci = (companyid,)
            #cur2.execute(sql2, strci)
            mydb.commit()
            mydb.close()
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Dataset Added!")
            msgbox.setWindowTitle("Success!")
            msgbox.exec_()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("No dataset was added!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)

    def loaddashboard(self):
        global companyid

        try:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            cur2 = mydb.cursor()
            cur3 = mydb.cursor()
            cur4 = mydb.cursor()
            cur5 = mydb.cursor()
            cur6 = mydb.cursor()
            sql = "SELECT SUM(stock) FROM product_table WHERE company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            rows = cur.fetchone()[0]
            PLSum = str(rows)
            print(rows, "ETO YUNG LISTING")
            self.TPListingLabel.setText(PLSum)

            sql2 = "SELECT SUM(sold_quantity) FROM sales_table WHERE (month(date)=month(now())-1 AND company_id = %s);"
            cur2.execute(sql2, strci)
            rows2 = cur2.fetchone()[0]
            MSSum = str(rows2)
            self.TMSalesLabel.setText(MSSum)

            sql3 = "SELECT SUM(total_sold) FROM sales_table WHERE (month(date)=month(now())-1 AND company_id = %s);"
            cur3.execute(sql3, strci)
            rows3 = cur3.fetchone()[0]
            MISum = str(rows3)
            self.TMIncomeLabel.setText(MISum)

            sql4 = "SELECT count(product_name) FROM product_table WHERE company_id = %s AND stock < 21;"
            cur4.execute(sql4, strci)
            rows4 = cur4.fetchone()[0]
            RunOut = str(rows4)
            self.RunningOut.setText(RunOut)

            sql5 = "SELECT count(order_id) FROM order_table WHERE company_id = %s AND order_status = 'Pending';"
            cur5.execute(sql5, strci)
            rows5 = cur5.fetchone()[0]
            Pend = str(rows5)
            self.PendingOrd.setText(Pend)

            sql6 = "SELECT SUM(def_total) FROM defective_table WHERE company_id = %s";
            cur6.execute(sql6, strci)
            rows6 = cur6.fetchone()[0]
            totes6 = str(rows6)
            self.pendingReturn.setText(totes6)


        except Exception as e:
            print(e)

    def loadcsvfromdb(self):
        global companyid
        try:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT company_csv FROM company_table WHERE company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            csv = cur.fetchone()[0]

            csv3 = csv.decode('UTF-8')

           # with open(csv, 'rt') as file:
             #   csvr = file.read()
            x = csv3.split("\n")


            x_new = []
            prodlist = []
            prodname = []
            datelist = []
            sqlist = []
            splist = []
            tslist = []
            for i in range (len(x)):
                x2 = x[i].split(',')
                x_new.append(x2)

            x_new[0][0] = "product_id"

            prod_keys = x_new[0]
            #x_new.pop(x_new[0])

            for xx1 in range(len(x_new)):
                prodlist = x_new[0][0]

            print("prodlist ito", prodlist)



            print(x_new)


            df1 = pd.DataFrame(data=csv3)

            #print(df1, "eto yung df")
            self.lineEdit_12.setText("Data Loaded")
        except Exception as e:
            print(e)

    def highlightproductdeletefunction(self):
        global pdeleteID, SelectedPID
        try:
            pcell = self.ProductTable.selectedItems()[0]

            pdeleteID = pcell.text()
            print(pdeleteID)
            SelectedPID = pdeleteID
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("No item is selected")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)

    def highlightsalesdeletefunction(self):
        global sdeleteID, SelectedSID
        try:
            scell = self.salesTable.selectedItems()[0]
            sdeleteID = scell.text()
            print(sdeleteID)
            SelectedSID = sdeleteID
            print(SelectedSID)
            if SelectedSID != 0:
                self.reb.setEnabled(True)
            else:
                self.reb.setEnabled(False)
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("No item is selected")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)

    def productdeletefunction(self):
        global pdeleteID, companyid
        try:

            IPDEL = int(pdeleteID)
            print(IPDEL, "IPDEL CHECK")
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "DELETE FROM product_table WHERE product_id = %s AND company_id = %s;"
            strci = (IPDEL, companyid)
            cur.execute(sql, strci)
            mydb.commit()
            mydb.close()
            self.loadproductstable()
        except Exception as e:
            print(e)


    def salesdeletefunction(self):
        global sdeleteID, companyid
        try:

            ISDEL = int(sdeleteID)
            print(ISDEL, "IPDEL CHECK")
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "DELETE FROM sales_table WHERE sales_id = %s AND company_id = %s;"
            strci = (ISDEL, companyid)
            cur.execute(sql, strci)
            mydb.commit()
            mydb.close()
        except Exception as e:
            print(e)
        self.loadsalestable()

    def showpredictionrange(self):
        global companyid
        try:
            sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
            cur = sqlcon.cursor()

            sql = "SELECT prediction_range FROM company_table WHERE company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            predRange = cur.fetchone()[0]
            print(predRange)
            self.predictionTB.setText(str(predRange))
        except Exception as e:
            print (e)

    def updatedpredRange(self):

        global companyid
        EPred = str(self.predictionTB.text())
        mydb =  mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
        cur = mydb.cursor()
        sql = "UPDATE company_table SET prediction_range = %s WHERE company_id = %s;"
        strci = (EPred, companyid)
        cur.execute(sql, strci)
        mydb.commit()
        mydb.close()

    def exportprintPO(self):
        try:
            global companyid, filname, ProductArr, StockArr, name
            ProductArr = []
            StockArr = []
            x = 0
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            cur6 = mydb.cursor()
            sql = "SELECT DISTINCT product_id FROM product_table WHERE stock<21 AND company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            arr = cur.fetchall()
            arr = [i[0] for i in arr]
            print(arr)
            sql = "SELECT company_name FROM company_table WHERE company_id = %s;"
            strci6 = (companyid,)
            cur6.execute(sql, strci6)
            compname = cur6.fetchone()[0]
            for row in arr:
                print("dumaan ba dito")
                filname = "ProductList"+str(x)+".csv"
                x= x+1
                print(filname)
                mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur = mydb.cursor()
                cur2 = mydb.cursor()
                sql = "SELECT product_table.product_name, sales_table.date, sales_table.sold_quantity, sales_table.selling_price, sales_table.sold_quantity FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s AND product_table.stock < 21 AND product_table.product_id = %s;"
                print(str(row), "eto yung row")
                strci = (companyid, row)
                cur.execute(sql, strci)
                categresult = cur.fetchall()


                print(categresult, "eto yung categresult")
                sql2 = "SELECT product_name FROM product_table WHERE company_id = %s AND product_id = %s"
                strci2 = (companyid, row)
                cur2.execute(sql2, strci2)
                prname = cur2.fetchone()[0]

                df = pd.DataFrame(categresult)
                headerList = ['product_name', 'date', 'sold_quantity', 'selling_price', 'total_sold']
                print(df,"eto yung dffile")
                df.to_csv(filname, header=headerList, index=False)
                ProductArr.append(prname)
                self.autopurchaseorder()

            name = str(compname)
            pdf = PDF2()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Times", size=10)
            stringStockArr = [str(i) for i in StockArr]
            data_as_dict = {"Product": ProductArr, "Quantity": stringStockArr}
            pdf.create_table(table_data=data_as_dict, title='Future Stocks and Suggested Prices', cell_width='even')
            pdf.ln()


            pdf.cell(180, 8, name, ln=1, align='R')
            pdf.cell(180, 8, 'Sign here ', ln=1, align='R')
            pdf.set_font("Times", size=12, style='U')
            pdf.cell(180, 8, name, ln=1, align='R')
            pdf.set_font("Times", size=10)
            pdf.cell(180, 8, 'Sign here ', ln=1, align='R')
            pdf.output('generated_order.pdf')
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Purchase Order has been generated!")
            msgbox.setWindowTitle("Success!")
            msgbox.exec_()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("No product is at critical/out of stock condition")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)

    def autopurchaseorder(self):
        global StockArr
        # import libraries
        import pandas as pd
        import matplotlib.pyplot as plt
        from prophet.plot import plot_plotly, plot_components_plotly
        from prophet import Prophet
        from statsmodels.tools.eval_measures import rmse
        from sklearn.metrics import mean_absolute_percentage_error
        import numpy as np

        def MAPE(Y_actual, Y_Predicted):
            mape = np.mean(np.abs((Y_actual - Y_Predicted) / Y_actual)) * 100
            return mape
        global filname
        # define number of periods to predict
        # print("Enter number of periods to predict: ")
        periods_to_predict = 10

        # read dataset
        df = pd.read_csv(filname)

        # date pre-processing

        df = df.drop_duplicates(subset=['product_name', 'date', 'sold_quantity', 'selling_price', 'total_sold'])
        df = df.dropna()

        # extract relevant data for predictions
        df = df[["date", "sold_quantity"]]

        # rename columns for Prophet to work
        df.columns = ['ds', 'y']
        df['ds'] = pd.to_datetime(df['ds'])

        # split dataset to train and to test
        train_size = int(len(df) * .80)
        train = df[0:train_size]
        test = df[train_size:len(df)]
        # print(train)
        # print(test)

        # make predictions
        m = Prophet()
        m.fit(train)

        periods_ = len(test) + periods_to_predict
        future = m.make_future_dataframe(periods=periods_, freq='D')  # MS for monthly, H for hourly
        forecast = m.predict(future)

        # extracting yhat from forecast to replace negative values to zero
        forecast_yhat_list = forecast['yhat'].tolist()
        print("foreccast_yhat_list ito ", forecast_yhat_list)
        # print("forecast looped yhat")
        for i in range(len(forecast_yhat_list)):
            if forecast_yhat_list[i] < 0:
                forecast_yhat_list[i] = 0

        # print(str(forecast_yhat_list))
        forecast['yhat'] = forecast_yhat_list

        # extracting predicted_period for rmse comparison
        predicted_period = forecast.tail(periods_to_predict)
        predicted_period = predicted_period[['ds', 'yhat']]
        prediction_with_date = forecast.iloc[train_size:len(df)]
        prediction_with_date = prediction_with_date[['ds', 'yhat']]

        array_demand = predicted_period['yhat'].tolist()
        print(array_demand)
        tots = math.ceil(sum(array_demand))

        print(tots)
        StockArr.append(tots)
        print("Eto yung array", StockArr, ProductArr)
    def processcsv(self):
        global basep, sales_prediction
        basep = self.bptb.text()
        def get_price(array_sales):
            global price_elasticity, model, result, df2, basep, slope, intercept, rmse_reg, mse_reg, mae_reg, mape_reg, pdfpname, test, tresult, unique_x, mean_per_price, result
            pdfpname = str(self.selectedpTB.text())
            selectedpname = self.selectedpTB.text()
            # 2 - split dataset to train and to test
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur21 = mydb.cursor()
            sql21 = "SELECT product_id FROM product_table WHERE company_id = %s AND product_name = %s"
            strci21 = (companyid, selectedpname)
            cur21.execute(sql21, strci21)
            poid = cur21.fetchone()[0]

            cur22 = mydb.cursor()
            sql22 = "SELECT selling_price FROM sales_table WHERE company_id = %s AND product_id = %s;"
            strci22 = (companyid, poid)
            cur22.execute(sql22, strci22)
            sp = cur22.fetchall()
            spx = [r[0] for r in sp]
            print(spx, "spx")
            cur23 = mydb.cursor()
            sql23 = "SELECT sold_quantity FROM sales_table WHERE company_id = %s AND product_id = %s;"
            strci23 = (companyid, poid)
            cur23.execute(sql23, strci23)
            sq = cur23.fetchall()
            sqx = [k[0] for k in sq]
            print(sqx, "sqx")
            reg_dict = {'selling_price': spx, 'sold_quantity': sqx}
            df3 = pd.DataFrame.from_dict(reg_dict)
            print(df3, "dito df")
            reg_train_size = int(len(df3) * .80)

            reg_train = df3[0:reg_train_size]
            reg_test = df3[reg_train_size:len(df3)]

            reg_train = reg_train[['sold_quantity', 'selling_price']]
            reg_test = reg_test[['sold_quantity', 'selling_price']]

            # 3 - sales as y and price as x
            x = reg_train['selling_price']
            y = reg_train['sold_quantity']



            print(x, "testx")
            print(y, "testy")
            plt.plot(spx, sqx)
            plt.title("Initial Regression Analysis")
            plt.savefig('Initial Regression.png')
            plt.close()
            print(y, "Y List")
            print(x, "X List")







            # add constant to predictor variables
            X = sm.add_constant(x)

            # fit linear regression model
            model = sm.OLS(y, X)

            result = model.fit()

            # view model summary
            print(result.summary())

            '''a, b = model.params

            print(a, "eto a")
            print(b, "eto b")
            '''
            print(str(result.f_pvalue), "P VALUE")


            tresult = result.f_pvalue
            # checking p_value<0.05
            if result.f_pvalue < 0.05:
                intercept, slope = result.params
                print(str(slope))
                # 6.1 - if p_value is valid then we accept the model
                reg_predictions = result.predict(reg_test)

                print(reg_predictions)

                # 6.2 - show the metrics such as RMSE
                print("Results")
                print("Root Mean Squared Error between actual and  predicted values: ",
                      rmse(reg_predictions, reg_test['selling_price']))
                print("Mean Value of Test Dataset:", reg_test['selling_price'].mean())

                df3_filtered = df3[['sold_quantity', 'selling_price']]
                reg_predictions = result.predict(df3_filtered)

                expected_price_dataframe = pd.DataFrame(reg_predictions, columns=['expected price'])
                df3['expected price'] = expected_price_dataframe['expected price']
                print(df3)
                df3.to_excel('New Prices Reg.xlsx')

            else:
                print("Extracting price elasticity to generate an equation.")
                # 7.1 - getting unique values of prices
                unique_x = x.tolist()
                unique_x = set(unique_x)
                unique_x = list(unique_x)

                # 7.2 - get mean per price point
                sale_per_price = []
                mean_per_price = []
                for i in range(len(unique_x)):
                    sale_per_price.append(df3[df3['selling_price'] == unique_x[i]])
                for i in range(len(sale_per_price)):
                    mean_per_price.append(sale_per_price[i]['sold_quantity'].mean())

                # 7.3 - re-assigning the x and y values
                x = df3['selling_price']
                y = df3['sold_quantity']

                print("The result is greater than .05")
                X = sm.add_constant(unique_x)
                model = sm.OLS(mean_per_price, X)
                result = model.fit()
                plt.plot(unique_x, mean_per_price)
                plt.title("Final Regression Analysis")
                plt.savefig('Final Regression.png')
                plt.clf()
                intercept, slope = result.params

                # Price elasticity Formula
                price_elasticity = round((slope) * (x.mean() / y.mean()), 2)
                price_elasticity_absolute = round(abs(price_elasticity), 2)
                price_elasticity_absolute_percent = price_elasticity_absolute / 100
                print(str(price_elasticity))

                # increase price by 1% then the demand decrease by price elasticity%
                average_price = round(x.mean(), 2)
                average_price_increased = round((average_price * .1) + average_price, 2)
                average_sales = round(y.mean(), 2)
                average_sales_decreased = abs(round(average_sales - (average_sales * (price_elasticity_absolute_percent * 10)), 2))

                # append the price and sales to it's respective arrays
                price_change = []
                sales_change = []
                price_change.append(average_price)
                price_change.append(average_price_increased)
                sales_change.append(average_sales)
                sales_change.append(average_sales_decreased)
                print(price_change)
                print(sales_change)

                X = sm.add_constant(price_change)
                model = sm.OLS(sales_change, X)
                result = model.fit()
                print(result.summary())

                intercept, slope = result.params

            # D = intercept + slope(p)

                y_values_array = y.tolist()
                expected_price_array = []
                for i in range(len(array_sales)):
                    expected_price = round((array_sales[i] - intercept) / slope, 2)
                    expected_price_array.append(expected_price)

                expected_price_eto = pd.DataFrame(expected_price_array, columns=['expected price'])

                print(expected_price_eto)
                expected_price_excel = []
                for i in range(len(y_values_array)):
                    expected_price = round((y_values_array[i] - intercept) / slope, 2)
                    expected_price_excel.append(expected_price)

                print(expected_price_excel)

                expected_price_dataframe = pd.DataFrame(expected_price_excel, columns=['expected price'])
                df3['expected price'] = expected_price_dataframe['expected price']
                print(df3)
                df3.to_excel('New Prices.xlsx')



                print("Results for Dynamic Pricing")

                print("Price Elasticity: " + str(price_elasticity))

                rmse_reg = sqrt(mean_squared_error(reg_test['selling_price'],
                                                   df3['expected price'].tail(len(reg_test['selling_price']))))
                mse_reg = mean_squared_error(reg_test['selling_price'],
                                             df3['expected price'].tail(len(reg_test['selling_price'])))
                mae_reg = mean_absolute_error(reg_test['selling_price'],
                                              df3['expected price'].tail(len(reg_test['selling_price'])))
                mape_reg = mean_absolute_percentage_error(df3['expected price'].tail(len(reg_test['selling_price'])),
                                                          reg_test['selling_price'])
                mape_reg = mape_reg * 100

                print("RMSE: " + str(rmse_reg))
                print("MSE: " + str(mse_reg))
                print("MAE: " + str(mae_reg))
                print("MAPE: " + str(mape_reg) + "%")

            '''
            print("Press [1] to input expected sales to find optimal price, or press [2] to enter price to find expected number of sales: ")
            choice = int(input())
            if (choice == 1):
                print("Enter expected number of sales: ")
                sales_input = int(input())
                price_output = round((sales_input - intercept) / slope, 2)
                print("Optimal Pricepoint: " + str(price_output))
            elif (choice == 2):
                print("Enter price: ")
                price_input = int(input())
                sales_output = intercept + slope * (price_input)
                print("Expected number of stocks to be sold: " + str(sales_output))
            else:
                print("Thank you so much.")
            '''
            return (expected_price_eto)




        try:
            global prodd

            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT date, selling_price, sold_quantity FROM sales_table WHERE company_id = %s and product_id = %s;"
            strci = (companyid, prodd)
            cur.execute(sql, strci)
            forec = cur.fetchall()
            mydb.commit()
            mydb.close()
            print(forec)

            result = list(map(list, zip(*forec)))
            det, selp, sold = result



            sales_table = {'date': det, 'selling_price': selp, 'sold_quantity': sold}
            global df2, rmse, rmean, m, forecast, price_elasticity, mape, mae, test
            df2 = pd.DataFrame(data=sales_table)
            print(df2, "DATABASEVAR")

            train_size = int(len(df2) * .80)
            train, test = df2[0:train_size], df2[train_size:len(df2)]

            DataTrain = train
            print(DataTrain, "DataTrain ito")

            # ----Enter needed inputs
            date_column = 'date'
            sales_column = 'sold_quantity'

            freq_key = 0
            freq_key1 = self.intervalCB.currentText()
            if freq_key1 == 'Daily':
                freq_key = 'D'
            elif freq_key1 == 'Weekly':
                freq_key = 'W'
            elif freq_key1 == 'Monthly':
                freq_key = 'M'
            elif freq_key1 == 'Yearly':
                freq_key = 'Y'

            print("Enter Number of periods to forecast: ")
            period = self.PredRTB.text()
            period = int(period)
            # ------log-transform
            train = train.rename(columns={sales_column: 'y', date_column: 'ds'})

            #train['y'] = np.log(train['y'])


            # ------instantiate prophet
            m = Prophet()
            m.fit(train)

            # ----make future dataframe
            p_period = len(test)
            future = m.make_future_dataframe(periods=p_period + period, freq=freq_key)
          #  DataTrain = DataTrain.append(test)
           # DataTrain = DataTrain.rename(columns={sales_column: 'y', date_column: 'ds'})


            # ----forecast
            forecast = m.predict(future)
            forecast_yhat_list = forecast['yhat'].tolist()
            print("forecast looped yhat")
            for i in range(len(forecast_yhat_list)):
                if forecast_yhat_list[i] < 0:
                    forecast_yhat_list[i] = 0

            print(str(forecast_yhat_list))
            forecast['yhat'] = forecast_yhat_list
            fig = m.plot(forecast)
            fig.savefig('prophetplot.png')


            plt.close(fig)

            pixmap2 = QPixmap('prophetplot.png')
            pixmap2 = pixmap2.scaled(811, 408)
            self.forecastlabel.setPixmap(pixmap2)

            # ----show output such as graphs and forecasted values for trained dataset





            # report on prophet
            #forecast_data_orig = forecast  # make sure we save the original forecast data

           # ----Show RMSE
          #  length = len(test) + period
          #  predictions = forecast_data_orig.iloc[-length:]['yhat']
           # predictions = predictions.iloc[0:len(test)]

            predicted_period = forecast.tail(period)
            predicted_period = predicted_period[['ds', 'yhat']]
            prediction_with_date = forecast.iloc[train_size:len(df2)]
            prediction_with_date = prediction_with_date[['ds', 'yhat']]

            predictions = prediction_with_date['yhat']

            print(test['sold_quantity'], "eto yung test y")
            print(str(predictions), "eto yung predictions")
           # print("Root Mean Squared Error between actual and  predicted values: ", rmse(predictions, test['sold_quantity']))
            print("Root Mean Squared Error between actual and  predicted values: ", sqrt(mean_squared_error(test['sold_quantity'], predictions)))
            print("Root Mean Squared Error between actual and  predicted values: ", mean_squared_error(test[sales_column], predictions, squared=False))
            rmse = mean_squared_error(test[sales_column], predictions, squared=False)
            mape = mean_absolute_percentage_error(test[sales_column], predictions)
            mae = mean_absolute_error(test[sales_column], predictions)
            mape = mape * 100
            print("Mean Absolute Percentage Error between actual and  predicted values: ", mape)
            print("Mean Value of Test Dataset:", test[sales_column].mean())
            rmean = test[sales_column].mean()

            # get predicted values of the given period and put in an array
            sales_prediction = predicted_period

            sales_prediction = sales_prediction.rename(columns={'ds': 'Date', 'yhat': 'Anticipated Volume'})
            array_sales = sales_prediction['Anticipated Volume'].to_numpy()





            price_prediction = get_price(array_sales)
            print(basep)
            base_price_array = []
            for i in range(len(price_prediction['expected price'])):
                base_price_array.append(basep)

            sales_prediction.reset_index(inplace=True)
            sales_prediction['Anticipated Price'] = price_prediction[
                'expected price']  # to save a copy of the original data..you'll see why shortly.

            base_price_array = pd.DataFrame(base_price_array, columns=['base price'])
            sales_prediction['base price'] = base_price_array['base price']

            # print output
            print(sales_prediction, "Eto yung sales prediction")


            # ----Show Plotly for better representation
            final_df = pd.DataFrame(forecast)
            import plotly.graph_objs as go
            import plotly.offline as py

            actual_chart = go.Scatter(y=train["y"], name='Actual')
            predict_chart = go.Scatter(y=final_df["yhat"], name='Predicted')
            predict_chart_upper = go.Scatter(y=final_df["yhat_upper"], name='Predicted Upper')
            predict_chart_lower = go.Scatter(y=final_df["yhat_lower"], name='Predicted Lower')
            py.plot([actual_chart, predict_chart, predict_chart_upper, predict_chart_lower])

            iarray = sales_prediction['Anticipated Volume'].tolist()
            sarray = sales_prediction['Anticipated Price'].tolist()
            print(iarray)
            day = 0
            total = 0
            temptotal = 0
            etotal = 0
            sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = sqlcon.cursor()
            sql = "SELECT price FROM product_table WHERE company_id = %s and product_id = %s"
            strci = (companyid, prodd)
            cur.execute(sql, strci)
            bp = float(cur.fetchone()[0])


            cur21 = sqlcon.cursor()
            sql21 = "SELECT stock FROM product_table WHERE company_id = %s AND product_id = %s"
            strci21 = (companyid, prodd)
            cur21.execute(sql21, strci21)
            stok = cur21.fetchone()[0]
            print(sarray)
            for i in range(len(iarray)):
                total = iarray[i] + total
                if float(stok) >= total:
                    if sarray[i] < bp:
                        day = day + 1
                        etotal = iarray[i] * bp
                        temptotal = etotal + temptotal
                    else:
                        day = day + 1
                        etotal = iarray[i] * sarray[i]
                        temptotal = etotal + temptotal
            cur2 = sqlcon.cursor()
            sql2 = "UPDATE product_table SET exp_valstock  = %s WHERE company_id = %s AND product_id = %s"
            strci2 = (temptotal, companyid, prodd)
            cur2.execute(sql2, strci2)

            cur3 = sqlcon.cursor()
            sql3 = "UPDATE product_table SET exp_numdate = %s WHERE company_id = %s AND product_id = %s"
            strci3 = (day, companyid, prodd)
            cur3.execute(sql3, strci3)

            print(total, "eto yung total")
            print(day, "eto yung day")

            cur4 = sqlcon.cursor()
            sql4 = "SELECT DISTINCT product_id FROM dpricing_table WHERE company_id = %s AND product_id = %s"
            strci4 = (companyid, prodd)
            cur4.execute(sql4, strci4)
            try:
                tets = cur4.fetchone()[0]
            except:
                tets = 0
            print("tapos ba dito", tets)
            sqlcon.commit()
            sqlcon.close()
            n = 0
            if prodd == tets:
                mydb3 = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur8 = mydb3.cursor()
                sql10 = "DELETE FROM dpricing_table WHERE company_id = %s AND product_id = %s;"
                strci10 = (companyid, prodd)
                cur8.execute(sql10, strci10)
                mydb3.commit()
                mydb3.close()
                for x in range(len(sarray)):
                    mydb2 = mysql.connector.connect(
                        host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                        user="uvs7rpn9lsiv2up2",
                        password="lLYwJiarRB6KUg2ObG5",
                        database="b3lupoymz85v7g9pcewp",
                        port = 21290
                    )
                    cur9 = mydb2.cursor()
                    print("or dito")
                    cur9.execute('INSERT INTO dpricing_table(product_id, company_id, anticipated_price) VALUES (%s, %s, %s)',(prodd, companyid, sarray[n]))
                    n = n+1
                    mydb2.commit()
                    mydb2.close()
            else:
                for x in range(len(sarray)):
                    mydb2 = mysql.connector.connect(
                        host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                        user="uvs7rpn9lsiv2up2",
                        password="lLYwJiarRB6KUg2ObG5",
                        database="b3lupoymz85v7g9pcewp",
                        port = 21290
                    )
                    cur9 = mydb2.cursor()
                    cur9.execute(
                        'INSERT INTO dpricing_table(product_id, company_id, anticipated_price) VALUES (%s, %s, %s)',
                        (prodd, companyid, sarray[n]))

                    n = n + 1
                    mydb2.commit()
                    mydb2.close()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Product/Dataset is not selected")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)








    def productsearchfunction(self):
        global companyid
        self.ProductTable.setRowCount(0);
        pstrsearch = self.productstextbox.text()
        try:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            pcur = mydb.cursor()
            pstrsearch = "%" + pstrsearch + "%"
            psql = "SELECT product_id, product_photo, product_name, category, stock, price FROM product_table WHERE company_id = %s AND product_name LIKE %s"
            pstrci = (companyid, pstrsearch)
            pcur.execute(psql, pstrci)
            presult = pcur.fetchall()
            tablerow = 0
            self.ProductTable.setRowCount(len(presult))
            for row in presult:
                if row[1] == None:
                    self.ProductTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.ProductTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.ProductTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.ProductTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.ProductTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.ProductTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                else:
                    self.ProductTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    image = row[1]
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(image, 'jpg')
                    label = QLabel()
                    label.setScaledContents(True)
                    label.setPixmap(pixmap)
                    self.ProductTable.setCellWidget(tablerow, 1, label)
                    self.ProductTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.ProductTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.ProductTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.ProductTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                tablerow += 1
        except Exception as e:
            print(e)

    def salessearchfunction(self):
        global companyid
        self.salesTable.setRowCount(0);
        pstrsearch = self.salestextbox.text()
        try:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            pcur = mydb.cursor()
            pstrsearch = "%" + pstrsearch + "%"
            psql = "SELECT product_table.product_id, product_table.product_photo, product_table.product_name, product_table.category, sales_table.sold_quantity, sales_table.total_sold, sales_table.date FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s AND product_table.product_name LIKE %s;"
            pstrci = (companyid, pstrsearch)
            pcur.execute(psql, pstrci)
            presult = pcur.fetchall()
            tablerow = 0
            self.salesTable.setRowCount(len(presult))
            for row in presult:
                if row[1] == None:
                    self.salesTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.salesTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.salesTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.salesTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.salesTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.salesTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.salesTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    tablerow += 1
                else:
                    self.salesTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    image = row[1]
                    pixmap2 = QtGui.QPixmap()
                    pixmap2.loadFromData(image, 'jpg')
                    label2 = QLabel()
                    label2.setScaledContents(True)
                    label2.setPixmap(pixmap2)
                    self.salesTable.setCellWidget(tablerow, 1, label2)
                    self.salesTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.salesTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.salesTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.salesTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.salesTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    tablerow += 1
        except Exception as e:
            print(e)

    def searchfunction(self):
        raw = None
        srows = None
        row = None
        try:
            self.ctcb.clear()
            self.pcb.clear()
            global companyid
            strsearch = self.stb.text()

            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            strsearch = "%" + strsearch + "%"
            sql = "SELECT DISTINCT category FROM product_table WHERE company_id = %s AND product_name LIKE %s;"
            strci = (companyid, strsearch)
            cur.execute(sql, strci)
            raw = cur.fetchall()
            print(raw)
            for row in raw:
                print(row)
                self.ctcb.addItem(str(*row))

            row = None

            mydb.close()
        except Exception as e:
            print(e)

    def searchfunction2(self):
        try:
            raw2 = None
            categvar = None
            self.pcb.clear()
            global companyid
            strsearch = self.stb.text()
            categvar = self.ctcb.currentText()
            mydb2 = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )

            cur2 = mydb2.cursor()
            sql2 = "SELECT DISTINCT product_name FROM product_table WHERE (company_id = %s AND (category = %s AND product_name LIKE %s));"
            strsearch = "%" + strsearch + "%"
            strci2 = (companyid, categvar, strsearch)
            cur2.execute(sql2, strci2)
            raw2 = cur2.fetchall()
            for row in raw2:
                print(row, "sa product to")
                self.pcb.addItem(str(*row))
        except Exception as e:
            print(e)
        mydb2.close()

    def selfunction(self):
        try:
            strp = self.pcb.currentText()
            categvar = self.ctcb.currentText()

            self.selectedpTB.setText(strp)
            prr = self.selectedpTB.text()
            prr = str(prr)
            global companyid
            strsearch = self.stb.text()

            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor(buffered=True)
            cur2 = mydb.cursor(buffered=True)
            strsearch = "%" + strsearch + "%"
            sql = "SELECT DISTINCT price FROM product_table WHERE (company_id = %s AND (category = %s AND product_name LIKE %s));"
            strci = (companyid, categvar, strsearch)
            cur.execute(sql, strci)
            price = cur.fetchone()[0]
            price2 = str(price)
            self.bptb.setText(price2)

            prr2 = str(self.pcb.currentText())
            print("eto yung prr2", prr2)
            global prodd

            sql2 = "SELECT product_id FROM product_table WHERE company_id = %s AND product_name = %s;"
            strci2 = (companyid, prr2)
            cur2.execute(sql2, strci2)
            prodd = cur2.fetchone()[0]
            print("eto yung prod", prodd)



        except Exception as e:
            print(e)

    def forecastclearfunction(self):
        self.PredRTB.clear()
        self.bptb.clear()
        self.stb.clear()
        self.selectedpTB.clear()



    def loaddashboardtable(self):


       self.dashboardtable.setRowCount(0);
       global companyid
       try:
           print("umabot ba dito")
           mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
           cur = mydb.cursor()
           sql = "SELECT product_table.product_id, product_table.product_photo, product_table.product_name, sum(sales_table.sold_quantity) FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s GROUP BY product_table.product_name ORDER BY sum(sales_table.sold_quantity) DESC;"
           strci = (companyid,)
           cur.execute(sql, strci)
           rows = cur.fetchall()

           tablerow=0
           self.dashboardtable.setRowCount(len(rows))
           for row in rows:

            if row[1] == None:
                self.dashboardtable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                self.dashboardtable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                self.dashboardtable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                self.dashboardtable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                tablerow+=1
            else:
                    self.dashboardtable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    image = row[1]
                    pixmap2 = QtGui.QPixmap()
                    pixmap2.loadFromData(image, 'jpg')
                    label2 = QLabel()
                    label2.setScaledContents(True)
                    label2.setPixmap(pixmap2)
                    self.dashboardtable.setCellWidget(tablerow, 1, label2)
                    self.dashboardtable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.dashboardtable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    tablerow += 1

       except Exception as e:
           print(e)

    def loadsalestable(self):
        self.salesTable.setRowCount(0);
        global companyid, SortVar, rawr2
        if SortVar == 0:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT sales_table.sales_id, product_table.product_photo, product_table.product_name, product_table.category, sales_table.sold_quantity, sales_table.total_sold, sales_table.date FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            rows = cur.fetchall()
            tablerow=0
            self.salesTable.setRowCount(len(rows))
            for row in rows:
                if row[1] == None:
                    self.salesTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.salesTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.salesTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.salesTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.salesTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.salesTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.salesTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))

                    tablerow+=1
                else:
                    self.salesTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    image = row[1]
                    pixmap2 = QtGui.QPixmap()
                    pixmap2.loadFromData(image, 'jpg')
                    label2 = QLabel()
                    label2.setScaledContents(True)
                    label2.setPixmap(pixmap2)
                    self.salesTable.setCellWidget(tablerow, 1, label2)
                    self.salesTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.salesTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                    self.salesTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.salesTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.salesTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    tablerow += 1
        else:
            try:
                tablerow=0
                self.salesTable.setRowCount(len(rawr2))
                for row in rawr2:
                    if row[1] == None:
                        self.salesTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                        self.salesTable.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                        self.salesTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                        self.salesTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                        self.salesTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                        self.salesTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                        self.salesTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                        tablerow += 1
                    else:
                        self.salesTable.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                        image = row[1]
                        pixmap2 = QtGui.QPixmap()
                        pixmap2.loadFromData(image, 'jpg')
                        label2 = QLabel()
                        label2.setScaledContents(True)
                        label2.setPixmap(pixmap2)
                        self.salesTable.setCellWidget(tablerow, 1, label2)
                        self.salesTable.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                        self.salesTable.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                        self.salesTable.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                        self.salesTable.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                        self.salesTable.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                        tablerow += 1
            except Exception as e:
                print(e)
class SortSalesScreen(QDialog):
    def __init__(self):
        try:
            super(SortSalesScreen, self).__init__()
            loadUi("SORTSALES.ui", self)
            self.loadcategory()
            self.CatCBOX.currentTextChanged.connect(self.sortsearchfunction)
            self.confirmsort.clicked.connect(self.sortfunction)
            self.sortsearchfunction()
        except Exception as e:
            print(e)
    def loadcategory(self):
        try:
            global companyid
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT category FROM category_table WHERE company_id = %s"
            strci = (companyid,)
            cur.execute(sql, strci)
            categresult = cur.fetchall()
            for row in categresult:
                self.CatCBOX.addItem(str(*row))

        except Exception as e:
            print(e)

    def sortsearchfunction(self):
        try:
            raw2 = None
            categvar = None
            self.cbpname.clear()
            global companyid
            categvar = self.CatCBOX.currentText()
            mydb2 = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )

            cur2 = mydb2.cursor()
            sql2 = "SELECT DISTINCT product_name FROM product_table WHERE (company_id = %s AND category = %s);"

            strci2 = (companyid, categvar)
            cur2.execute(sql2, strci2)
            raw2 = cur2.fetchall()
            print(raw2, "eto yung product names", companyid, categvar, "eto yung dalwa")
            for row in raw2:
                self.cbpname.addItem(str(*row))
        except Exception as e:
            print(e)
        mydb2.close()
    def sortfunction(self):
        global companyid, rawr2, SortVar

        try:
            sortcateg = self.CatCBOX.currentText()
            sortprodname = self.cbpname.currentText()
            sortstartdate = self.startdate.text()
            sortenddate = self.enddate.text()
            print("sila to", sortcateg, sortprodname, sortstartdate, sortenddate)
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT product_id FROM product_table WHERE (company_id = %s AND product_name = %s);"
            strci = (companyid, sortprodname)
            cur.execute(sql, strci)
            rawr = cur.fetchone()[0]

            cur2 = mydb.cursor()
            sql2 = "SELECT sales_table.sales_id, product_table.product_photo, product_table.product_name, product_table.category, sales_table.sold_quantity, sales_table.total_sold, sales_table.date FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE (sales_table.company_id = %s AND ((sales_table.date BETWEEN %s AND %s) AND sales_table.product_id = %s));"
            strci2 = (companyid, sortstartdate, sortenddate, rawr)
            cur2.execute(sql2, strci2)
            rawr2 = cur.fetchall()

            SortVar = 1

        except Exception as e:
            print(e)



        except Exception as e:
            print(e)
class RunDynamicPricingScreen(QDialog):
    def __init__(self):
        try:
            super(RunDynamicPricingScreen, self).__init__()
            loadUi("DYNAMIC-PRICING.ui", self)
            self.loadtable()
            self.loadlabel()
            self.radioButton_price.clicked.connect(self.optimalprice)
            self.radioButton_sales.clicked.connect(self.expectedsales)
            self.entersales.textChanged.connect(self.optimalprice)
            self.enterprice.textChanged.connect(self.expectedsales)
            self.dpx.clicked.connect(self.closefunction)
        except Exception as e:
            print(e)
    def loadlabel(self):
        self.oplabel.setHidden(True)
        self.eslabel.setHidden(True)
    def closefunction(self):
        try:
            self.deleteLater()
            widget5.hide()
        except Exception as e:
            print(e)

    def loadtable(self):
        global pdfpname
        try:
            del sales_prediction["index"]
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT price FROM product_table WHERE (company_id = %s AND product_name = %s);"
            strci = (companyid, pdfpname)
            cur.execute(sql, strci)
            rawr = cur.fetchone()[0]

            topl = list(sales_prediction.itertuples(index=False, name=None))

            tablerow = 0
            self.DynamicTB.setRowCount(len(sales_prediction))
            for row in topl:
                self.DynamicTB.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                #if row[1] > 0:
                self.DynamicTB.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                self.DynamicTB.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                self.DynamicTB.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(rawr)))
               # else:
               #     self.DynamicTB.setItem(tablerow, 1, QtWidgets.QTableWidgetItem("0"))
                #    self.DynamicTB.setItem(tablerow, 2, QtWidgets.QTableWidgetItem("0"))
                tablerow += 1
        except Exception as e:
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT price FROM product_table WHERE (company_id = %s AND product_name = %s);"
            strci = (companyid, pdfpname)
            cur.execute(sql, strci)
            rawr = cur.fetchone()[0]

            topl = list(sales_prediction.itertuples(index=False, name=None))

            tablerow = 0
            self.DynamicTB.setRowCount(len(sales_prediction))
            for row in topl:
                self.DynamicTB.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                # if row[1] > 0:
                self.DynamicTB.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                self.DynamicTB.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                self.DynamicTB.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(rawr)))
                # else:
                #     self.DynamicTB.setItem(tablerow, 1, QtWidgets.QTableWidgetItem("0"))
                #    self.DynamicTB.setItem(tablerow, 2, QtWidgets.QTableWidgetItem("0"))
                tablerow += 1
    def optimalprice(self):
        try:
            global intercept, slope
            if self.radioButton_price.isChecked():
                self.oplabel.setHidden(False)
                sales_input = float(self.entersales.text())
                price_output = round((sales_input - intercept) / slope, 2)
                self.oplabel.setText("Optimal Pricepoint: " + str(price_output))
            else:
                self.oplabel.setText(" ")
        except Exception as e:
            self.radioButton_price.setChecked(False)
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Invalid input for expected sales!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
    def expectedsales(self):
        try:
            global intercept, slope
            if self.radioButton_sales.isChecked():
                self.eslabel.setHidden(False)
                price_input =  float(self.enterprice.text())
                sales_output = intercept + slope * (price_input)
                self.eslabel.setText("Expected number of stocks to be sold: " + str(sales_output))

            else:
                self.eslabel.setText(" ")
        except Exception as e:
            self.radioButton_sales.setChecked(False)
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Invalid input for expected sales!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()

            print(e)
class AddCategoryScreen(QDialog):
    def __init__(self):
        super(AddCategoryScreen, self).__init__()
        loadUi("CATEGORY.ui", self)
        self.addcatconfirm.clicked.connect(self.addcategfunction)
        self.pushButton_24.clicked.connect(self.clear)

    def clear(self):
        self.categTB.clear()
    def addcategfunction(self):
        strCat = self.categTB.text()
        global companyid
        try:
            if len(strCat) == 0:
                print("Please enter a valid category name")
            else:
                sqlcon = mysql.connector.connect(
                    host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                    user="uvs7rpn9lsiv2up2",
                    password="lLYwJiarRB6KUg2ObG5",
                    database="b3lupoymz85v7g9pcewp",
                    port = 21290
                )
                cur = sqlcon.cursor()
                cur.execute('INSERT INTO category_table(company_id, category) VALUES (%s, %s)', (companyid, strCat))
                sqlcon.commit()
                sqlcon.close()
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setText("Category Added!")
                msgbox.setWindowTitle("Success!")
                msgbox.exec_()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Category already exists!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
class AddProductScreen(QDialog):

    def __init__(self):
        super(AddProductScreen, self).__init__()
        loadUi("ADDPROD.ui", self)
        self.loadcategory()
        self.clearButton.clicked.connect(self.clearfunction)
        self.confirmButton.clicked.connect(self.addprodfunction)
        #self.picButton.clicked.connect(self.addphotofunction)
        self.pclse.clicked.connect(self.closefunction)

    def closefunction(self):
        try:
            self.deleteLater()
            widget2.hide()
        except Exception as e:
            print(e)

    def addphotofunction(self):

            pic = QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'Image files (*.jpg)')
            imagepixmap = pic[0]
            pixmap = QPixmap(imagepixmap)
            global binarydata
            with open(imagepixmap, 'rb', encoding='utf-8') as file:
                binarydata = file.read()

            if pixmap != None:
                print("ok")
            else:
                print("pls pic")
            self.photoTB.setText(imagepixmap)

    def clearfunction(self):
        global binarydata
        self.prodnameTB.clear()
        self.sellpriceTB.clear()
        self.quantityTB.clear()
        binarydata is None

    def addprodfunction(self):
        try:
            global companyid, binarydata
            strProdname = self.prodnameTB.text()
            strSellprice = self.sellpriceTB.text()
            strQuantity = self.quantityTB.text()
            strCategory = self.categCB.currentText()
            print("eto values", strProdname, strCategory, strQuantity, strSellprice, companyid)
            if len(strProdname) == 0 or len(strSellprice) == 0 or len(strQuantity) == 0:
                print("Incomplete selection")
            else:
                sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur = sqlcon.cursor()
                cur.execute('INSERT INTO product_table(product_name, category, stock, price, company_id) VALUES (%s, %s, %s, %s, %s)', (strProdname, strCategory, strQuantity, strSellprice, companyid))

                sqlcon.commit()
                sqlcon.close()
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setText("Product Added!")
                msgbox.setWindowTitle("Success!")
                msgbox.exec_()
        except Exception as e:

            print(e)



    def loadcategory(self):
        try:
            global companyid
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
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
class AddSalesScreen(QDialog):
    def __init__(self):
        try:
            super(AddSalesScreen, self).__init__()
            loadUi("ADDSALES.ui", self)
            self.loadcategory()
            self.loadproductname()
            self.total2()
            self.salesQTB.textChanged.connect(self.total)
            self.salesQTB_2.textChanged.connect(self.total)
            self.clrbt.clicked.connect(self.clearfunction)
            self.salesconfirmButton.clicked.connect(self.addsalesfunction)
            self.PNCB.currentTextChanged.connect(self.total2)
            self.CatCB.currentTextChanged.connect(self.loadproductname)
            self.sclse.clicked.connect(self.closefunction)
        except Exception as e:
            print(e)
    def closefunction(self):
        try:
            self.deleteLater()
            widget4.hide()
        except Exception as e:
            print(e)
    def loadcategory(self):
        try:
            self.CatCB.clear()
            global companyid
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT DISTINCT product_table.category FROM product_table WHERE company_id = %s AND stock > 0"
            strci = (companyid,)
            cur.execute(sql, strci)
            categresult = cur.fetchall()
            for row in categresult:
                self.CatCB.addItem(str(*row))
            mydb.close()
        except Exception as e:
            print(e)
    def loadproductname(self):
        try:
            self.PNCB.clear()
            global companyid, pid, pp
            va1 = self.CatCB.currentText()

            mydb3 = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb3.cursor()
            sql = "SELECT DISTINCT product_name FROM product_table WHERE company_id = %s AND category = %s;"
            strci = (companyid, va1)
            cur.execute(sql, strci)
            categresult = cur.fetchall()
            categresults = [i[0] for i in categresult]
            print("eto yung categresults", categresults)
            print(companyid, )
            for row in categresults:
                self.PNCB.addItem(row)
        except Exception as e:

            print(e)
    def total2(self):
        try:
            global companyid, pid, pp
            mydb3 = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )

            cur2 = mydb3.cursor()
            cur3 = mydb3.cursor()
            va2 = self.PNCB.currentText()
            sql2 = "SELECT product_id FROM product_table WHERE company_id = %s AND product_name = %s;"
            strci2 = (companyid, va2)
            cur2.execute(sql2, strci2)
            pid = cur2.fetchone()[0]


            sql3 = "SELECT price FROM product_table WHERE company_id = %s AND product_id = %s;"
            strci3 = (companyid, str(pid))
            cur3.execute(sql3, strci3)
            pp = float(cur3.fetchone()[0])

            self.salesQTB_2.setText(str(pp))
            mydb3.close()
        except Exception as e:
            print(e)
    def total(self):
        try:
            global companyid
            quan = self.salesQTB.text()
            pp = float(self.salesQTB_2.text())
            tot = int(quan) * int(float(pp))
            self.salesTTB.setText(str(tot))
        except Exception as e:
            print("Dito yung error")
            print(e)
    def addsalesfunction(self):

        try:
            global companyid, pid
            #DISABLE PRODUCT NAME, PRICE,  TEXT BOX

            strSalePN = self.PNCB.currentText()
            strSalePrice = self.salesQTB_2.text()
            strSaleCat = self.CatCB.currentText()
            strSaleQuan = self.salesQTB.text()
            strSaletotal = self.salesTTB.text()
            strSaleDate = self.salesDTB.date().toPyDate()

            print(companyid, "company id")
            print(pid, "pid")
            print(strSaleDate, "Sale date")
            print(strSaleQuan, "Quantity")
            print(strSalePrice, "sale price")
            print(strSaletotal, "sale total")
            if len(strSaleQuan) == 0:
                print("Incomplete selection")
            else:
                mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur = mydb.cursor()
                sql = "SELECT stock FROM product_table WHERE company_id = %s and product_id = %s"
                strci = (companyid, pid)
                cur.execute(sql, strci)
                stk = int(cur.fetchone()[0])
                print(stk, "eto yung stk", strSaleQuan, "eto yung str quan")

                if stk >= int(strSaleQuan):
                    totaltalaga = stk - int(strSaleQuan)
                    sqlcon = mysql.connector.connect(
                        host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                    )
                    cur = sqlcon.cursor()
                    cur2 = sqlcon.cursor()
                    cur.execute(
                            'INSERT INTO sales_table(company_id, product_id, date, sold_quantity, selling_price, total_sold) VALUES (%s, %s, %s, %s, %s, %s)',
                            (companyid, pid, strSaleDate, strSaleQuan, strSalePrice, strSaletotal))

                    sql2 = "UPDATE product_table SET stock = %s WHERE company_id = %s AND product_id = %s;"
                    strci2 = (totaltalaga, companyid, pid)
                    cur2.execute(sql2, strci2)
                    sqlcon.commit()
                    sqlcon.close()
                    msgbox = QMessageBox()
                    msgbox.setIcon(QMessageBox.Information)
                    msgbox.setText("Sale record has been added!")
                    msgbox.setWindowTitle("Success!")
                    msgbox.exec_()
                    self.clearfunction()
                else:
                    msgbox = QMessageBox()
                    msgbox.setIcon(QMessageBox.Critical)
                    msgbox.setText("Sale quantity is higher than remaining stocks!")
                    msgbox.setWindowTitle("Error!")
                    msgbox.exec_()
        except Exception as e:
            print(e)
    def clearfunction(self):
        self.salesQTB.clear()
        self.loadcategory()
class EditProductScreen(QDialog):
    def __init__(self):
        try:
            super(EditProductScreen, self).__init__()
            loadUi("EDITPROD.ui", self)
            self.loadcategory()
            self.loadcells()
            self.clearButtonE.clicked.connect(self.clearfunction)
            self.confirmButtonE.clicked.connect(self.editprodfunction)
            #self.picButtonE.clicked.connect(self.addphotofunction)
            self.xbutton.clicked.connect(self.closefunction)
        except Exception as e:
            print(e)
    def closefunction(self):
        try:
            self.deleteLater()
            widget7.hide()
        except Exception as e:
            print(e)
    def loadcells(self):

        self.prodnameTBE.clear()
        self.sellpriceTBE.clear()

        global companyid, SelectedPID
        try:
            print(SelectedPID, companyid, "selid pati companyid")
            sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = sqlcon.cursor()
            cur2 = sqlcon.cursor()
            cur3 = sqlcon.cursor()
            cur4 = sqlcon.cursor()

            sql = "SELECT product_name FROM product_table WHERE company_id = %s AND product_id = %s"
            strci = (companyid, SelectedPID)
            cur.execute(sql, strci)
            PName = cur.fetchone()[0]


            sql2 = "SELECT price FROM product_table WHERE company_id = %s AND product_id = %s"
            strci2 = (companyid, SelectedPID)
            cur2.execute(sql2, strci2)
            Price = cur2.fetchone()[0]

            sql3 = "SELECT stock FROM product_table WHERE company_id = %s AND product_id = %s"
            strci3 = (companyid, SelectedPID)
            cur3.execute(sql3, strci3)
            PQuantity = cur3.fetchone()[0]


            print(PName, Price, PQuantity, "ETO RESULTS")


            self.prodnameTBE.setText(str(PName))
            self.sellpriceTBE.setText(str(Price))


        except Exception as e:
            print(e)
    def addphotofunction(self):

        pic = QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'Image files (*.jpg)')
        imagepixmap = pic[0]
        pixmap = QPixmap(imagepixmap)
        global binarydata
        with open(imagepixmap, 'rb', encoding='utf-8') as file:
            binarydata = file.read()

        if pixmap != None:
            print("ok")
        else:
            print("pls pic")
        self.photoTB.setText(imagepixmap)

    def clearfunction(self):
        global binarydata
        self.prodnameTBE.clear()
        self.sellpriceTBE.clear()

        binarydata is None

    def editprodfunction(self):

        try:
            global binarydata
            binarydata is None
            global companyid, SelectedPID
            print(SelectedPID, "SELECTEDPID TO")
            strProdname = self.prodnameTBE.text()
            strSellprice = self.sellpriceTBE.text()

            strCategory = self.categCBE.currentText()

            if len(strProdname) == 0 or len(strSellprice) == 0:
                print("Incomplete selection")
            else:
                sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur = sqlcon.cursor()
                if binarydata == None:
                    sql = "UPDATE product_table SET product_name = %s, category = %s, price = %s WHERE company_id = %s AND product_id = %s;"
                    strci = (strProdname, strCategory, strSellprice, companyid, SelectedPID)
                    cur.execute(sql, strci)
                    print("BN")
                    print(strProdname, strCategory,  strSellprice, companyid, SelectedPID)
                    sqlcon.commit()
                    sqlcon.close()
                else:
                    sql = "UPDATE product_table SET product_name = %s, category = %s, price = %s, product_photo = %s WHERE company_id = %s AND product_id = %s;"
                    strci = (strProdname, strCategory, strSellprice, binarydata, companyid, pDeleteID)
                    cur.execute(sql, strci)
                    print("BBN")
                    sqlcon.commit()
                    sqlcon.close()

            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Product information changed!")
            msgbox.setWindowTitle("Success!")
            msgbox.exec_()
        except Exception as e:
            print(e)

    def loadcategory(self):
        try:
            global companyid
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT category FROM category_table WHERE company_id = %s"
            strci = (companyid,)
            cur.execute(sql, strci)
            categresult = cur.fetchall()
            for row in categresult:
                self.categCBE.addItem(str(*row))
            print(categresult)
        except Exception as e:
            print(e)
class EditSalesScreen(QDialog):
    def __init__(self):
        try:
            super(EditSalesScreen, self).__init__()
            loadUi("EDITSALES.ui", self)
            self.loadcells()
            self.salesQTBS.textChanged.connect(self.total)
            self.salesconfirmButtonS.clicked.connect(self.saleseditfunction)
            self.clse.clicked.connect(self.closefunction)


        except Exception as e:
            print(e)

    def closefunction(self):
        try:
            self.deleteLater()
            widget8.hide()
        except Exception as e:
            print(e)

    def saleseditfunction(self):
        global companyid, SelectedSID
        try:
            totes = 0
            self.salesPNTBS.text()
            tot = self.salesTTBS.text()
            self.salesPTBS.text()
            self.dateEditS.date().toPyDate()
            quant = self.salesQTBS.text()
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            cur2 = mydb.cursor()
            cur3 = mydb.cursor()
            cur4 = mydb.cursor()
            cur5 = mydb.cursor()

            sql2 = "SELECT product_id FROM sales_table WHERE company_id = %s AND sales_id = %s"
            strci2 = (companyid, SelectedSID)
            cur2.execute(sql2, strci2)
            proid = cur2.fetchone()[0]
            print("salesid", proid)

            sql3 = "SELECT stock FROM product_table WHERE company_id = %s AND product_id = %s"
            strci3 = (companyid, proid)
            cur3.execute(sql3, strci3)
            istak = cur3.fetchone()[0]
            istakx = float(istak)
            print(istak, "istak")

            sql5 = "SELECT sold_quantity FROM sales_table WHERE company_id = %s AND sales_id = %s"
            strci5 = (companyid, SelectedSID)
            cur5.execute(sql5, strci5)
            sq = cur5.fetchone()[0]
            sqx = float(sq)
            t = 0
            if float(quant) < sqx:
                t = sqx - float(quant)
                totes = istakx + t
            else:
                t = float(quant) - sqx
                totes = istakx - t

            if float(quant) < istakx:

                if float(quant) > 0:


                    sql = "UPDATE sales_table SET sold_quantity = %s, total_sold = %s WHERE company_id = %s AND sales_id = %s;"
                    strci = (quant, tot, companyid, SelectedSID)
                    cur.execute(sql, strci)

                    sql4 = "UPDATE product_table SET stock = %s WHERE company_id = %s AND product_id = %s;"
                    strci4 = (totes, companyid, proid)
                    cur4.execute(sql4, strci4)

                    mydb.commit()
                    mydb.close()
                    msgbox = QMessageBox()
                    msgbox.setIcon(QMessageBox.Information)
                    msgbox.setText("Sale record updated!")
                    msgbox.setWindowTitle("Success!")
                    msgbox.exec_()

                else:
                    print("INVALID QUANTITY")
                    print(str(quant))
            else:
                msgbox2 = QMessageBox()
                msgbox2.setIcon(QMessageBox.Critical)
                msgbox2.setText("Sale quantity is greater than stock!")
                msgbox2.setWindowTitle("Error!")
                msgbox2.exec_()

        except Exception as e:
            print(e)
    def total(self):
        try:
            quan = self.salesQTBS.text()
            sp = self.salesPTBS.text()
            totes = float(quan) * float(sp)
            self.salesTTBS.setText(str(totes))
        except Exception as e:
            print(e)

    def loadcells(self):
        global companyid
        global SelectedSID
        self.salesPNTBS.clear()
        self.salesTTBS.clear()
        self.salesPTBS.clear()
        self.salesQTBS.clear()


        try:
            print(SelectedSID, companyid, "selid pati companyid")
            sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = sqlcon.cursor()
            cur2 = sqlcon.cursor()
            cur3 = sqlcon.cursor()
            cur4 = sqlcon.cursor()
            cur5 = sqlcon.cursor()
            cur6 = sqlcon.cursor()

            sql = "SELECT product_id FROM sales_table WHERE company_id = %s AND sales_id = %s"
            strci = (companyid, SelectedSID)
            cur.execute(sql, strci)
            SID = cur.fetchone()[0]


            sql2 = "SELECT product_name FROM product_table WHERE company_id = %s AND product_id = %s"
            strci2 = (companyid, SID)
            cur2.execute(sql2, strci2)
            Pname = cur2.fetchone()[0]


            sql3 = "SELECT total_sold FROM sales_table WHERE company_id = %s AND sales_id = %s"
            strci3 = (companyid, SelectedSID)
            cur3.execute(sql3, strci3)
            STotal = cur3.fetchone()[0]
            print(STotal, "Stotal")
            sql4 = "SELECT selling_price FROM sales_table WHERE company_id = %s AND sales_id = %s"
            strci4 = (companyid, SelectedSID)
            cur4.execute(sql4, strci4)
            SPrice = cur4.fetchone()[0]
            print(SPrice, "SPrice")
            sql5 = "SELECT sold_quantity FROM sales_table WHERE company_id = %s AND sales_id = %s"
            strci5 = (companyid, SelectedSID)
            cur5.execute(sql5, strci5)
            SQuantity = cur5.fetchone()[0]
            print(SQuantity, "SQ")
            sql6 = "SELECT date FROM sales_table WHERE company_id = %s AND sales_id = %s"
            strci6 = (companyid, SelectedSID)
            cur6.execute(sql6, strci6)
            SDate = cur6.fetchone()[0]
            print(SDate, "SDATE")


            self.salesPNTBS.setText(str(Pname))
            self.salesTTBS.setText(str(STotal))
            self.salesPTBS.setText(str(SPrice))
            self.salesQTBS.setText(str(SQuantity))
            SDate = str(SDate)
            qtd = QDate.fromString(SDate, "yyyy-MM-dd")
            self.dateEditS.setDate(qtd)


        except Exception as e:
            print(e)
class ExportSalesScreen(QDialog):
    def __init__(self):
        super(ExportSalesScreen, self).__init__()
        loadUi("EXPORTSALES.ui", self)
        self.loadcategtable()
        self.loadproductname()
        self.excateg.currentTextChanged.connect(self.loadproductname)
        self.printb.clicked.connect(self.exportprint)
    def loadcategtable(self):
        try:
            global companyid
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT DISTINCT product_table.category FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            categresult = cur.fetchall()
            for row in categresult:
                self.excateg.addItem(str(*row))
            print(categresult)
        except Exception as e:
            print(e)

    def loadproductname(self):
        try:
            self.exprod.clear()
            print("tigil")
            pname = self.excateg.currentText()
            pname = str(pname)
            global companyid
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT DISTINCT product_table.product_name FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s AND product_table.category = %s;"
            strci = (companyid, pname)
            cur.execute(sql, strci)
            categresult = cur.fetchall()
            for row in categresult:
                self.exprod.addItem(str(*row))
            print(categresult)
        except Exception as e:
            print(e)
    def exportprint(self):
        try:
            global companyid
            SR = str(self.extype.currentText())
            cat = str(self.excateg.currentText())
            PN = str(self.exprod.currentText())
            SD = str(self.Sdate.text())
            ED = str(self.Edate.text())

            pname = self.excateg.currentText()
            pname = str(pname)
            global companyid
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            if SR == "YEARLY":
                sql = "SELECT sales_table.sales_id, product_table.product_name, product_table.category, SUM(sales_table.sold_quantity) AS sold_quantity, AVG(sales_table.selling_price) AS selling_price, SUM(sales_table.total_sold) AS total_sold, MIN(YEAR(sales_table.date)) AS date FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE (sales_table.company_id = %s and product_table.product_name = %s) and date BETWEEN %s AND %s GROUP BY YEAR(date) ORDER BY YEAR(date); "
            elif SR == "MONTHLY":
                sql = "SELECT sales_table.sales_id, product_table.product_name, product_table.category, SUM(sales_table.sold_quantity) AS sold_quantity, AVG(sales_table.selling_price) AS selling_price, SUM(sales_table.total_sold) AS total_sold, MIN(sales_table.date) AS date FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE (sales_table.company_id = %s and product_table.product_name = %s) and date BETWEEN %s AND %s GROUP BY MONTH(date) ORDER BY MONTH(date);"
            elif SR == "WEEKLY":
                sql = "SELECT sales_table.sales_id, product_table.product_name, product_table.category, SUM(sales_table.sold_quantity) AS sold_quantity, AVG(sales_table.selling_price) AS selling_price, SUM(sales_table.total_sold) AS total_sold, MIN(sales_table.date) AS date FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE (sales_table.company_id = %s and product_table.product_name = %s) and date BETWEEN %s AND %s GROUP BY WEEK(date, 5) ORDER BY WEEK(date, 5);"
            elif SR == "DAILY":
                sql = "SELECT sales_table.sales_id, product_table.product_name, product_table.category, sales_table.sold_quantity, sales_table.selling_price, sales_table.total_sold, sales_table.date FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE (sales_table.company_id = %s and product_table.product_name = %s) and date BETWEEN %s AND %s ORDER BY date"
            else:
                print("error")
            strci = (companyid, PN, SD, ED)
            cur.execute(sql, strci)
            categresult = cur.fetchall()

            df = pd.DataFrame(categresult)
            headerList = ['sales_id', 'product_name', 'category', 'sold_quantity', 'selling_price', 'total_sold', 'date']
            df.to_csv('CSVfile.csv', header=headerList, index=False)
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Sales Record Created!")
            msgbox.setWindowTitle("Success!")
            msgbox.exec_()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Please double check all your fields!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
class EditRefundScreen(QDialog):
    def __init__(self):
        super(EditRefundScreen, self).__init__()
        loadUi("EDITREFUND.ui", self)
        self.loadcells()
        self.refundclse.clicked.connect(self.closefunction)
        self.refconfirmButtonS.clicked.connect(self.refundeditfunction)





    def closefunction(self):
        try:
            self.deleteLater()
            widget10.hide()
        except Exception as e:
            print(e)

    def refundeditfunction(self):
        global companyid, SelectedRID, SQuantity
        try:

            prodname = self.refundPNTBS.text()
            tot = self.refundTTBS.text()
            self.refundPTBS.text()
            self.dateEditR.date().toPyDate()
            quant = self.refundQTBS.text()
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur4 = mydb.cursor()
            sql4 = "SELECT stock FROM product_table WHERE company_id = %s AND product_name = %s"
            strci4 = (companyid, prodname)
            cur4.execute(sql4, strci4)
            stockresult = cur4.fetchone()[0]
            print("stockresult ", stockresult)

            if float(quant) > 0:
                if float(stockresult) < float(quant):
                    msgbox = QMessageBox()
                    msgbox.setIcon(QMessageBox.Critical)
                    msgbox.setText("Refund is higher than stocks!")
                    msgbox.setWindowTitle("Error!")
                    msgbox.exec_()
                elif float(stockresult) >= float(quant):
                    if float(SQuantity) > float(quant):

                        oldstock = float(stockresult)
                        newstock = float(SQuantity) - float(quant)
                        print(">")
                        totalstock = oldstock + newstock

                        mydb = mysql.connector.connect(
                            host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                            user="uvs7rpn9lsiv2up2",
                            password="lLYwJiarRB6KUg2ObG5",
                            database="b3lupoymz85v7g9pcewp",
                            port = 21290
                        )
                        cur = mydb.cursor()
                        cur2 = mydb.cursor()
                        sql = "UPDATE refund_table SET sold_quantity = %s, total_sold = %s WHERE company_id = %s AND refund_id = %s;"
                        sql2 = "UPDATE product_table SET stock = %s WHERE company_id = %s AND product_name = %s"
                        strci = (quant, tot, companyid, SelectedRID)
                        cur.execute(sql, strci)
                        print("dito ba error")
                        strci2 = (totalstock, companyid, prodname)
                        cur2.execute(sql2, strci2)

                        mydb.commit()
                        mydb.close()
                    elif float(SQuantity) <= float(quant):
                        oldstock = float(stockresult)
                        newstock = float(quant) - float(SQuantity)
                        print("<")
                        totalstock = oldstock - newstock
                        mydb = mysql.connector.connect(
                            host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                            user="uvs7rpn9lsiv2up2",
                            password="lLYwJiarRB6KUg2ObG5",
                            database="b3lupoymz85v7g9pcewp",
                            port = 21290
                        )
                        cur = mydb.cursor()
                        cur2 = mydb.cursor()
                        sql = "UPDATE refund_table SET sold_quantity = %s, total_sold = %s WHERE company_id = %s AND refund_id = %s;"
                        sql2 = "UPDATE product_table SET stock = %s WHERE company_id = %s AND product_name = %s"
                        strci = (quant, tot, companyid, SelectedRID)
                        cur.execute(sql, strci)
                        print("dito ba error")
                        strci2 = (totalstock, companyid, prodname)
                        cur2.execute(sql2, strci2)

                        mydb.commit()
                        mydb.close()


            else:
                print("INVALID QUANTITY")
                print(str(quant))
        except Exception as e:
            print(e)
    def total(self):
        try:
            quan = self.refundQTBS.text()
            sp = self.refundPTBS.text()
            totes = float(quan) * float(sp)
            self.refundTTBS.setText(str(totes))
        except Exception as e:
            print(e)

    def loadcells(self):
        global companyid, SelectedRID, SQuantity
        self.refundPNTBS.clear()
        self.refundTTBS.clear()
        self.refundPTBS.clear()
        self.refundQTBS.clear()

        try:
            print(SelectedRID, companyid, "selid pati companyid")
            sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = sqlcon.cursor()
            cur2 = sqlcon.cursor()
            cur3 = sqlcon.cursor()
            cur4 = sqlcon.cursor()
            cur5 = sqlcon.cursor()
            cur6 = sqlcon.cursor()

            sql = "SELECT product_id FROM refund_table WHERE company_id = %s AND refund_id = %s"
            strci = (companyid, SelectedRID)
            cur.execute(sql, strci)
            RID = cur.fetchone()[0]


            sql2 = "SELECT product_name FROM product_table WHERE company_id = %s AND product_id = %s"
            strci2 = (companyid, RID)
            cur2.execute(sql2, strci2)
            Pname = cur2.fetchone()[0]


            sql3 = "SELECT total_sold FROM refund_table WHERE company_id = %s AND refund_id = %s"
            strci3 = (companyid, SelectedRID)
            cur3.execute(sql3, strci3)
            STotal = cur3.fetchone()[0]
            print(STotal, "Stotal")
            sql4 = "SELECT selling_price FROM refund_table WHERE company_id = %s AND refund_id = %s"
            strci4 = (companyid, SelectedRID)
            cur4.execute(sql4, strci4)
            SPrice = cur4.fetchone()[0]
            print(SPrice, "SPrice")
            sql5 = "SELECT sold_quantity FROM refund_table WHERE company_id = %s AND refund_id = %s"
            strci5 = (companyid, SelectedRID)
            cur5.execute(sql5, strci5)
            SQuantity = cur5.fetchone()[0]
            print(SQuantity, "SQ")
            sql6 = "SELECT date FROM refund_table WHERE company_id = %s AND refund_id = %s"
            strci6 = (companyid, SelectedRID)
            cur6.execute(sql6, strci6)
            SDate = cur6.fetchone()[0]
            print(SDate, "SDATE")


            self.refundPNTBS.setText(str(Pname))
            self.refundTTBS.setText(str(STotal))
            self.refundPTBS.setText(str(SPrice))
            self.refundQTBS.setText(str(SQuantity))
            SDate = str(SDate)
            qtd = QDate.fromString(SDate, "yyyy-MM-dd")
            self.dateEditR.setDate(qtd)


        except Exception as e:
            print(e)
class ViewAccuracyScreen(QDialog):
    def __init__(self):
        try:
            super(ViewAccuracyScreen, self).__init__()
            loadUi("VIEWACCURACY.ui", self)
            self.loadData()
            self.vax.clicked.connect(self.closefunction)
        except Exception as e:
            print(e)

    def closefunction(self):
        try:
            self.deleteLater()
            widget11.hide()
        except Exception as e:
            print(e)
    def loadData(self):
        global rmse, mape, rmean, mae, rmse_reg, mse_reg, mae_reg, mape_reg
        self.tRMSE.setText(str(rmse))
        self.tMAPE.setText(str(mape))
        self.tMAE.setText(str(mae))
        MSE = float(rmse) * float(rmse)
        self.tMSE.setText(str(MSE))

        self.tRMSE_2.setText(str(rmse_reg))
        self.tMSE_2.setText(str(mse_reg))
        self.tMAE_2.setText(str(mae_reg))
        self.tMAPE_2.setText(str(mape_reg))



class NotificationScreen(QDialog):
    def __init__(self):
        try:
            super(NotificationScreen, self).__init__()
            loadUi("NOTIF.ui", self)
            self.loadData()
            self.notifx.clicked.connect(self.closefunction)
            self.NotificationTable.clicked.connect(self.highlightnotiffunction)
           # self.sendnotif()
            self.exportprintPO()

            StockArr2 = []
        except Exception as e:
            print(e)

    def sendnotif(self):
        try:

            global arrayvar, stringusername, rowsx
            sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = sqlcon.cursor()
            sql = "SELECT email FROM company_table WHERE username = %s"
            email = (stringusername,)
            cur.execute(sql, email)
            newemail = cur.fetchone()[0]
            stremail = str(newemail)



            sender_email = "sales.cast00@gmail.com"
            sender_password = "uoowwijobxdigiiy"
            rec_email = stremail
            notifmsg = "\nSales Cast is notifying you about your product stocks in: ", rowsx
            notifmsg = str(notifmsg)
            print(notifmsg)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, rec_email, notifmsg)

            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Notification has been sent to your email!")
            msgbox.setWindowTitle("Sent!")
            msgbox.exec_()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("username does not exist!")
            msgbox.setWindowTitle("Not found!")
            msgbox.exec_()
            print(e)

    def loadtable2(self):
        self.APTable.setRowCount(0);
        print("test dito")
        try:
            global companyid, SelectedNID, array_base, tots, SelectedNID2
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT anticipated_price FROM dpricing_table WHERE company_id = %s AND product_id = %s"
            strci = (companyid, SelectedNID)
            cur.execute(sql, strci)
            rowz = cur.fetchall()
            rowzt = [i[0] for i in rowz]

            cur2 = mydb.cursor()
            sql2 = "SELECT stock FROM product_table WHERE company_id = %s AND product_id = %s"
            strci2 = (companyid, SelectedNID)
            cur2.execute(sql2, strci2)
            stokk = cur.fetchone()[0]
            stokk = int(stokk)
            x=int(0)
            print(rowzt, "rowszsdasd")
            print
            print(SelectedNID2, "eto selectednid2", x, "eto x")
            SelectedNID3 = int(SelectedNID2)
            total=0

            cur3 = mydb.cursor()
            sql3 = "SELECT price FROM product_table WHERE company_id = %s AND product_id = %s"
            strci3 = (companyid, SelectedNID)
            cur3.execute(sql3, strci3)
            bp = int(cur3.fetchone()[0])


            self.APTable.setRowCount(len(rowzt))
            for row in rowzt:
                total = array_base[SelectedNID3][int(x)] + total
                if total <= stokk:
                    if row < bp:
                        self.APTable.setItem(x, 0, QtWidgets.QTableWidgetItem(str(math.floor(array_base[SelectedNID3][int(x)]))))
                        self.APTable.setItem(x, 1, QtWidgets.QTableWidgetItem(str(bp)))
                        print("napalitan")
                    else:
                        self.APTable.setItem(x, 0, QtWidgets.QTableWidgetItem(str(math.floor(array_base[SelectedNID3][int(x)]))))
                        self.APTable.setItem(x, 1, QtWidgets.QTableWidgetItem(str(row)))

                    x = x+1
                else:
                    print("eto yung pinalitan", str(row))
        except Exception as e:
            print(e)
    def highlightnotiffunction(self):
        global ndeleteID, SelectedNID, SelectedNID2
        try:
            Ncell = self.NotificationTable.selectedItems()[1]
            Ncell2 = self.NotificationTable.selectedItems()[0]
            ndeleteID = Ncell.text()
            ndeleteID2 = Ncell2.text()
            SelectedNID = ndeleteID
            SelectedNID2 = ndeleteID2
            print(ndeleteID)
            self.loadtable2()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("No item is selected")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)
    def exportprintPO(self):
        try:
            global companyid, filname, ProductArr2, StockArr2, name, array_base, row, df
            ProductArr2 = []
            StockArr2 = []
            array_base = []
            array_bases = []
            x = 0
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            cur6 = mydb.cursor()
            sql = "SELECT DISTINCT product_id FROM product_table WHERE stock<21;"
            cur.execute(sql)
            arr = cur.fetchall()
            arr = [i[0] for i in arr]

            sql = "SELECT company_name FROM company_table WHERE company_id = %s;"
            strci6 = (companyid,)
            cur6.execute(sql, strci6)
            compname = cur6.fetchone()[0]
            for row in arr:
                print("dumaan ba dito")
                filname = "ProductList" + str(x) + ".csv"
                print(filname)
                x = x + 1

                mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur = mydb.cursor()
                cur2 = mydb.cursor()
                sql = "SELECT product_table.product_name, sales_table.date, sales_table.sold_quantity, sales_table.selling_price, sales_table.sold_quantity FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s AND product_table.stock < 21 AND product_table.product_id = %s;"
                print(str(row))
                strci = (companyid, row)
                cur.execute(sql, strci)
                categresult = cur.fetchall()

                sql2 = "SELECT product_name FROM product_table WHERE company_id = %s AND product_id = %s"
                strci2 = (companyid, row)
                cur2.execute(sql2, strci2)
                prname = cur.fetchone()[0]

                df = pd.DataFrame(categresult)
                headerList = ['product_name', 'date', 'sold_quantity', 'selling_price', 'total_sold']
                print(df, "eto yung dffile")
                df.to_csv(filname, header=headerList, index=False)
                ProductArr2.append(prname)
                self.autopurchaseorder()

        except Exception as e:
            print(e)
    def autopurchaseorder(self):
        try:
            global StockArr2
            # import libraries
            import pandas as pd
            import matplotlib.pyplot as plt
            from prophet.plot import plot_plotly, plot_components_plotly
            from prophet import Prophet
            from statsmodels.tools.eval_measures import rmse
            from sklearn.metrics import mean_absolute_percentage_error
            import numpy as np

            def MAPE(Y_actual, Y_Predicted):
                mape = np.mean(np.abs((Y_actual - Y_Predicted) / Y_actual)) * 100
                return mape
            global filname, array_base, array_demand, tots, ProductA
            # define number of periods to predict
            # print("Enter number of periods to predict: ")
            periods_to_predict = 10

            # read dataset
            df = pd.read_csv(filname)

            # date pre-processing

            df = df.drop_duplicates(subset=['product_name', 'date', 'sold_quantity', 'selling_price', 'total_sold'])
            df = df.dropna()

            # extract relevant data for predictions
            df = df[["date", "sold_quantity"]]

            # rename columns for Prophet to work
            df.columns = ['ds', 'y']
            df['ds'] = pd.to_datetime(df['ds'])

            # split dataset to train and to test
            train_size = int(len(df) * .80)
            train = df[0:train_size]
            test = df[train_size:len(df)]
            # print(train)
            # print(test)

            # make predictions
            m = Prophet()
            m.fit(train)

            periods_ = len(test) + periods_to_predict
            future = m.make_future_dataframe(periods=periods_, freq='D')  # MS for monthly, H for hourly
            forecast = m.predict(future)

            # extracting yhat from forecast to replace negative values to zero
            forecast_yhat_list = forecast['yhat'].tolist()

            # print("forecast looped yhat")
            for i in range(len(forecast_yhat_list)):
                if forecast_yhat_list[i] < 0:
                    forecast_yhat_list[i] = 0

            # print(str(forecast_yhat_list))
            forecast['yhat'] = forecast_yhat_list

            # extracting predicted_period for rmse comparison
            predicted_period = forecast.tail(periods_to_predict)
            predicted_period = predicted_period[['ds', 'yhat']]
            prediction_with_date = forecast.iloc[train_size:len(df)]
            prediction_with_date = prediction_with_date[['ds', 'yhat']]

            array_demand = predicted_period['yhat'].tolist()
            print(array_demand)
            tots = math.ceil(sum(array_demand))

            array_base.append(array_demand)
            print(array_base)
            print(tots, "eto yung tots")
            StockArr2.append(tots)
            print("Eto yung array", StockArr2, ProductArr2)
        except Exception as e:
            print(e)
    def closefunction(self):
        try:
            self.deleteLater()
            widget12.hide()
        except Exception as e:
            print(e)
    def loadData(self):
        self.NotificationTable.setRowCount(0);
        try:
            global companyid, arrayvar, rowsx
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            cur2 = mydb.cursor()
            cur3 = mydb.cursor()
            cur4 = mydb.cursor()
            sql = "SELECT product_name FROM product_table WHERE company_id = %s AND stock BETWEEN 0 AND 20;"
            strci = (companyid,)
            cur.execute(sql, strci)
            rowsx = cur.fetchall()
            rowsx = [i[0] for i in rowsx]
            sql2 = "SELECT stock FROM product_table WHERE company_id = %s AND stock BETWEEN 0 AND 20;"
            strci2 = (companyid,)
            cur2.execute(sql2, strci2)
            rows2x = cur2.fetchall()
            rows2x = [i[0] for i in rows2x]
            sql3 = "SELECT product_id FROM product_table WHERE company_id = %s AND stock BETWEEN 0 AND 20;"
            strci3 = (companyid,)
            cur3.execute(sql3,strci3)
            rows3x = cur3.fetchall()
            rows3x = [i[0] for i in rows3x]
            rows = list(rowsx)
            rows2 = list(rows2x)
            rows3 = list(rows3x)
            x = 0
            arrayvar = []
            self.NotificationTable.setRowCount(len(rows))

            while x < len(rows):
                strtemp = ""

                if int(rows2[x]) <= 0:
                    strtemp = "Stocks: " + str(rows2[x]) + "     " + str(rows[x]) + " is out of stock"
                elif int(rows2[x]) > 0:
                    strtemp = "Stocks: " + str(rows2[x]) + "    " + str(rows[x]) + " is low on stocks"
                arrayvar.append(strtemp)
                self.NotificationTable.setItem(x, 0, QtWidgets.QTableWidgetItem(str(x)))
                self.NotificationTable.setItem(x, 1, QtWidgets.QTableWidgetItem(str(rows3[x])))
                self.NotificationTable.setItem(x, 2, QtWidgets.QTableWidgetItem(str(arrayvar[x])))

                x = x + 1
            print(arrayvar)

        except Exception as e:
            print(e)
class AddRefundScreen(QDialog):
    def __init__(self):
        try:
            super(AddRefundScreen, self).__init__()
            loadUi("ADDREFUND.ui", self)
            self.loadcategtable()
            self.loadproductname()
            self.refCatCB.currentTextChanged.connect(self.loadproductname)
            self.loadproductdate()
            self.refPNCB.currentTextChanged.connect(self.loadproductdate)
            self.refPNCB.currentTextChanged.connect(self.loadproductprice)
            self.refPNCB.currentTextChanged.connect(self.total)
            self.loadproductprice()
            self.refQTB.textChanged.connect(self.total)
            self.rx.clicked.connect(self.closefunction)
            self.refconfirmButton.clicked.connect(self.refundfunction)
        except Exception as e:
            print(e)

    def refundfunction(self):
        try:
            global companyid
            pname = str(self.refPNCB.currentText())
            date = str(self.refundCBD.currentText())
            baseprice = str(self.refQTB_2.text())
            tprice = str(self.refTTB.text())
            descript = str(self.rdesc.currentText())
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            cur4 = mydb.cursor()
            sql = "SELECT stock FROM product_table WHERE company_id = %s AND product_name = %s"
            sql4 = "SELECT product_id FROM product_table WHERE company_id = %s AND product_name = %s"
            strci = (companyid, pname)
            cur.execute(sql, strci)
            categresult = cur.fetchone()[0]

            strci4 = (companyid, pname)
            cur4.execute(sql4, strci4)
            categresult2 = cur4.fetchone()[0]
            prodid = str(categresult2)
            print(pname, str(categresult), "eto yung refund")
            if float(self.refQTB.text()) > float(categresult):
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Critical)
                msgbox.setText("Refund is higher than stocks!")
                msgbox.setWindowTitle("Error!")
                msgbox.exec_()
            elif float(self.refQTB.text()) <= float(categresult):
                newstock = float(self.refQTB.text())
                oldstock = float(categresult)

                totalstock = oldstock - newstock
                print(newstock, oldstock, totalstock, "stocks list")
                mydb2 = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
                )
                cur2 = mydb2.cursor()
                cur3 = mydb2.cursor()
                sql2 = "UPDATE product_table SET stock = %s WHERE company_id = %s AND product_name = %s"

                strci2 = (totalstock, companyid, pname)
                cur2.execute(sql2, strci2)

                cur3.execute(
                    'INSERT INTO refund_table(company_id, product_id, date, sold_quantity, selling_price, total_sold, description) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (companyid, prodid, date, newstock, baseprice, tprice, descript))

                mydb2.commit()
                mydb2.close()
            else:
                print("Error!")

        except Exception as e:
            print(e)
    def closefunction(self):
        try:
            self.deleteLater()
            widget13.hide()
        except Exception as e:
            print(e)

    def loadproductprice(self):
        try:
            global companyid
            self.refQTB_2.clear()
            pname = self.refPNCB.currentText()
            pname = str(pname)
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT sales_table.selling_price FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s AND product_table.product_name = %s"
            strci = (companyid,pname)
            cur.execute(sql, strci)
            categresult = cur.fetchone()[0]
            self.refQTB_2.setText(str(categresult))
        except Exception as e:
            print(e)
    def loadcategtable(self):
        try:
            global companyid
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT DISTINCT product_table.category FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s;"
            strci = (companyid,)
            cur.execute(sql, strci)
            categresult = cur.fetchall()
            for row in categresult:
                self.refCatCB.addItem(str(*row))

        except Exception as e:
            print(e)

    def loadproductname(self):
        try:
            self.refPNCB.clear()
            pname = self.refCatCB.currentText()
            pname = str(pname)
            global companyid
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT DISTINCT product_table.product_name FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s AND product_table.category = %s;"
            strci = (companyid, pname)
            cur.execute(sql, strci)
            categresult = cur.fetchall()
            for row in categresult:
                self.refPNCB.addItem(str(*row))

        except Exception as e:
            print(e)

    def loadproductdate(self):
        try:
            self.refundCBD.clear()
            pname = self.refPNCB.currentText()
            pname = str(pname)
            global companyid
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "SELECT sales_table.date FROM sales_table INNER JOIN product_table ON sales_table.product_id = product_table.product_id WHERE sales_table.company_id = %s AND product_table.product_name = %s;"
            strci = (companyid, pname)
            cur.execute(sql, strci)
            categresult = cur.fetchall()
            categresultx = [i[0] for i in categresult]
            for row in categresultx:
                self.refundCBD.addItem(str(row))
            print(categresult)
        except Exception as e:
            print(e)

    def loadcells(self):
        global companyid, SelectedRID
        print(companyid)
        mydb = mysql.connector.connect(
            host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
            user="uvs7rpn9lsiv2up2",
            password="lLYwJiarRB6KUg2ObG5",
            database="b3lupoymz85v7g9pcewp",
            port = 21290
        )
        cur = mydb.cursor()
        sql = "SELECT product_name FROM product_table WHERE company_id = %s AND stock BETWEEN 0 AND 20;"
        strci = (companyid, SelectedRID)
        cur.execute(sql, strci)
        rowsx = cur.fetchall()

    def total(self):
        try:
            quan = float(self.refQTB.text())
            pric = float(self.refQTB_2.text())
            total = quan * pric
            if len(self.refQTB.text()) < 1:
                self.refTTB.setText("0")
            else:
                self.refTTB.setText(str(total))



        except Exception as e:
            self.refTTB.setText("0")
            print(e)


class UserEditScreen(QDialog):
    def __init__(self):
        try:
            super(UserEditScreen, self).__init__()
            loadUi("EDITUSER.ui", self)
            self.loadcells()
            self.userx.clicked.connect(self.closefunction)
            self.edituserconfirm.clicked.connect(self.edituserfunc)
        except Exception as e:
            print(e)
    def closefunction(self):
        try:
            self.deleteLater()
            widget14.hide()
        except Exception as e:
            print(e)

    def loadcells(self):

        self.fname.clear()
        self.uname.clear()
        self.cname.clear()
        self.passwd.clear()
        self.emailadd.clear()
        self.confirmpass.clear()
        global companyid
        try:

            sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = sqlcon.cursor()
            cur2 = sqlcon.cursor()
            cur3 = sqlcon.cursor()
            cur4 = sqlcon.cursor()
            cur5 = sqlcon.cursor()
            cur6 = sqlcon.cursor()

            sql = "SELECT full_name FROM company_table WHERE company_id = %s"
            strci = (companyid,)
            cur.execute(sql, strci)
            FName = cur.fetchone()[0]

            sql2 = "SELECT username FROM company_table WHERE company_id = %s"
            strci2 = (companyid,)
            cur2.execute(sql2, strci2)
            Uname = cur2.fetchone()[0]

            sql3 = "SELECT company_name FROM company_table WHERE company_id = %s"
            strci3 = (companyid,)
            cur3.execute(sql3, strci3)
            CName = cur3.fetchone()[0]

            sql4 = "SELECT password FROM company_table WHERE company_id = %s"
            strci4 = (companyid,)
            cur4.execute(sql4, strci4)
            Password = cur4.fetchone()[0]

            sql5 = "SELECT email FROM company_table WHERE company_id = %s"
            strci5 = (companyid,)
            cur5.execute(sql5, strci5)
            EmailAdd = cur5.fetchone()[0]

            sql6 = "SELECT password FROM company_table WHERE company_id = %s"
            strci6 = (companyid,)
            cur6.execute(sql6, strci6)
            ConPass = cur6.fetchone()[0]

            print(FName, Uname, CName, Password, EmailAdd, ConPass)

            self.fname.setText(str(FName))
            self.uname.setText(str(Uname))
            self.cname.setText(str(CName))
            self.passwd.setText(str(Password))
            self.emailadd.setText(str(EmailAdd))
            self.confirmpass.setText(str(ConPass))
        except Exception as e:
            print(e)

    def edituserfunc(self):
        global companyid
        try:

            self.fname.text()
            self.uname.text()
            self.cname.text()
            self.passwd.text()
            self.emailadd.text()
            funame = self.fname.text()
            usename = self.uname.text()
            comname = self.cname.text()
            pswdd = self.passwd.text()
            emadd = self.emailadd.text()

            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            sql = "UPDATE company_table SET username = %s, email = %s, password = %s, full_name = %s, company_name = %s WHERE company_id = %s;"
            strci = (usename, emadd, pswdd, funame, comname, companyid)
            cur.execute(sql, strci)
            mydb.commit()
            mydb.close()
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("User information has been updated!")
            msgbox.setWindowTitle("Success!")
            msgbox.exec_()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Information Error!")
            msgbox.setWindowTitle("Error!")
            msgbox.exec_()
            print(e)

class AddOrderScreen(QDialog):

    def __init__(self):

        super(AddOrderScreen, self).__init__()
        loadUi("CREATEORDER.ui", self)
        self.orderCB()
        self.OconfirmButton.clicked.connect(self.addOrder)
        self.rx.clicked.connect(self.closefunction)
        self.Oclear.clicked.connect(self.closefunction)

    def orderCB(self):

        mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
        cur = mydb.cursor()
        sql = "SELECT product_name FROM product_table WHERE company_id = %s;"
        strci = (companyid,)
        cur.execute(sql, strci)
        VAR001 = cur.fetchall()
        prodresults = [i[0] for i in VAR001]

        for row in prodresults:
            self.prodAdd.addItem(row)

    def addOrder(self):

        global companyid
        OProd = str(self.prodAdd.currentText())
        today = date.today()
        d2 = today.strftime("%Y-%m-%d")
        OQty = str(self.qtyAddOrder.text())


        sqlcon = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
        )

        cur = sqlcon.cursor()
        sql = "SELECT product_id FROM product_table WHERE product_name = %s AND company_id = %s;"
        strci = (OProd, companyid)
        cur.execute(sql, strci)
        OPID = cur.fetchone()[0]

        cur2 = sqlcon.cursor()
        cur2.execute('INSERT INTO order_table(product_id, company_id, order_placedate, order_quantity) VALUES (%s, %s, %s, %s)', (OPID, companyid, d2, OQty))
        sqlcon.commit()
        sqlcon.close()
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setText("Order has been placed!")
        msgbox.setWindowTitle("Success!")
        msgbox.exec_()
    def closefunction(self):
        try:
            self.deleteLater()
            widget15.hide()
        except Exception as e:
            print(e)

    def clearfunction(self):
        self.qtyAddOrder.clear()

class NewRefundScreen(QDialog):
    def __init__(self):
        try:
            super(NewRefundScreen, self).__init__()
            loadUi("SALESREFUND.ui", self)
            self.loaddata()
            self.RefundSalesconfirmButton.clicked.connect(self.confirmb)
            self.rrclse.clicked.connect(self.closefunction)
        except Exception as e:
            print(e)
    def closefunction(self):
        try:
            self.deleteLater()
            widget16.hide()
        except Exception as e:
            print(e)
    def loaddata(self):
        self.refundReason.clear()
        self.refundReason.addItem("Defective")
        self.refundReason.addItem("Wrong Item")

    def confirmb(self):
        try:
            qtref = float(self.qtyRefund.text())
            rr = str(self.refundReason.currentText())
            global companyid, SelectedSID
            tester = 0
            mydb = mysql.connector.connect(
                host="b3lupoymz85v7g9pcewp-mysql.services.clever-cloud.com",
                user="uvs7rpn9lsiv2up2",
                password="lLYwJiarRB6KUg2ObG5",
                database="b3lupoymz85v7g9pcewp",
                port = 21290
            )
            cur = mydb.cursor()
            cur1 = mydb.cursor()
            cur2 = mydb.cursor()
            cur3 = mydb.cursor()
            cur4 = mydb.cursor()
            cur5 = mydb.cursor()
            cur6 = mydb.cursor()
            sql = "SELECT sales_id FROM refund_table WHERE company_id = %s AND sales_id = %s"
            strci = (companyid, SelectedSID)
            cur.execute(sql, strci)
            try:
                tester = cur.fetchone()[0]
            except:
                tester = 0
            sql1 = "SELECT sold_quantity FROM sales_table WHERE company_id = %s AND sales_id = %s;"
            strci1 = (companyid, SelectedSID)
            cur1.execute(sql1, strci1)
            soldq = cur1.fetchone()[0]
            soldqx = float(soldq)

            sql2 = "SELECT product_id FROM sales_table WHERE company_id = %s AND sales_id = %s"
            strci2 = (companyid, SelectedSID)
            cur2.execute(sql2, strci2)
            prodid = cur2.fetchone()[0]

            sql3 = "SELECT date FROM sales_table WHERE company_id = %s AND sales_id = %s"
            strci3 = (companyid, SelectedSID)
            cur3.execute(sql3, strci3)
            saledat = cur3.fetchone()[0]
            saledate = str(saledat)

            sql4 = "SELECT selling_price FROM sales_table WHERE company_id = %s AND sales_id = %s"
            strci4 = (companyid, SelectedSID)
            cur4.execute(sql4, strci4)
            salepric = cur4.fetchone()[0]
            saleprice = str(salepric)

            totals = qtref * float(saleprice)

            if soldqx >= qtref:
                if tester == 0:
                    cur5.execute('INSERT INTO refund_table(company_id, product_id, sales_id, date, sold_quantity, selling_price, total_sold, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                                 ,(companyid, prodid, SelectedSID, saledate, qtref, saleprice, str(totals), rr))
                    mydb.commit()
                    mydb.close()
                else:
                    msgbox = QMessageBox()
                    msgbox.setIcon(QMessageBox.Critical)
                    msgbox.setText("You have already refunded this Item")
                    msgbox.setWindowTitle("Error!")
                    msgbox.exec_()
            else:
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Critical)
                msgbox.setText("Refund Amount Error!")
                msgbox.setWindowTitle("Error!")
                msgbox.exec_()
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Item has been refunded!")
            msgbox.setWindowTitle("Success!")
            msgbox.exec_()
        except Exception as e:
            print(e)
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget2 = QtWidgets.QStackedWidget()
widget3 = QtWidgets.QStackedWidget()
widget4 = QtWidgets.QStackedWidget()
widget5 = QtWidgets.QStackedWidget()
widget6 = QtWidgets.QStackedWidget()
widget7 = QtWidgets.QStackedWidget()
widget8 = QtWidgets.QStackedWidget()
widget9 = QtWidgets.QStackedWidget()
widget10 = QtWidgets.QStackedWidget()
widget11 = QtWidgets.QStackedWidget()
widget12 = QtWidgets.QStackedWidget()
widget13 = QtWidgets.QStackedWidget()
widget14 = QtWidgets.QStackedWidget()
widget15 = QtWidgets.QStackedWidget()
widget16 = QtWidgets.QStackedWidget()
widget.show()
app.exec()
