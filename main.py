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
import os
from dotenv import load_dotenv
import plotly.express as px
# from sqlalchemy import create_engine

# Classes
class Golfer:
    #Outer Class
    def __init__(self, name):
        self.data = self.Data()



    ...

    class Data:
        #Inner Class
        def readData(self, data):
            print("All data on THE GOLFERS NAME has been pulled.")
            print(data)

class Course:
    #Inner Class
    def __init__(self, course, cType, yardage, slope, rating):

        self.course = course
        self.cType = cType
        self.yardage = yardage
        self.slope = slope
        self.rating = rating

    def __str__(self):
        return f"Course Name: {self.course}/n cType: {self.cType}/n Yardage: {self.yardage}/n Slope: {self.slope}/n Rating: {self.rating}/n"

    @classmethod
    def getCourse(cls):
        # Collect course data from user input and return as a list of dictionaries.
        courseDictList = []

        p = int(input("How many courses will you enter data for?: "))
        
        # Could add try/except block here for later
        if p == []:
            print("Okay! No courses to enter.")
            return []
        elif p != []:
            for _ in range(0, p):
                course = input("Course name: ")
                cType = input("Type: ")
                # Add failsafe for wrong course type at later date
                yardage = int(input("Yardage: "))
                slope = float(input("Slope: "))
                rating = float(input("Rating: "))

                courseDictList.append({
                'Course': course,
                'Type': cType,
                'Yardage': yardage,
                'Slope': slope,
                'Rating': rating
                })
            # Check for courseDictList data components & structure
            print(f"Collected Course Data: {courseDictList}")
            return courseDictList

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

def dbConnCourses():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "GolfCourses.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    createCoursesTable = """
    CREATE TABLE IF NOT EXISTS Courses(
        CourseName TEXT PRIMARY KEY, 
        Type TEXT, 
        Yardage INTEGER, 
        Slope REAL, 
        Rating REAL,
        UNIQUE(CourseName, Type, Yardage, Slope, Rating)
    );
    """

    cursor.execute(createCoursesTable)
    conn.commit()
    return conn, cursor

def checkTable():
    conn, cursor = dbConnCourses()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in database: {tables}")

    conn.close()

def checkEntry(courseDictList):
    conn, cursor = dbConnCourses()

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
    
def addCourses(courseDictList):
    # Inserts a new course into the Courses table."""
    conn, cursor = dbConnCourses()

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

def grabDifficulty():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "GolfCourses.db")
    
    try:
    
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
                difficulty = ((math.sqrt(slope + rating))/10)-1 if slope and rating != 0 else 0
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

            user_choice = int(input("Would you like to see this in a graph? \nPress 1 to view \nPress 2 to return to the menu \n\nEnter Option: "))
            if user_choice == 1:
                barG.show()
            else:
                pass
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occured: {e}")  

def showCourses():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "GolfCourses.db")
    
    try:
    
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            show_courses = """
            SELECT * FROM Courses;
            """
            # or 'SELECT FROM Courses (CourseName, Type, Yardage, Slope, Rating)'

            cursor.execute(show_courses)
            rows = cursor.fetchall()
            headers = ["Course", "Type", "Yardage", "Slope", "Rating"]

            if rows:
                time.sleep(0.5)
                print(tabulate(rows, headers=headers, tablefmt="grid"))
            else:
                print("No courses found in database.")
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occured: {e}")

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

def returnMenu():
    menu_input = int(input("\nWould you like to return to the menu?: \nPress 1 for YES \nPress 2 for NO\n\n"))
    if menu_input == 1:
        menu()
    elif menu_input == 2:
        print("Thank you, see you next time! \n")
        sys.exit()
    else:
        print("Invalid key, please try again!")
        returnMenu()
    

def menu():
    print(" \n|---MENU---| \n\n 1. Add a Course \n 2. Check Course Database \n 3. Check Course Difficulty \n 4. Exit Program \n")
    menu_input = int(input("Please enter menu option: "))

    if menu_input == 1:
        get_course = Course.getCourse()
        check_entry = checkEntry(get_course)
        try:
            if get_course:
                if check_entry is None:
                    addCourses(get_course)
                else:
                    raise Exception('\nThis course data already exists in the database. You can check the database using menu option "2". ')     
            else:
                print("\nNo courses to add.")
        except Exception as e:
            print(e)
        checkTable()
        returnMenu()   
    elif menu_input == 2:
        showCourses()
        readCoursesDatabase()
        returnMenu()
    elif menu_input == 3:
        grabDifficulty()
        returnMenu()
    elif menu_input == 4:
        print("\nClosing program. See ya next time! \n")
        sys.exit()
    else:
        print("\nInvalid key pressed, please try again... ")
        menu()
        if menu_input not in [1, 2, 3, 4]:
            print("\nClosing program due to too many incorrect keys... Goodbye! \n")
            sys.exit()
        else:
            pass

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
    dbConnCourses()

    menu()

if __name__ == "__main__":
    main()