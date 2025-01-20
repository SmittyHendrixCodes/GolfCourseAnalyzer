# This is the main file for analyzing data from golf courses to determine feasibility of tyheir handicap vs. the type of course. Other data provided as well

from threading import Thread
from tabulate import tabulate
import math
import sys
import json
import time
import sqlite3
from numbers import Number
import pandas as pd
import numpy as np
import datetime
from collections import defaultdict
import random
import string
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QWidget, QPushButton, QLabel, QLineEdit, QFormLayout, QHBoxLayout, QVBoxLayout, QSizePolicy, QTableView, QTableWidget, QTableWidgetItem, QButtonGroup, QHeaderView, QSpacerItem
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer, QObject, QAbstractTableModel, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWebEngineWidgets import QWebEngineView
# from sqlalchemy import create_engine

# Global Variables
db_file = "GolfCourses.db"

class AddGolferBioWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.bg_image = loadBGImage()
        self.bgImageLabel = QLabel(self)
        # self.bg_image = QPixmap(r"C:\Users\Smitty Hendrix\Documents\Coding\GolfDataAnalysis\golfappbg.png")

        self.nameLabel = QLabel("Name")
        self.nameText = QLineEdit()
        self.ageLabel = QLabel("Age")
        self.ageText = QLineEdit()
        self.nationLabel = QLabel("Nationality")
        self.nationText = QLineEdit()
        self.heightLabel = QLabel("Height (cm)")
        self.heightText = QLineEdit()
        self.weightLabel = QLabel("Weight (kg)")
        self.weightText = QLineEdit()
        self.handLabel = QLabel("Handedness")
        self.handText = QLineEdit()
        self.dataFormLayout = QFormLayout()
        self.dataFormContainer = QWidget()
        self.inputWindow = QWidget()
        self.mainLayout = QVBoxLayout()
        self.buttonLayout = QVBoxLayout()
        self.addPlayerButton = QPushButton("Add Golfer")
        self.backButton = QPushButton("Back")
        
        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Add Golfer Biography')

        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        
        self.addPlayerButton.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.nameText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.nameText.setPlaceholderText("Enter Golfer")
        self.ageText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.ageText.setPlaceholderText("Enter Age")
        self.nationText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.nationText.setPlaceholderText("Enter Nationality")
        self.heightText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.heightText.setPlaceholderText("Enter Height in cm")
        self.weightText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.weightText.setPlaceholderText("Enter Weight in kg")
        self.handText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.handText.setPlaceholderText("Enter Preferred Handedness")

        self.nameLabel.setStyleSheet("font-size: 17px; color: blue; font-family: Arial;")
        self.ageLabel.setStyleSheet("font-size: 17px; color: blue; font-family: Arial;")
        self.nationLabel.setStyleSheet("font-size: 17px; color: blue; font-family: Arial;")
        self.heightLabel.setStyleSheet("font-size: 17px; color: blue; font-family: Arial;")
        self.weightLabel.setStyleSheet("font-size: 17px; color: blue; font-family: Arial;")
        self.handLabel.setStyleSheet("font-size: 17px; color: blue; font-family: Arial;")

        self.addPlayerButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addPlayerButton.setMaximumSize(200, 50)
        self.addPlayerButton.setMinimumSize(100, 33)
        self.addPlayerButton.clicked.connect(self.clickAddGolfer)
        self.addPlayerButton.setStyleSheet("font-size: 12px; font-family: Arial;")

        self.backButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.backButton.setMinimumSize(100, 25)
        self.backButton.setMaximumSize(200, 25)
        self.backButton.clicked.connect(self.clickBackButton)
        self.backButton.setStyleSheet("font-size: 12px; font-family: Arial;")

        for lineEdit in [self.nameText, self.ageText, self.nationText, self.heightText, self.weightText, self.handText]:
            lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            lineEdit.setMinimumSize(200, 25)
            lineEdit.setMaximumSize(250, 33)
            lineEdit.setStyleSheet("font-size: 12px; font-family: Arial;")

        self.dataFormLayout.addRow(self.nameLabel, self.nameText)
        self.dataFormLayout.addRow(self.ageLabel, self.ageText)
        self.dataFormLayout.addRow(self.nationLabel, self.nationText)
        self.dataFormLayout.addRow(self.heightLabel, self.heightText)
        self.dataFormLayout.addRow(self.weightLabel, self.weightText)
        self.dataFormLayout.addRow(self.handLabel, self.handText)

        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.addPlayerButton, alignment=Qt.AlignCenter)
        self.buttonLayout.addWidget(self.backButton, alignment=Qt.AlignCenter)
        self.buttonLayout.addStretch(1)
        
        self.dataFormContainer.setLayout(self.dataFormLayout)

        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.dataFormContainer, alignment=Qt.AlignCenter)
        self.mainLayout.addLayout(self.buttonLayout)
        self.mainLayout.addStretch(1)

        self.inputWindow.setLayout(self.mainLayout)
        self.setCentralWidget(self.inputWindow)

        self.show()    
    
    def getGolferBio(self):
        golfer_bio = []
        
        randomNum = random.randint(1, 999)
        randomLet1 = random.choice(string.ascii_uppercase)
        randomLet2 = random.choice(string.ascii_uppercase)
        randomLet3 = random.choice(string.ascii_uppercase)
        randomLetMult = str(randomLet1) + str(randomLet2) + str(randomLet3)
        
        id = f"{randomLetMult}{randomNum}"
        name = self.nameText.text()
        age = self.ageText.text()
        nation = self.nationText.text()
        height = self.heightText.text()
        weight = self.weightText.text()
        hand = self.handText.text()

        golfer_bio.append({
            'ID': id,
            'Name': name, 
            'Age': age, 
            'Nation': nation, 
            'Height': height, 
            'Weight': weight, 
            'Hand': hand})
        
        print(golfer_bio)

        return golfer_bio

    def storePlayerBio(self):
        global db_file
        
        conn, cursor = dbConnPlayers()
        
        golfer_bio = self.getGolferBio()     
        print(golfer_bio)

        createPlayersTable = """    
        CREATE TABLE IF NOT EXISTS PlayerBio (
            ID TEXT PRIMARY KEY,
            Name TEXT, 
            Age REAL, 
            Nation TEXT, 
            Height REAL, 
            Weight REAL, 
            Hand TEXT
        );
        """
        store_bio = """
        INSERT OR IGNORE INTO PlayerBio (ID, Name, Age, Nation, Height, Weight, Hand)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """

        try:
            cursor.execute(createPlayersTable)
            print('PlayerBio table checked/created')

        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            
        for golfer in golfer_bio:
            try:
                cursor.execute(store_bio, (
                    golfer['ID'],
                    golfer['Name'],
                    golfer['Age'],
                    golfer['Nation'],
                    golfer['Height'],
                    golfer['Weight'],
                    golfer['Hand'],
                ))
                print(f"Golfer {golfer['Name']} added successfully")
            except sqlite3.Error as e:
                print(f"Error adding player: {golfer['Name']}, Error: {e}")
        conn.commit()
        conn.close()

    def clickAddGolfer(self):
        self.storePlayerBio()
        
        self.nameText.clear()
        self.ageText.clear()
        self.nationText.clear()
        self.heightText.clear()
        self.weightText.clear()
        self.handText.clear()

    def clickBackButton(self):
        self.close()

    def resizeEvent(self, event):
    
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()

        # Pull buttons forward
        self.addPlayerButton.raise_()

        super().resizeEvent(event)

    class Data:
        #Inner Class
        def readData(self, data):
            print("All data on THE GOLFERS NAME has been pulled.")
            print(data)

class Course:
    def __init__(self, course, cType, yardage, slope, rating):

        self.course = course
        self.cType = cType
        self.yardage = yardage
        self.slope = slope
        self.rating = rating

    def __str__(self):
        return f"Course Name: {self.course}/n cType: {self.cType}/n Yardage: {self.yardage}/n Slope: {self.slope}/n Rating: {self.rating}/n"

class MenuWindow(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.addCourseButton = QPushButton("Add Course", self)
        self.checkCourseDBButton = QPushButton("Courses Database", self)
        self.checkCourseDifficultyButton = QPushButton("Check Difficulty", self)
        self.exitButton = QPushButton("Exit", self)     
        self.golferWindowButton = QPushButton("Golfer Database", self)
       
        self.bg_image = loadBGImage()
        self.bgImageLabel = QLabel(self)
        # self.bg_image = QPixmap(r"C:\Users\Smitty Hendrix\Documents\Coding\GolfDataAnalysis\golfappbg.png")

        self.buttonStack = QVBoxLayout() 
        self.menuWindow = QWidget()

        self.initUI()

    # Don't look at this bullhonky
    #class ParabolaWidget(QWidget):
        def __init__(self):
            super().__init__()            
            self.color_step = 0
            # self.colors = [Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.cyan, Qt.magenta]
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_color)
            self.timer.start(30)
        
        def update_color(self):
            self.color_step = (self.color_step + 10) % 1536
            self.update()

        def paintEvent(self, event):
            qp = QPainter()
            qp.begin(self)
            self.draw_parabola(qp)
            qp.end()

        def calc_rgb(self, step):
            if step < 256:
                return 255, step, 0 # Red to Green 
            elif step < 512:
                return 511 - step, 255, 0 # Green to Yellow 
            elif step < 768:
                return 0, 255, step - 512 # Yellow to Blue 
            elif step < 1024:
                return 0, 1023 - step, 255 # Blue to Cyan 
            elif step < 1280:
                return step - 1024, 0, 255 # Cyan to Magenta 
            else:
                return 255, 0, 1535 - step # Magenta to Red 

        def draw_parabola(self, qp):
            width = self.width()
            height = self.height()
            for x in range(-width // 2, width // 2):
                step = (self.color_step + x) % 1536
                r, g, b = self.calc_rgb(step)                         
                color = QColor(r, g, b)
                pen = QPen(color, 25) # set color and pen thickness
                qp.setPen(pen)

                # Parabola equation
                y = (x ** 2) // 100 
                qp.drawPoint(x + width//2, height//2 - y)


    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Main Menu')

        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # parabolaWindow = QWidget(self)
        # self.setCentralWidget(parabolaWindow)
        # self.parabolaLayout = QVBoxLayout(parabolaWindow)
        # self.parabolaWidget = self.ParabolaWidget()
        # self.parabolaLayout.addWidget(self.parabolaWidget)
        # parabolaWindow.setLayout(self.parabolaLayout)
        # self.resizeEvent(None)

        # Button Clicked Actions
        self.addCourseButton.clicked.connect(self.clickAddCourse)
        self.checkCourseDBButton.clicked.connect(self.clickCheckCourseDB)
        self.golferWindowButton.clicked.connect(self.clickGolferButton)
        self.checkCourseDifficultyButton.clicked.connect(self.clickCheckDifficulty)
        self.exitButton.clicked.connect(self.clickExit)

        for button in [self.addCourseButton, self.checkCourseDBButton, self.checkCourseDifficultyButton, self.golferWindowButton]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumSize(133, 25)
            button.setMaximumSize(150, 50)
            button.setStyleSheet("font-size: 12px; font-family: Arial;")
        self.exitButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.exitButton.setMinimumSize(75, 25)
        self.exitButton.setMaximumSize(150, 33)

        self.buttonStack.stretch(1)
        self.buttonStack.addWidget(self.addCourseButton)
        self.buttonStack.addWidget(self.checkCourseDBButton)
        self.buttonStack.addWidget(self.golferWindowButton)
        self.buttonStack.addWidget(self.checkCourseDifficultyButton)
        self.buttonStack.addWidget(self.exitButton)
        self.buttonStack.stretch(1)
        self.buttonStack.setAlignment(Qt.AlignHCenter)

        self.menuWindow.setLayout(self.buttonStack)
        self.setCentralWidget(self.menuWindow)

        self.show()

    def clickAddCourse(self):
        self.addCourseWindow = AddCourseWindow()
        self.addCourseWindow.show()

    def clickCheckCourseDB(self):
        self.courseDBWindow = CourseDatabaseWindow()
        self.courseDBWindow.show()

    def clickCheckDifficulty(self):
        self.difficultyWindow = DifficultyWindow()
        self.difficultyWindow.show()

    def clickGolferButton(self):
        self.golferDB = GolferDataWindow()
        self.golferDB.show()

    def clickExit(self):
        sys.exit()

    def resizeEvent(self, event):
        
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()

        # Pull parabola to front
        # self.parabolaWidget.raise_()

        # Pull buttons forward
        self.addCourseButton.raise_()
        self.checkCourseDBButton.raise_()
        self.checkCourseDifficultyButton.raise_()
        self.exitButton.raise_()

        super().resizeEvent(event)

class AddCourseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.bgImageLabel = QLabel(self)
        self.bg_image = loadBGImage()

        self.addCourseButton = QPushButton("Add Course")
        self.backButton = QPushButton("Back")
        self.courseNameLabel = QLabel("Course Name: ")
        self.courseNameText = QLineEdit()
        self.courseTypeLabel = QLabel("Type: ")
        self.courseTypeText = QLineEdit()
        self.courseYardageLabel = QLabel("Yardage: ")
        self.courseYardageText = QLineEdit()
        self.courseSlopeLabel = QLabel("Slope: ")
        self.courseSlopeText = QLineEdit()
        self.courseRatingLabel = QLabel("Rating: ")
        self.courseRatingText = QLineEdit()
        
        self.addCourseWindow = QWidget()
        self.addCourseLayout = QFormLayout()
        self.mainLayout = QVBoxLayout()

        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Add Course')

        self.addCourseButton.setStyleSheet("font-size: 15px;")
        self.addCourseButton.setFixedSize(100, 33)
        self.addCourseButton.clicked.connect(self.clickAddCourse)

        self.backButton.setStyleSheet("font-size: 15px;")
        self.backButton.setFixedSize(75, 25)
        self.backButton.clicked.connect(self.clickBackButton)
        
        self.courseNameLabel.setStyleSheet("font-size: 15px; color: blue; font-family: Arial;")                                            
        self.courseNameText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.courseNameText.setPlaceholderText("Name of Course")
        self.courseTypeLabel.setStyleSheet("font-size: 15px; color: blue; font-family: Arial;")
        self.courseTypeText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.courseTypeText.setPlaceholderText("Type of Grass")
        self.courseYardageLabel.setStyleSheet("font-size: 15px; color: blue; font-family: Arial;")
        self.courseYardageText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.courseYardageText.setPlaceholderText("Course Length")
        self.courseSlopeLabel.setStyleSheet("font-size: 15px; color: blue; font-family: Arial;")
        self.courseSlopeText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.courseSlopeText.setPlaceholderText("Course Slope")
        self.courseRatingLabel.setStyleSheet("font-size: 15px; color: blue; font-family: Arial;")     
        self.courseRatingText.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.courseRatingText.setPlaceholderText("Course Rating")

        self.addCourseLayout.addRow(self.courseNameLabel, self.courseNameText)
        self.addCourseLayout.addRow(self.courseTypeLabel, self.courseTypeText)
        self.addCourseLayout.addRow(self.courseYardageLabel, self.courseYardageText)
        self.addCourseLayout.addRow(self.courseSlopeLabel, self.courseSlopeText)
        self.addCourseLayout.addRow(self.courseRatingLabel, self.courseRatingText)
        self.addCourseLayout.setFormAlignment(Qt.AlignCenter)
        
        self.addCourseLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.addCourseLayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        self.addCourseLayout.setLabelAlignment(Qt.AlignLeft)

        addCourseButtonLayout = QHBoxLayout()
        addCourseButtonLayout.addStretch(1)
        addCourseButtonLayout.addWidget(self.backButton)
        addCourseButtonLayout.addWidget(self.addCourseButton)
        addCourseButtonLayout.addStretch(1)
        
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.addCourseLayout)
        self.mainLayout.addLayout(addCourseButtonLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.setAlignment(Qt.AlignHCenter)

        self.addCourseWindow.setLayout(self.mainLayout)
        self.setCentralWidget(self.addCourseWindow)

        self.show()

    # This will need to be updated to be able to send information to the data dictionaries to connect to SQLite3    
    def clickAddCourse(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "GolfCourses.db")        
        
        self.addCourses(db_path)
        ###
        # check_entry = checkEntry(storeCourse)
        # try:
        #     if storeCourse:
        #         if check_entry is None:
        #             addCourses(storeCourse)
        #         else:
        #             raise Exception('\nThis course data already exists in the database. You can check the database using menu option "2". ')     
        #     else:
        #         print("\nNo courses to add.")
        # except Exception as e:
        #     print(e)
        # checkTable()
        
        self.courseNameText.clear()
        self.courseTypeText.clear()
        self.courseYardageText.clear()
        self.courseSlopeText.clear()
        self.courseRatingText.clear()

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        super().resizeEvent(event)

    def storeCourseDictList(self):
        courseDictList = []
        
        courseNameText = self.courseNameText.text()
        courseTypeText = self.courseTypeText.text()
        courseYardageText = self.courseYardageText.text()
        courseSlopeText = self.courseSlopeText.text()
        courseRatingText = self.courseRatingText.text()
        

        courseDictList.append({
        'Course': courseNameText,
        'Type': courseTypeText,
        'Yardage': courseYardageText,
        'Slope': courseSlopeText,
        'Rating': courseRatingText
        })

        return courseDictList
    
    def addCourses(self, db_path):
    # Inserts a new course into the Courses table."""
        conn, cursor = dbConnCourses(db_path)
        courseDictList = self.storeCourseDictList()

        add_courses = """
        INSERT OR IGNORE INTO Courses (CourseName, Type, Yardage, Slope, Rating)
        VALUES (?, ?, ?, ?, ?);
        """

        for course in courseDictList:

            try:
                cursor.execute(add_courses, (
                    course['Course'],
                    course['Type'],
                    course['Yardage'],
                    course['Slope'],
                    course['Rating'],
                ))
                
            except sqlite3.Error as e:
                print(f"Error adding courses: {course['Course']}, Error: {e}")

        conn.commit()
        conn.close()
        print("All courses have been successfully added to the database.")

    def clickBackButton(self):
        self.close()

class CourseDatabaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.courseDBWindow = QWidget(self)
        self.DBLayout = QVBoxLayout()
        self.tableWidget = QTableWidget()

        # Background image
        self.bgImageLabel = QLabel(self)
        self.bg_image = loadBGImage()
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Course Database')

        self.courseDBWindow.setLayout(self.DBLayout)
        self.setCentralWidget(self.courseDBWindow)
        
        self.DBLayout.addWidget(self.tableWidget)

        data = self.showCourses()
        if data == None:
            print("failed to retrieve data.")
            return
        
    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.tableWidget.setGeometry(100, 100, 400, 100)

        # Push image to back
        self.bgImageLabel.lower()

        # Pull table forward
        self.tableWidget.raise_()

        super().resizeEvent(event)

    def showCourses(self):
        try:
        
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "GolfCourses.db")

            print("Connecting to db...")
            time.sleep(0.5)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                print("Connected...")
                time.sleep(0.25)
                
                print("Performing Query...")
                time.sleep(0.25)

                show_courses = """
                SELECT * FROM Courses;
                """

                cursor.execute(show_courses)
                data = cursor.fetchall()

                print("Query executed successfully...")
                time.sleep(0.25)

                if not data:
                    print("No data found in Courses table.")
                    return

                headers = ["Course", "Type", "Yardage", "Slope", "Rating"]
                
                self.tableWidget.setColumnCount(len(headers))
                self.tableWidget.setHorizontalHeaderLabels(headers)
                self.tableWidget.setRowCount(len(data))

                for rowIndex, rowData in enumerate(data):
                    for columnIndex, columnData in enumerate(rowData):
                        self.tableWidget.setItem(rowIndex, columnIndex, QTableWidgetItem(str(columnData)))

                print("Table widget popoulated with data...")
                time.sleep(0.5)                
                print("Cursor closed...")
                time.sleep(0.25)
                print("Connection closed...")
                return data
                
        except sqlite3.Error as e:
            print(f"An error occured: {e}")
            return None

class AddGolferAttributesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bgImageLabel = QLabel(self)
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bg_image = loadBGImage()
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.addAttributesButton = QPushButton("Add Golfer Attributes")
        self.backButton = QPushButton("Back")
        self.attributesForm = QFormLayout()
        self.golferIDLabel = QLabel("Golfer ID")
        self.driveDistanceLabel = QLabel("Driving Distance:")
        self.driveAccuracyLabel = QLabel("Driving Accuracy:")
        self.approach50to100Label = QLabel("Approach 50-100yds:")
        self.approach100to150Label = QLabel("Approach 100-150yds:")
        self.approach150to200Label = QLabel("Approach 150-200yds:")
        self.approach200Label = QLabel("Approach 200+ yds:")
        self.atgFairwayLabel = QLabel("Fairway to Green:")
        self.atgRoughLabel = QLabel("Rough to Green:")
        self.atgBunkerLabel = QLabel("Bunker to Green:")
        self.putting2to5Label = QLabel("Putts 2-5ft:")
        self.putting5to30Label = QLabel("Putts 5-30ft:")
        self.putting30Label = QLabel("Putts 30+ft:")
        self.golferIDText = QLineEdit()
        self.driveDistanceText = QLineEdit()
        self.driveAccuracyText = QLineEdit()
        self.approach50to100Text = QLineEdit()
        self.approach100to150Text = QLineEdit()
        self.approach150to200Text = QLineEdit()
        self.approach200Text = QLineEdit()
        self.atgFairwayText = QLineEdit()
        self.atgRoughText = QLineEdit()
        self.atgBunkerText = QLineEdit()
        self.putting2to5Text = QLineEdit()
        self.putting5to30Text = QLineEdit()
        self.putting30Text = QLineEdit()
        
        self.mainWidget = QWidget()
        self.formLayout = QFormLayout()
        self.hBox = QHBoxLayout()
        self.vBox = QVBoxLayout()
        self.mainLayout = QVBoxLayout()

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 750, 400)
        self.setWindowTitle('Add Golfer Attributes') 

        self.golferIDText.setPlaceholderText("Enter Golfer ID")
        self.driveDistanceText.setPlaceholderText("Average Driving Distance")
        self.driveAccuracyText.setPlaceholderText("Fairway Finder Accuracy")
        self.approach50to100Text.setPlaceholderText("Accuracy in")
        self.approach100to150Text.setPlaceholderText("Accuracy in")
        self.approach150to200Text.setPlaceholderText("Accuracy in")
        self.approach200Text.setPlaceholderText("Accuracy in")
        self.atgFairwayText.setPlaceholderText("Accuracy from Fairway to Green")
        self.atgRoughText.setPlaceholderText("Accuracy from Rough to Green")
        self.atgBunkerText.setPlaceholderText("Accuracy from Bunker to Green")
        self.putting2to5Text.setPlaceholderText("Accuracy of 2-5ft. Putts")
        self.putting5to30Text.setPlaceholderText("Accuracy of 5-30ft. Putts")
        self.putting30Text.setPlaceholderText("Accuracy of 30+ft. Putts")

        for lineEdit in [self.golferIDText, 
                        self.driveDistanceText, 
                        self.driveAccuracyText, 
                        self.approach50to100Text,
                        self.approach100to150Text,
                        self.approach150to200Text,
                        self.approach200Text,
                        self.atgFairwayText,
                        self.atgRoughText,
                        self.atgBunkerText,
                        self.putting2to5Text,
                        self.putting5to30Text,
                        self.putting30Text]:
            lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding,)
            lineEdit.setMaximumSize(400, 25)
            lineEdit.setMinimumSize(150, 20)
            lineEdit.setStyleSheet("font-size: 14px; font-family: Arial;")

        self.addAttributesButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addAttributesButton.setMaximumSize(200, 75)
        self.addAttributesButton.setMinimumSize(150, 50)
        self.addAttributesButton.clicked.connect(self.clickAddAttributesButton)
        self.addAttributesButton.setStyleSheet("font-size: 12px; font-family: Arial;")

        self.backButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.backButton.setMinimumSize(150, 25)
        self.backButton.setMaximumSize(200, 33)
        self.backButton.clicked.connect(self.clickBackButton)
        self.backButton.setStyleSheet("font-size: 12px; font-family: Arial;")

        self.formLayout.addRow(self.golferIDLabel, self.golferIDText)
        self.formLayout.addRow(self.driveDistanceLabel, self.driveDistanceText)
        self.formLayout.addRow(self.driveAccuracyLabel, self.driveAccuracyText)
        self.formLayout.addRow(self.approach50to100Label, self.approach50to100Text)
        self.formLayout.addRow(self.approach100to150Label, self.approach100to150Text)
        self.formLayout.addRow(self.approach150to200Label, self.approach150to200Text)
        self.formLayout.addRow(self.approach200Label, self.approach200Text)
        self.formLayout.addRow(self.atgFairwayLabel, self.atgFairwayText)
        self.formLayout.addRow(self.atgRoughLabel, self.atgRoughText)
        self.formLayout.addRow(self.atgBunkerLabel, self.atgBunkerText)
        self.formLayout.addRow(self.putting2to5Label, self.putting2to5Text)
        self.formLayout.addRow(self.putting5to30Label, self.putting5to30Text)
        self.formLayout.addRow(self.putting30Label, self.putting30Text)

        self.vBox.addWidget(self.addAttributesButton)
        self.vBox.addWidget(self.backButton)
        self.vBox.setAlignment(Qt.AlignCenter)
        self.hBox.addLayout(self.formLayout)
        self.hBox.addLayout(self.vBox)
        self.mainLayout.addLayout(self.hBox)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.hBox.setAlignment(Qt.AlignVCenter)
        self.mainLayout.setAlignment(Qt.AlignHCenter)

        self.show()

    def clickAddAttributesButton(self):
        self.storeGolferAttributes()

    def storeGolferAttributes(self):
        global db_file
        
        conn, cursor = dbConnPlayers()
        
        golfer_attributes = self.getGolferAttributes()     
        print(golfer_attributes)

        createGolferAttributesTable = """    
        CREATE TABLE IF NOT EXISTS GolferAttributes (
            "UserJoin#" INTEGER PRIMARY KEY AUTOINCREMENT,
            ID TEXT,
            TeamID TEXT,
            DriveDistance REAL, 
            DriveAccuracy REAL, 
            "Approach50-100yds" REAL, 
            "Approach100-150yds" REAL, 
            "Approach150-200yds" REAL, 
            "Approach200+yds" REAL,
            ATGFairway REAL,
            ATGRough REAL,
            ATGBunker REAL,
            "Putting2-5ft" REAL,
            "Putting5-30ft" REAL,
            "Putting30+ft" REAL,
            FOREIGN KEY (ID) REFERENCES PlayerBio(ID)
        );
        """
        store_attributes = """
        INSERT OR IGNORE INTO GolferAttributes (ID, TeamID, DriveDistance, DriveAccuracy, 
        "Approach50-100yds", "Approach100-150yds", "Approach150-200yds", "Approach200+yds", 
        ATGFairway, ATGRough, ATGBunker, "Putting2-5ft", "Putting5-30ft", "Putting30+ft")
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        try:
            cursor.execute(createGolferAttributesTable)
            print('GolferAttributes table checked/created')

        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            
        for golfer in golfer_attributes:
            try:
                cursor.execute(store_attributes, (
                    golfer['ID'],
                    golfer['TeamID'],
                    golfer['DriveDistance'],
                    golfer['DriveAccuracy'],
                    golfer['Approach50-100yds'],
                    golfer['Approach100-150yds'],
                    golfer['Approach150-200yds'],
                    golfer['Approach200+yds'],
                    golfer['ATGFairway'],
                    golfer['ATGRough'],
                    golfer['ATGBunker'],
                    golfer['Putting2-5ft'],
                    golfer['Putting5-30ft'],
                    golfer['Putting30+ft']
                ))
                print(f"Golfer {golfer['ID']} added successfully")
            except sqlite3.Error as e:
                print(f"Error adding player: {golfer['ID']}, Error: {e}")
        conn.commit()
        conn.close()

    def getGolferAttributes(self):
        golfer_attributes = []
                
        randTeam = str(random.choice(["Thunder Raptors", "Solar Titans", "Galactic Guardians", "Mystic Warriors", "Velocity Vanguards"]))

        rTeam = randTeam
        id = self.golferIDText.text()
        dd = self.driveDistanceText.text()
        da = self.driveAccuracyText.text()
        a50to = self.approach50to100Text.text()
        a100to = self.approach100to150Text.text()
        a150to = self.approach150to200Text.text()
        a200 = self.approach200Text.text()
        atgf = self.atgFairwayText.text()
        atgr = self.atgRoughText.text()
        atgb = self.atgBunkerText.text()
        p2to = self.putting2to5Text.text()
        p5to = self.putting5to30Text.text()
        p30 = self.putting30Text.text()

        golfer_attributes.append({
            'ID': id,
            'TeamID': rTeam,
            'DriveDistance': dd, 
            'DriveAccuracy': da, 
            'Approach50-100yds': a50to, 
            'Approach100-150yds': a100to, 
            'Approach150-200yds': a150to, 
            'Approach200+yds': a200,
            'ATGFairway': atgf,
            'ATGRough': atgr,
            'ATGBunker': atgb,
            'Putting2-5ft': p2to,
            'Putting5-30ft': p5to,
            'Putting30+ft': p30})

        return golfer_attributes
    
    def clickBackButton(self):
        self.close()

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push image to back
        self.bgImageLabel.lower()

        # Pull widget to front
        self.mainWidget.raise_()

        super().resizeEvent(event)

class DifficultyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.scratchButton = QPushButton("Scratch Golfer")
        self.bogeyButton = QPushButton("Bogey Golfer")
        self.backButton = QPushButton("Back")
        self.buttonGroup = QButtonGroup()
        self.buttonLayout = QVBoxLayout()
        self.bogeyGraphLayout = QHBoxLayout()
        self.scrachcGraphLayout = QHBoxLayout()
        self.mainLayout = QVBoxLayout()
        self.mainWidget = QWidget()

        # Background image
        self.bgImageLabel = QLabel(self)
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bg_image = loadBGImage()
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.initUI()

    def initUI(self):
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Course Difficulty Menu')       
        
        self.bogeyButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bogeyButton.setMinimumSize(100, 50)
        self.bogeyButton.setMaximumSize(200, 75)
        self.bogeyButton.setStyleSheet("font-size: 12px; font-family: Arial;")
        self.bogeyButton.clicked.connect(self.bogeyButtonClicked)
        
        self.scratchButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scratchButton.setMinimumSize(100, 50)
        self.scratchButton.setMaximumSize(200, 75)
        self.scratchButton.setStyleSheet("font-size: 12px; font-family: Arial;")
        self.scratchButton.clicked.connect(self.scratchButtonClicked)
        
        self.backButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.backButton.setMinimumSize(75, 25)
        self.backButton.setMaximumSize(200, 33)
        self.backButton.setStyleSheet("font-size: 12px; font-family: Arial;")
        self.backButton.clicked.connect(self.clickBackButton)

        self.buttonLayout.addWidget(self.bogeyButton)
        self.buttonLayout.addWidget(self.scratchButton)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonGroup.addButton(self.bogeyButton)
        self.buttonGroup.addButton(self.scratchButton)
        self.buttonLayout.setAlignment(Qt.AlignCenter)

        self.mainLayout.addLayout(self.buttonLayout)
        self.mainLayout.addLayout(self.bogeyGraphLayout)

        self.mainWidget.setLayout(self.mainLayout)
        self.mainWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.mainWidget)

        self.centralWidget().updateGeometry()
        self.centralWidget().adjustSize()

        self.show()

    def bogeyButtonClicked(self):
        self.bogeyGraphWindow = BogeyGraphWindow()

    def scratchButtonClicked(self):
        self.scratchGraphWindow = ScratchGraphWindow()

    def clickBackButton(self):
        self.close()

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()

        # Bring main layout to front
        self.mainWidget.raise_()

        super().resizeEvent(event)

# Not being used anywhere
# class CoursesTableModel(QAbstractTableModel):
#     def __init__(self, data):
#         super(CoursesTableModel, self).__init__()
#         self._data = data
#         self.headers = ["CourseName", "Type", "Yardage", "Slope", "Rating"]

#     def data(self, index, role):
#         if role == Qt.DisplayRole:
#             return self._data[index.row()][index.column()]
        
#     def rowCount(self, index):
#         return len(self._data)
    
#     def columnCount(self, index):
#         return len(self._data[0]) if self._data else 0
    
#     def headerData(self, section, orientation, role):
#         if role == Qt.DisplayRole:
#             if orientation == Qt.Horizontal:
#                 return self.headers[section]
#             if orientation == Qt.Vertical:
#                 return section + 1

class GolferDataWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.bgImageLabel = QLabel(self)
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bg_image = loadBGImage()
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.addBioButton = QPushButton("Add Golfer Biography")
        self.bioButton = QPushButton("View Golfer Biography Database")
        self.addAttributesButton = QPushButton("Add Golfer Attributes")
        self.attributesButton = QPushButton("View Golfer Attributes Database")
        self.backButton = QPushButton("Back")
        self.buttonStack = QButtonGroup()
        self.buttonVbox = QVBoxLayout()
        self.mainWidget = QWidget()

        self.addBioButton.clicked.connect(self.clickAddBioButton)
        self.bioButton.clicked.connect(self.clickBioDBButton)
        self.addAttributesButton.clicked.connect(self.clickAddAttributesButton)
        self.attributesButton.clicked.connect(self.clickAttributesDBButton)
        self.backButton.clicked.connect(self.clickBackButton)

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Golfer Data Menu') 

        for button in [self.addBioButton, self.bioButton, self.addAttributesButton, self.attributesButton]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumSize(200, 33)
            button.setMaximumSize(300, 50)
            button.setStyleSheet("font-size: 12px; font-family: Arial;")

        self.backButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.backButton.setMinimumSize(200, 25)
        self.backButton.setMaximumSize(300, 25)
        self.backButton.setStyleSheet("font-size: 12px; font-family: Arial;")


        self.buttonStack.addButton(self.bioButton)
        self.buttonStack.addButton(self.attributesButton)

        self.buttonVbox.addWidget(self.addBioButton)
        self.buttonVbox.addWidget(self.bioButton)
        self.buttonVbox.addWidget(self.addAttributesButton)
        self.buttonVbox.addWidget(self.attributesButton)
        self.buttonVbox.addWidget(self.backButton)
        self.buttonVbox.setAlignment(Qt.AlignHCenter)
        self.mainWidget.setLayout(self.buttonVbox)
        self.setCentralWidget(self.mainWidget)

        self.show()

    def clickAddBioButton(self):
        self.addBio = AddGolferBioWindow()
        self.addBio.show()

    def clickBioDBButton(self):
        self.bioDB = ViewGolferBioWindow()
        self.bioDB.show()

    def clickAddAttributesButton(self):
        self.attributesWindow = AddGolferAttributesWindow()
        self.attributesWindow.show()

    def clickAttributesDBButton(self):
        self.attributesDB = ViewGolferAttributesWindow()
        self.attributesDB.show()

    def clickBackButton(self):
        self.close()

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()

        # Bring main layout to front
        

        super().resizeEvent(event)

class ViewGolferBioWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.bgImageLabel = QLabel(self)
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bg_image = loadBGImage()
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.tableVbox = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.bioWidget = QWidget(self)

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 650, 400)
        self.setWindowTitle('Golfer Biography Database') 

        self.bioWidget.setLayout(self.tableVbox)
        self.setCentralWidget(self.bioWidget)
        
        self.tableVbox.setAlignment(Qt.AlignHCenter)
        self.tableVbox.addWidget(self.tableWidget)

        data = self.showGolferBio()
        if data == None:
            print("Failed to retreive data.")
        else:
            return data

    def showGolferBio(self):
        try:
        
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "GolfCourses.db")

            print("Connecting to db...")
            time.sleep(0.5)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                print("Connected...")
                time.sleep(0.25)
                
                print("Performing Query...")
                time.sleep(0.25)

                show_golfers = """
                SELECT * FROM PlayerBio;
                """

                cursor.execute(show_golfers)
                data = cursor.fetchall()

                print("Query executed successfully...")
                time.sleep(0.25)

                if not data:
                    print("No data found in PlayerBio table.")
                    return

                headers = ["ID", "Name", "Nation", "Height", "Weight", "Hand"]
                
                self.tableWidget.setColumnCount(len(headers))
                self.tableWidget.setHorizontalHeaderLabels(headers)
                self.tableWidget.setRowCount(len(data))

                for rowIndex, rowData in enumerate(data):
                    for columnIndex, columnData in enumerate(rowData):
                        self.tableWidget.setItem(rowIndex, columnIndex, QTableWidgetItem(str(columnData)))

                print("Table widget popoulated with data...")
                time.sleep(0.5)                
                print("Cursor closed...")
                time.sleep(0.25)
                print("Connection closed...")
                return data
                
        except sqlite3.Error as e:
            print(f"An error occured: {e}")
            return None

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.tableWidget.setGeometry(100, 100, 400, 100)

        # Push image to back
        self.bgImageLabel.lower()

        # Pull table forward
        self.tableWidget.raise_()

        super().resizeEvent(event)

class ViewGolferAttributesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.bgImageLabel = QLabel(self)
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bg_image = loadBGImage()
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.tableVbox = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.attributesWidget = QWidget(self)

        self.initUI()
    
    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(150, 300, 1600, 400)
        self.setWindowTitle('Golfer Attributes Database') 
       
        self.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableVbox.setAlignment(Qt.AlignHCenter)
        self.tableVbox.addWidget(self.tableWidget)
        self.attributesWidget.setLayout(self.tableVbox)
        self.setCentralWidget(self.attributesWidget)

        data = self.showGolferAttributes()
        if data == None:
            print("Failed to retreive data.")
        else:
            return data

    def showGolferAttributes(self):
        try:
        
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "GolfCourses.db")

            print("Connecting to db...")
            time.sleep(0.5)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                print("Connected...")
                time.sleep(0.25)
                
                print("Performing Query...")
                time.sleep(0.25)

                show_attributes = """
                SELECT ID, TeamID, DriveDistance, DriveAccuracy, "Approach50-100yds", "Approach100-150yds", 
                "Approach150-200yds", "Approach200+yds", ATGFairway, ATGRough, ATGBunker, "Putting2-5ft", 
                "Putting5-30ft", "Putting30+ft" FROM GolferAttributes;
                """

                cursor.execute(show_attributes)
                data = cursor.fetchall()

                print("Query executed successfully...")
                time.sleep(0.25)

                if not data:
                    print("No data found in GolferAttributes table.")
                    return

                headers = ["ID", "TeamID", "DriveDistance", "DriveAccuracy", "Approach50-100yds", "Approach100-150yds", 
                "Approach150-200yds", "Approach200+yds", "ATGFairway", "ATGRough", "ATGBunker", "Putting2-5ft", 
                "Putting5-30ft", "Putting30+ft"]

                self.tableWidget.setColumnCount(len(headers))
                self.tableWidget.setHorizontalHeaderLabels(headers)
                self.tableWidget.setRowCount(len(data))

                for rowIndex, rowData in enumerate(data):
                    for columnIndex, columnData in enumerate(rowData):
                        self.tableWidget.setItem(rowIndex, columnIndex, QTableWidgetItem(str(columnData)))

                print("Table widget popoulated with data...")
                time.sleep(0.5)                
                print("Cursor closed...")
                time.sleep(0.25)
                print("Connection closed...")
                return data
                
        except sqlite3.Error as e:
            print(f"An error occured: {e}")
            return None

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.tableWidget.setGeometry(100, 100, 400, 100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # Push image to back
        self.bgImageLabel.lower()

        # Pull table forward
        self.tableWidget.raise_()

        super().resizeEvent(event)

class BogeyGraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.bgImageLabel = QLabel(self)
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bg_image = loadBGImage()
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.webView = QWebEngineView()
        self.widget = QWidget()
        self.hBox = QHBoxLayout()
        self.qVbox = QVBoxLayout()

        self.initUI()

    def initUI(self):
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(50, 50, 1400, 1000)
        self.setWindowTitle('Bogey Golfer Difficulty Graph')
        
        self.hBox.addWidget(self.webView)   
        self.widget.setLayout(self.hBox)
        self.setCentralWidget(self.widget)

        self.plotlyGraphBogey()

        self.show()

    def plotlyGraphBogey(self):
        fig = grabDifficultyBogey()

        if fig is not None:
            fig_html = fig.to_html(include_plotlyjs='cdn')
            print(fig_html)
            self.webView.setHtml(fig_html)
        else:
            print("Failed to generate the Bogey graph.")

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()

        # Bring main layout to front
        

        super().resizeEvent(event)

class ScratchGraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.bgImageLabel = QLabel(self)
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bg_image = loadBGImage()
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.webView = QWebEngineView()
        self.widget = QWidget()
        self.hBox = QHBoxLayout()
        self.qVbox = QVBoxLayout()

        self.initUI()

    def initUI(self):
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(50, 50, 1400, 1000)
        self.setWindowTitle('Scratch Golfer Difficulty Graph')
        
        self.hBox.addWidget(self.webView)   
        self.widget.setLayout(self.hBox)
        self.setCentralWidget(self.widget)

        self.plotlyGraphScratch()

        self.show()

    def plotlyGraphScratch(self):
        fig = grabDifficultyScratch()

        if fig is not None:
            fig_html = fig.to_html(include_plotlyjs='cdn')
            print(fig_html)
            self.webView.setHtml(fig_html)
        else:
            print("Failed to generate the Scratch graph.")

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()

        # Bring main layout to front
        

        super().resizeEvent(event)

def loadBGImage():
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "golfappbg.png")

    try:
        bg_image = QPixmap(image_path)
        if bg_image.isNull():
            raise FileNotFoundError(f"Background image could not be loaded: {image_path}")
        else:
            pass
    except Exception as e:
        print(f"Error loading background image: {e}")
    
    return bg_image


def loadConfig(config_path='GolfDataAnalysis\config.json'):

    # load env. variables
    load_dotenv()

    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # override env. variables, if available
    config['db_path'] = os.getenv('DB_PATH', config['db_path'])
    config['export_path'] = os.getenv('EXPORT_PATH', config['export_path'])
    config['default_fn'] = os.getenv('DEFAULT_FN', config['default_fn'])

    return config

def dbConnCourses(db_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, db_file)
    
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_path)

    if not db.open():   
        print("cannot open database")
        return None, None

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    return conn, cursor

def dbConnPlayers():
    global db_file
    print(f"db_file: {db_file}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"script_dir: {script_dir}")

    db_path = os.path.join(script_dir, db_file)
    print(f"db_path: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Error connecting to databse: {e}")
        return None, None

def checkTable(db_path):
    db, conn, cursor = dbConnCourses(db_path)

    if not conn:
        print("Cannot connect to database.")
        return db, conn, cursor
        
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in database: {tables}")

    cursor.close()
    conn.close()
    db.close()

def checkEntry(courseDictList, db_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, db_file)
    
    conn, cursor = dbConnCourses(db_path)

    check_entry = """
    SELECT CourseName FROM Courses
    WHERE CourseName = ? AND Type = ? AND Yardage = ? AND Slope = ? AND Rating = ?;
    """
    
    for course in courseDictList: 
        try:
            cursor.execute(check_entry, (
                course['Course'],
                course['Type'],
                course['Yardage'],
                course['Slope'],
                course['Rating']
                ))
            existing_course = cursor.fetchone()
            if existing_course:
                print(f"{course['Course']} already exists in the database.")
            else:
                pass
        except sqlite3.Error as e:
            print(f"Error adding courses: {course['Course']}, Error: {e}")
        return existing_course
    conn.close()
    
def grabDifficultyScratch():
    try:
    
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "GolfCourses.db")
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            grab_values = """
            SELECT CourseName, Type, Yardage, Slope, Rating
            FROM Courses;
            """
            cursor.execute(grab_values)
            rows = cursor.fetchall()

            # Calculation
            results = []
            for row in rows:
                course, cType, yardage, slope, rating = row
                difficulty = ((((rating))/80)**4) if rating != 0 else 0
                results.append((*row, difficulty))
            
            # Sorts results
            sorted_results = sorted(results, key=lambda x: x[5], reverse=True)

            # This prints my sorted table
            headers = ["CourseName", "Type", "Yardage", "Slope", "Rating", "Difficulty"]
            time.sleep(0.5)
            print(tabulate(sorted_results, headers=headers, tablefmt="grid"))

            # This creates dataframe for bar graph visual
            df = pd.DataFrame(sorted_results, columns=["CourseName", "Type", "Yardage", "Slope", "Rating", "Difficulty"])
            barG = px.bar(df, 
                          x="CourseName", 
                          y="Difficulty", 
                          color="CourseName", 
                          title="Course Difficulty Comparison", 
                          text="Yardage", 
                          template="plotly_dark",
                          hover_data={"Type": True})
            barG.update_layout(yaxis=dict(range=[0, 1]),
                               hoverlabel=dict(font=dict(color='white')))
            barG.update_traces(textposition="inside", 
                               texttemplate='%{text:,} yds', 
                               textfont=dict(size=12, color='white', family='Arial'))

            return barG
    except sqlite3.Error as e:
        print(f"An error occured: {e}")  
        return None

def grabDifficultyBogey():
    try:
    
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "GolfCourses.db")
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            grab_values = """
            SELECT CourseName, Type, Yardage, Slope, Rating
            FROM Courses;
            """
            cursor.execute(grab_values)
            rows = cursor.fetchall()

            # Calculation
            results = []
            for row in rows:
                course, cType, yardage, slope, rating = row
                difficulty = ((((slope))/155)**2) if slope != 0 else 0
                results.append((*row, difficulty))
            
            # Sorts results
            sorted_results = sorted(results, key=lambda x: x[5], reverse=True)

            # This prints my sorted table
            headers = ["CourseName", "Type", "Yardage", "Slope", "Rating", "Difficulty"]
            time.sleep(0.5)
            print(tabulate(sorted_results, headers=headers, tablefmt="grid"))

            # This creates dataframe for bar graph visual
            df = pd.DataFrame(sorted_results, columns=["CourseName", "Type", "Yardage", "Slope", "Rating", "Difficulty"])
            barG = px.bar(df, 
                          x="CourseName", 
                          y="Difficulty", 
                          color="CourseName", 
                          title="Course Difficulty Comparison", 
                          text="Yardage", 
                          template="plotly_dark",
                          hover_data={"Type": True})
            barG.update_layout(yaxis=dict(range=[0, 1]),
                               hoverlabel=dict(font=dict(color='white')))
            barG.update_traces(textposition="inside", 
                               texttemplate='%{text:,} yds', 
                               textfont=dict(size=12, color='white', family='Arial'))

            return barG
    except sqlite3.Error as e:
        print(f"An error occured: {e}")  
        return None

def sanitized_fn(filename):
    import re
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    sanitized = sanitized.strip()
    return sanitized

def readCoursesDatabase():
    # Load .env file
    load_dotenv()
    
    # export path using .env file, to send export to downloads if user chooses to export)
    export_path = os.path.expandvars(os.getenv('EXPORT_PATH', os.path.join(os.getenv('USERPROFILE'), 'Downloads')))
    
    x = int(input("Would you like to export this data to a .JSON file? \n\nPress 1 for YES \nPress 2 for NO \n\n"))
    if x == 1:
        path_input = input("Please insert a name for the file: ")
        sanitized_path = sanitized_fn(path_input)
        path = os.path.join(export_path, f"{sanitized_path}.json")

        conn, cursor = dbConnCourses()

        read_courses = """
        SELECT * FROM Courses
        """

        cursor.execute(read_courses)
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        data = [dict(zip(column_names, row)) for row in rows]

        with open(path, 'w') as f:
            json.dump(data, f, indent = 2)
        conn.close()
        print(f"{path} has been created. ")
    else:
        pass

def menu():
    app = QApplication(sys.argv)
    menuWin = MenuWindow()
    menuWin.show()

    sys.exit(app.exec_())

# if needed to reset id in sqlite tables, doesn't contain autoincrement right now
# def reset_autoincrement():
#     conn = sqlite3.connect("GolfCourses.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT MAX(course_id) FROM Courses;") 
#     max_id = cursor.fetchone()[0]

#     cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'Courses';", (max_id,)) 
#     conn.commit() 
#     conn.close()

def main():
    config =loadConfig()
    print(config)

    menu()

if __name__ == "__main__":
    main()