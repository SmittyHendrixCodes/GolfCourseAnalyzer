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
import PyQt5
import plotly.express as px
import plotly.graph_objects as go
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QWidget, QStackedWidget, QPushButton, QLabel, QLineEdit, QComboBox, QFormLayout, QHBoxLayout, QVBoxLayout, QSizePolicy, QTableView, QTableWidget, QTableWidgetItem, QButtonGroup, QHeaderView, QSpacerItem
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

        self.nameLabel = QLabel("Name:")
        self.nameText = QLineEdit()
        self.ageLabel = QLabel("Age:")
        self.ageText = QLineEdit()
        self.nationLabel = QLabel("Nationality:")
        self.nationText = QLineEdit()
        self.heightLabel = QLabel("Height (cm):")
        self.heightText = QLineEdit()
        self.weightLabel = QLabel("Weight (kg):")
        self.weightText = QLineEdit()
        self.handLabel = QLabel("Handedness:")
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

        for lineEdit in [self.nameText, self.ageText, self.nationText, self.heightText, self.weightText, self.handText]:
            palette = lineEdit.palette()
            palette.setColor(QPalette.PlaceholderText, QColor("black"))
            lineEdit.setPalette(palette)

        self.nameLabel.setStyleSheet("font-size: 17px; color: black; font-family: Arial;")
        self.ageLabel.setStyleSheet("font-size: 17px; color: black; font-family: Arial;")
        self.nationLabel.setStyleSheet("font-size: 17px; color: black; font-family: Arial;")
        self.heightLabel.setStyleSheet("font-size: 17px; color: black; font-family: Arial;")
        self.weightLabel.setStyleSheet("font-size: 17px; color: black; font-family: Arial;")
        self.handLabel.setStyleSheet("font-size: 17px; color: black; font-family: Arial;")

        self.addPlayerButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addPlayerButton.setMaximumSize(200, 50)
        self.addPlayerButton.setMinimumSize(100, 33)
        self.addPlayerButton.clicked.connect(self.clickAddGolfer)
        self.addPlayerButton.setStyleSheet("background-color: white; color: black; padding: 5px; border: 1px solid black; font-size: 12px; font-family: Arial;")

        self.backButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.backButton.setMinimumSize(100, 25)
        self.backButton.setMaximumSize(200, 25)
        self.backButton.clicked.connect(self.clickBackButton)
        self.backButton.setStyleSheet("background-color: white; color: black; padding: 5px; border: 1px solid black; font-size: 12px; font-family: Arial;")

        for lineEdit in [self.nameText, self.ageText, self.nationText, self.heightText, self.weightText, self.handText]:
            lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            lineEdit.setMinimumSize(200, 25)
            lineEdit.setMaximumSize(250, 33)
            lineEdit.setStyleSheet("font-size: 12px; font-family: Arial; color: black; background-color: white")

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

class CourseCompareWindow(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()

        self.bg_image = loadBGImage()
        self.bgImageLabel = QLabel(self)

        self.widget = QWidget()
        self.compareButton = QPushButton("Compare")
        self.backButton = QPushButton("Back")
        self.comboBox1 = QComboBox()
        self.comboBox2 = QComboBox()
        self.webView = QWebEngineView()
        self.vBox = QVBoxLayout()
        self.hBox = QHBoxLayout()
        self.vBox1 = QVBoxLayout()
        self.mainLayout = QVBoxLayout()

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(200, 200, 600, 400)
        self.setWindowTitle('Golf Course Difficulty Comparison')

        self.webView.setFixedSize(800, 600)

        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        for button in [self.backButton, self.compareButton]:
            button.setStyleSheet("border: 1px solid black; font-size: 15px; background-color: white; color: black; font-family: Arial;")
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumSize(150, 25)
            button.setMaximumSize(200, 33)

        for combo in [self.comboBox1, self.comboBox2]:
            combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            combo.setMinimumSize(150, 25)
            combo.setMaximumSize(200, 33)
            combo.setStyleSheet("border: 2px solid black; font-size: 15px; color: black; font-family: Arial; background-color: white;")

        data = self.comboBoxPop()
        self.comboBox1.addItems(data)
        self.comboBox1.currentIndexChanged.connect(self.on_change)
        self.comboBox2.addItems(data)

        self.compareButton.clicked.connect(self.clickCompareButton)
        self.backButton.clicked.connect(self.clickBackButton)

        self.vBox.addWidget(self.webView)
        self.hBox.addStretch(1)
        self.hBox.addWidget(self.comboBox1)
        self.hBox.addWidget(self.comboBox2)
        self.hBox.addStretch(1)
        self.vBox1.addWidget(self.compareButton, alignment=Qt.AlignCenter)
        self.vBox1.addWidget(self.backButton, alignment=Qt.AlignCenter)
        self.mainLayout.addLayout(self.vBox)
        self.mainLayout.addLayout(self.hBox)
        self.mainLayout.addLayout(self.vBox1)

        self.widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.widget)

        self.showRadar(self.comboBox1.currentText())

    def comboBoxPop(self):
        conn, cursor = dbConnCourses()

        get_courses = """
        SELECT CourseName FROM Courses;
        """
        cursor.execute(get_courses)
        data = cursor.fetchall()
        conn.close()
        return [item[0] for item in data]

    def getCourses(self, course_id):
        conn, cursor = dbConnCourses()

        get_courses = """
        SELECT Yardage, Slope, Rating FROM Courses WHERE CourseName = ?;
        """
        cursor.execute(get_courses, (course_id,))
        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]
        data = pd.DataFrame(rows, columns=columns)

        normalized_values = []
        max_values = [10000] + [200] + [100]

        for idx, column in enumerate(columns):
            max_val = max_values[idx]
            normalized_values.append(data[column] / max_val)

        normalized_data = pd.concat(normalized_values, axis=1)  

        colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A5', '#A533FF', '#33FFA5', '#FF5733', '#33FF57', '#3357FF', '#FF33A5', '#A533FF', '#33FFA5']

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=normalized_data.iloc[0],
            theta=columns,
            fill='toself',
            fillcolor='lightcoral',
            marker=dict(color=colors),
            line=dict(color='crimson', width=2),
            name=f"{self.comboBox1.currentText()}" + " Statistics"
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    tickvals=[0, .2, .4, .6, .8, 1.0],
                    ticktext=[],
                    range=[0, 1]
                )
            ),
            showlegend=True
        )

        conn.close()
        return normalized_data, columns, fig

    def clickCompareButton(self):
        combo1 = self.comboBox1.currentText()
        combo2 = self.comboBox2.currentText()

        if combo1 != combo2:
            data1, columns, _ = self.getCourses(combo1)
            data2, _, _ = self.getCourses(combo2)

            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=data1.iloc[0], 
                theta=columns, 
                fill='toself',
                name=f'Golfer {combo1}',
                marker=dict(color='darkgreen'),
                line=dict(color='green', width=2)
            ))

            fig.add_trace(go.Scatterpolar(
                r=data2.iloc[0], 
                theta=columns, 
                fill='toself',
                name=f'Golfer {combo2}',
                marker=dict(color='red'),
                line=dict(color='crimson', width=2)
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        tickvals=[.20, .40, .60, .80, 1.0],
                        ticktext=['20%', '40%', '60%', '80%', '100%'],
                        range=[0,1]
                    )
                ),
                showlegend=True
            )
            
            fig_html = fig.to_html(include_plotlyjs='cdn')
            self.webView.setHtml(fig_html)
        else:
            self.showRadar(combo1)

    def showRadar(self, course_id):
        _, _, fig = self.getCourses(course_id)

        if fig is not None:
            fig_html = fig.to_html(include_plotlyjs='cdn')
            print(fig_html)
            self.webView.setHtml(fig_html)
        else:
            print("Failed to generate the Golfer's Attributes graph.")

    def on_change(self):
        course_id = self.comboBox1.currentText()
        self.showRadar(course_id)

    def clickBackButton(self):
        self.close()

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()

        # Pull buttons forward
        self.compareButton.raise_()
        self.comboBox1.raise_()
        self.comboBox2.raise_()

        super().resizeEvent(event)

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

        self.buttonStack = QVBoxLayout() 
        self.menuWindow = QWidget()

        self.initUI()

    # Don't look at this bullhonky
    # class ParabolaWidget(QWidget):
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
            button.setStyleSheet("font-size: 12px; font-family: Arial; background-color: white; color: black; border: 1px solid black; padding: 5px;")
            button.setFlat(False)
        self.exitButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.exitButton.setMinimumSize(133, 25)
        self.exitButton.setMaximumSize(150, 33)
        self.exitButton.setFlat(False)
        self.exitButton.setStyleSheet("font-size: 12px; font-family: Arial; background-color: white; color: black; border: 1px solid black; padding: 5px;")

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
        self.courseDBMenu = CourseDatabaseMenu()
        self.courseDBMenu.show()

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
        self.resultsLabel = QLabel("STATUS:")
        self.resultsLabelImage = QLabel("")
        
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

        self.addCourseButton.setStyleSheet("font-size: 15px; color: black; background-color: white")
        self.addCourseButton.setFixedSize(100, 33)
        self.addCourseButton.clicked.connect(self.clickAddCourse)

        self.backButton.setStyleSheet("font-size: 15px; color: black; background-color: white;")
        self.backButton.setFixedSize(75, 25)
        self.backButton.clicked.connect(self.clickBackButton)
        
        self.courseNameLabel.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")                                            
        self.courseNameText.setStyleSheet("font-size: 15px; color: black; font-family: Arial; background-color: white;")
        self.courseNameText.setPlaceholderText("Name of Course")
        self.courseTypeLabel.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.courseTypeText.setStyleSheet("font-size: 15px; color: black; font-family: Arial; background-color: white;")
        self.courseTypeText.setPlaceholderText("Type of Grass")
        self.courseYardageLabel.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.courseYardageText.setStyleSheet("font-size: 15px; color: black; font-family: Arial; background-color: white;")
        self.courseYardageText.setPlaceholderText("Course Length")
        self.courseSlopeLabel.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")
        self.courseSlopeText.setStyleSheet("font-size: 15px; color: black; font-family: Arial; background-color: white;")
        self.courseSlopeText.setPlaceholderText("Course Slope")
        self.courseRatingLabel.setStyleSheet("font-size: 15px; color: black; font-family: Arial;")     
        self.courseRatingText.setStyleSheet("font-size: 15px; color: black; font-family: Arial; background-color: white;")
        self.courseRatingText.setPlaceholderText("Course Rating")
        self.resultsLabel.setStyleSheet("border: 1px solid black; padding: 5px; font-size: 15px; color: black; font-family: Arial;")

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
        self.mainLayout.addWidget(self.resultsLabel, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.resultsLabelImage, alignment=Qt.AlignCenter)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.addCourseLayout)
        self.mainLayout.addLayout(addCourseButtonLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.setAlignment(Qt.AlignHCenter)

        self.addCourseWindow.setLayout(self.mainLayout)
        self.setCentralWidget(self.addCourseWindow)

        self.show()

    def clickAddCourse(self, db_path):
        self.addCourses(db_path)
        
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
        
        courseDictList = self.storeCourseDictList()
        add_courses = """
        INSERT OR IGNORE INTO Courses (CourseName, Type, Yardage, Slope, Rating)
        VALUES (?, ?, ?, ?, ?);
        """

        for course in courseDictList:
            if self.checkEntry(db_path) is not None:
                self.resultsLabelImage.setStyleSheet("border: 5px solid red; padding: 1px; font-size: 15px; background-color: red; font-family: Arial;")
                self.resultsLabel.setText(f"{course['Course']} already exists in the database.")
            else:
                try:
                    conn, cursor = dbConnCourses(db_path)
                    cursor.execute(add_courses, (
                        course['Course'],
                        course['Type'],
                        course['Yardage'],
                        course['Slope'],
                        course['Rating'],
                    ))
                    conn.commit()
                    conn.close()
                    self.resultsLabelImage.setStyleSheet("border: 5px solid green; padding: 1px; font-size: 15px; background-color: green; font-family: Arial;")
                    self.resultsLabel.setText(f"{course['Course']} added successfully.")
                except sqlite3.Error as e:
                    print(f"Error adding courses: {course['Course']}, Error: {e}")

    def checkEntry(self, db_path):
        conn, cursor = dbConnCourses(db_path)

        courseDictList = self.storeCourseDictList()
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
                return existing_course
            except sqlite3.Error as e:
                print(f"Error adding courses: {course['Course']}, Error: {e}")
                return None
        conn.close()

    def clickBackButton(self):
        self.close()

class CourseDatabaseMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bgImageLabel = QLabel(self)
        self.bg_image = loadBGImage()
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.courseDBWindow = QWidget()
        self.menuLayout = QVBoxLayout()
        self.vBox = QVBoxLayout()
        self.databaseButton = QPushButton("Course Database")
        self.courseStatsButton = QPushButton("Course Stats")
        self.backButton = QPushButton("Back")
        self.buttonStack = QButtonGroup()

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Course Database Menu')

        self.buttonStack.addButton(self.databaseButton)
        self.buttonStack.addButton(self.courseStatsButton)
        self.buttonStack.addButton(self.backButton)

        for button in [self.databaseButton, self.courseStatsButton, self.backButton]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumSize(150, 25)
            button.setMaximumSize(200, 33)
            button.setStyleSheet("font-size: 12px; font-family: Arial; background-color: white; color: black; border: 1px solid black; padding: 5px;")
            button.setFlat(False)

        self.vBox.addWidget(self.databaseButton)
        self.vBox.addWidget(self.courseStatsButton)
        self.vBox.addWidget(self.backButton)
        self.menuLayout.addLayout(self.vBox)
        self.menuLayout.setAlignment(Qt.AlignHCenter)
        self.courseDBWindow.setLayout(self.menuLayout)
        self.setCentralWidget(self.courseDBWindow)

        self.databaseButton.clicked.connect(self.databaseButtonClicked)
        self.courseStatsButton.clicked.connect(self.courseStatsButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

        self.show()

    def courseStatsButtonClicked(self):
        self.courseStatsWindow = CourseCompareWindow()
        self.courseStatsWindow.show()

    def databaseButtonClicked(self):
        self.courseDBWindow = CourseDatabaseWindow()
        self.courseDBWindow.show()

    def backButtonClicked(self):
        self.close()

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()

        # Pull buttons forward
        self.databaseButton.raise_()
        self.courseStatsButton.raise_()
        self.backButton.raise_()

        super().resizeEvent(event)

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

        self.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableWidget.setMinimumSize(400, 400)
        self.tableWidget.setMaximumSize(800, 600)

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

        # Push image to back
        self.bgImageLabel.lower()

        # Pull table forward
        self.tableWidget.raise_()

        super().resizeEvent(event)

    def showCourses(self):
        try:
        
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "GolfCourses.db")

            time.sleep(0.5)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()

                show_courses = """
                SELECT * FROM Courses;
                """

                cursor.execute(show_courses)
                data = cursor.fetchall()

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

        for label in [self.golferIDLabel,
                        self.driveDistanceLabel,
                        self.driveAccuracyLabel,
                        self.approach50to100Label,
                        self.approach100to150Label,
                        self.approach150to200Label,
                        self.approach200Label,
                        self.atgFairwayLabel,
                        self.atgRoughLabel,
                        self.atgBunkerLabel,
                        self.putting2to5Label,
                        self.putting5to30Label,
                        self.putting30Label]:
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            label.setStyleSheet("color: black; font-size: 14px; font-family: Arial;")

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
            lineEdit.setStyleSheet("font-size: 14px; background-color: white; color: black; font-family: Arial;")

        self.addAttributesButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addAttributesButton.setMaximumSize(200, 75)
        self.addAttributesButton.setMinimumSize(150, 50)
        self.addAttributesButton.clicked.connect(self.clickAddAttributesButton)
        self.addAttributesButton.setStyleSheet("font-size: 12px; border: 1px solid black; color: black; background-color: white; font-family: Arial;")

        self.backButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.backButton.setMinimumSize(150, 25)
        self.backButton.setMaximumSize(200, 33)
        self.backButton.clicked.connect(self.clickBackButton)
        self.backButton.setStyleSheet("font-size: 12px; border: 1px solid black; background-color: white; color: black; font-family: Arial;")

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
        self.bogeyButton.setStyleSheet("font-size: 12px; color: black; background-color: white; border: 1px solid black; font-family: Arial;")
        self.bogeyButton.clicked.connect(self.bogeyButtonClicked)
        
        self.scratchButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scratchButton.setMinimumSize(100, 50)
        self.scratchButton.setMaximumSize(200, 75)
        self.scratchButton.setStyleSheet("font-size: 12px; color: black; background-color: white; border: 1px solid black; font-family: Arial;")
        self.scratchButton.clicked.connect(self.scratchButtonClicked)
        
        self.backButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.backButton.setMinimumSize(75, 25)
        self.backButton.setMaximumSize(200, 33)
        self.backButton.setStyleSheet("font-size: 12px; color: black; background-color: white; border: 1px solid black; font-family: Arial;")
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
        self.attributesButton.clicked.connect(self.clickAttributesMenuButton)
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
            button.setStyleSheet("font-size: 12px; color: black; background-color: white; border: 1px solid black; font-family: Arial;")

        self.backButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.backButton.setMinimumSize(200, 25)
        self.backButton.setMaximumSize(300, 25)
        self.backButton.setStyleSheet("font-size: 12px; color: black; background-color: white; border: 1px solid black; font-family: Arial;")


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

    def clickAttributesMenuButton(self):
        self.attributesMenu = GolferAttributesMenu()
        self.attributesMenu.show()

    def clickBackButton(self):
        self.close()

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()

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

        self.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableWidget.setFixedSize(700, 300)

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

            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                time.sleep(0.25)

                show_golfers = """
                SELECT * FROM PlayerBio;
                """

                cursor.execute(show_golfers)
                data = cursor.fetchall()

                if not data:
                    print("No data found in PlayerBio table.")
                    return

                headers = ["ID", "Name", "Age", "Nation", "Height", "Weight", "Hand"]
                
                self.tableWidget.setColumnCount(len(headers))
                self.tableWidget.setHorizontalHeaderLabels(headers)
                self.tableWidget.setRowCount(len(data))

                for rowIndex, rowData in enumerate(data):
                    for columnIndex, columnData in enumerate(rowData):
                        self.tableWidget.setItem(rowIndex, columnIndex, QTableWidgetItem(str(columnData)))

                return data
                
        except sqlite3.Error as e:
            print(f"An error occured: {e}")
            return None

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push image to back
        self.bgImageLabel.lower()

        # Pull table forward
        self.tableWidget.raise_()

        super().resizeEvent(event)

class GolferAttributesMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.bgImageLabel = QLabel(self)
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bg_image = loadBGImage()
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.widget = QWidget()
        self.vBox = QVBoxLayout()

        self.radarGraphButton = QPushButton('Golfer Stats')
        self.tableButton =QPushButton('Golfer Database')
        self.backButton = QPushButton('Back')
        
        self.radarGraphButton.clicked.connect(self.radarButtonClicked)
        self.tableButton.clicked.connect(self.tableButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)

        self.initUI()

    def initUI(self):
    
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Player Attributes Menu')

        for button in [self.radarGraphButton, self.tableButton]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setStyleSheet("padding: 5px; font-size: 12px; color: black; background-color: white; border: 1px solid black; font-family: Arial;")
            button.setMinimumSize(200, 33)
            button.setMaximumSize(250, 50)

        self.backButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.backButton.setStyleSheet("padding: 5px; font-size: 12px; color: black; background-color: white; border: 1px solid black; font-family: Arial;")
        self.backButton.setMinimumSize(200, 25)
        self.backButton.setMaximumSize(250, 33)

        self.vBox.addWidget(self.radarGraphButton)
        self.vBox.addWidget(self.tableButton)
        self.vBox.addWidget(self.backButton)

        self.vBox.setSpacing(10)
        self.vBox.setContentsMargins(0, 0, 0, 0)
        self.vBox.setAlignment(Qt.AlignHCenter)

        self.widget.setLayout(self.vBox)
        self.setCentralWidget(self.widget)

    def radarButtonClicked(self):
        self.radar = GolferAttributesRadar()
        self.radar.show()

    def tableButtonClicked(self):
        self.table = ViewGolferAttributesWindow()
        self.table.show()

    def backButtonClicked(self):
        self.close()

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()      

        super().resizeEvent(event)

class GolferAttributesRadar(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.bgImageLabel = QLabel(self)
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bg_image = loadBGImage()
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        self.webView = QWebEngineView()
        self.comboBox = QComboBox()
        self.comboBox2 = QComboBox()
        self.widget = QWidget()
        self.hBox = QHBoxLayout()
        self.vBox = QVBoxLayout()
        self.compareButton = QPushButton("Compare")
        self.backButton = QPushButton('Back')

        self.compareButton.clicked.connect(self.clickCompareButton)
        self.backButton.clicked.connect(self.clickBackButton)

        self.initUI()

    def initUI(self):
    
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.setGeometry(100, 100, 1000, 1000)
        self.setWindowTitle('Player Attributes Graph')

        self.webView.setFixedSize(800, 600)

        for button in [self.compareButton, self.backButton]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMaximumSize(200, 33)
            button.setMinimumSize(250, 25)
            button.setStyleSheet("font-size: 12px; color: black; background-color: white; border: 1px solid black; font-family: Arial;")
    
        for combo in [self.comboBox, self.comboBox2]:
            combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            combo.setMaximumSize(200, 33)
            combo.setMinimumSize(250, 25)
            combo.setStyleSheet("font-size: 12px; color: black; background-color: white; border: 1px solid black; font-family: Arial;")

        # Combo Box Populate
        data = self.comboBoxPop()
        self.comboBox.addItems(data)
        self.comboBox.currentIndexChanged.connect(self.on_change)
        self.comboBox2.addItems(data)

        self.vBox.addStretch(1)
        self.vBox.addWidget(self.webView)
        self.vBox.addStretch(1)
        self.vBox.addWidget(self.comboBox)
        self.vBox.addWidget(self.comboBox2)
        self.vBox.addWidget(self.compareButton)
        self.vBox.addWidget(self.backButton)
        self.vBox.addStretch(1)

        self.hBox.addLayout(self.vBox)
        self.hBox.setAlignment(Qt.AlignHCenter)

        self.widget.setLayout(self.hBox)
        self.setCentralWidget(self.widget)

        self.showRadar(self.comboBox.currentText())

    def grabAttributes(self, golfer_id):
        conn, cursor = dbConnPlayers()
 
        select_attributes = """
        SELECT DriveDistance, DriveAccuracy, 
        "Approach50-100yds", "Approach100-150yds", "Approach150-200yds", "Approach200+yds", 
        ATGFairway, ATGRough, ATGBunker, "Putting2-5ft", "Putting5-30ft", "Putting30+ft" 
        FROM GolferAttributes WHERE ID = ?
        """

        cursor.execute(select_attributes, (golfer_id,))
        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]
        data = pd.DataFrame(rows, columns=columns)

        max_values = [350] + [1.5] * 11
        normalized_values = []
            
        for idx, column in enumerate(columns):
            max_val = max_values[idx]
            normalized_values.append(data[column] / max_val)

        normalized_data = pd.concat(normalized_values, axis=1)       

        fig = go.Figure()

        # fig.add_trace(go.Scatterpolar(
        #         r=normalized_data.iloc[0],
        #         theta=columns[2:],
        #         fill='toself',
        #         name='Golfer Statistics'
        # ))

        # fig.update_traces(
        #     selector=dict(theta=column),
        #     marker=dict(size=12),
        #     line=dict(width=2)
        # )

        colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A5', '#A533FF', '#33FFA5', '#FF5733', '#33FF57', '#3357FF', '#FF33A5', '#A533FF', '#33FFA5']

        fig.add_trace(go.Scatterpolar(
            r=normalized_data.iloc[0],  # Plotting the first row
            theta=columns,  # Using the attribute columns
            fill='toself',
            fillcolor='lightcoral',
            name='Golfer Statistics',
            marker=dict(color=colors),  # Default color marker
            line=dict(color='crimson', width=2)  # Default color line
        ))

        # Update the trace colors
        for i, (category, colors) in enumerate(zip(columns, colors)):
            fig.add_trace(go.Scatterpolar(
                r=[normalized_data.iloc[0]],
                theta=[category],
                fill='toself',
                name=category,
                marker=dict(color=colors),
                line=dict(color=colors, width=2)
            ))
            
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    tickvals=[.20, .40, .60, .80, 1.0],
                    ticktext=['20%', '40%', '60%', '80%', '100%'],
                    range=[0,1]
                )
            )
        )
        conn.close()
        return normalized_data, columns, fig
    
    def grabComboAttributes(self, item):
        conn, cursor = dbConnPlayers()
 
        player_attributes = """
        SELECT * FROM GolferAttributes WHERE ID = ?
        """

        cursor.execute(player_attributes, (item,))
        rows = cursor.fetchall()
        conn.close()
        print(rows)
        return rows
    
    def on_change(self):
        golfer_id = self.comboBox.currentText()
        self.showRadar(golfer_id)

    def showRadar(self, golfer_id):
        _, _, fig = self.grabAttributes(golfer_id)

        if fig is not None:
            fig_html = fig.to_html(include_plotlyjs='cdn')
            print(fig_html)
            self.webView.setHtml(fig_html)
        else:
            print("Failed to generate the Golfer's Attributes graph.")

    def comboBoxPop(self):
        conn, cursor = dbConnPlayers()
        grab_golfers = "SELECT ID FROM GolferAttributes"
        cursor.execute(grab_golfers)
        data = cursor.fetchall()

        conn.close()

        return [item[0] for item in data]
    
    def clickCompareButton(self):
        combo1 = self.comboBox.currentText()
        combo2 = self.comboBox2.currentText()

        if combo1 != combo2:
            data1, columns, _ = self.grabAttributes(combo1)
            data2, _, _ = self.grabAttributes(combo2)

            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=data1.iloc[0], 
                theta=columns, 
                fill='toself',
                name=f'Golfer {combo1}',
                marker=dict(color='darkgreen'),  # Default color marker
                line=dict(color='green', width=2)  # Default color line
            ))

            fig.add_trace(go.Scatterpolar(
                r=data2.iloc[0], 
                theta=columns, 
                fill='toself',
                name=f'Golfer {combo2}',
                marker=dict(color='red'),  # Default color marker
                line=dict(color='crimson', width=2)  # Default color line
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        tickvals=[.20, .40, .60, .80, 1.0],
                        ticktext=['20%', '40%', '60%', '80%', '100%'],
                        range=[0,1]
                    )
                ),
                showlegend=True
            )
            
            fig_html = fig.to_html(include_plotlyjs='cdn')
            self.webView.setHtml(fig_html)
        else:
            self.showRadar(combo1)

    def clickBackButton(self):
        self.close()

    def resizeEvent(self, event):
        self.bgImageLabel.setGeometry(0, 0, self.width(), self.height())
        self.bgImageLabel.setPixmap(self.bg_image.scaled(self.bgImageLabel.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        # Push bg image to back
        self.bgImageLabel.lower()      

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
       
        self.tableWidget.setFixedSize(1200, 300)
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

            time.sleep(0.5)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                time.sleep(0.25)

                show_attributes = """
                SELECT ID, TeamID, DriveDistance, DriveAccuracy, "Approach50-100yds", "Approach100-150yds", 
                "Approach150-200yds", "Approach200+yds", ATGFairway, ATGRough, ATGBunker, "Putting2-5ft", 
                "Putting5-30ft", "Putting30+ft" FROM GolferAttributes;
                """

                cursor.execute(show_attributes)
                data = cursor.fetchall()


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

                time.sleep(0.5)                
                time.sleep(0.25)
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


def loadConfig():
    # Load environment variables
    load_dotenv()

    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the potential config paths
    config_paths = [
        os.path.join(current_dir, 'config.json'),
        os.path.join(current_dir, 'GolfDataAnalysis', 'config.json')
    ]

    # Find the first existing config file
    config_path = None
    for path in config_paths:
        if os.path.exists(path):
            config_path = path
            break

    if config_path is None:
        raise FileNotFoundError("config.json file not found in the expected directories.")

    # Load the configuration file
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Override environment variables, if available
    config['db_path'] = os.getenv('DB_PATH', config['db_path'])
    config['export_path'] = os.getenv('EXPORT_PATH', config['export_path'])
    config['default_fn'] = os.getenv('DEFAULT_FN', config['default_fn'])

    return config

def dbConnCourses():
    global db_file
    print(f"db_file: {db_file}")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"script_dir: {script_dir}")
    db_path = os.path.join(script_dir, db_file)
    print(f"db_path: {db_path}")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None, None

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
    conn, cursor = dbConnCourses(db_path)

    if not conn:
        print("Cannot connect to database.")
        return conn, cursor
        
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in database: {tables}")

    cursor.close()
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

# This class creates random golfers and attributes bio and stats to their profiles
class RandomPlayers():

    pass

def menu():
    app = QApplication(sys.argv)
    menuWin = MenuWindow()
    menuWin.show()

    sys.exit(app.exec_())

def main():
    config =loadConfig()
    print(config)

    menu()

if __name__ == "__main__":
    main()