#!/usr/bin/python3.4
__author__ = 'Mertcan Gokgoz'

import mysql.connector
import sys

try:
    # Database connection string
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@123"
    )
    
    # Prepare cursor object
    cursor = database.cursor()

    # Check if the 'timetable' database already exists
    cursor.execute("SHOW DATABASES LIKE 'timetable'")
    result = cursor.fetchone()

    if result:
        print("Database 'timetable' already exists.")
    else:
        # Create the 'timetable' database
        cursor.execute("CREATE DATABASE timetable")
        print("Database 'timetable' created.")

    # Switch to the 'timetable' database
    cursor.execute("USE timetable")

    # Drop table if it already exists
    cursor.execute("DROP TABLE IF EXISTS TimeTable")

    # SQL command to create table
    sql = """CREATE TABLE TimeTable (
            Batch VARCHAR(45) NOT NULL COMMENT '',
            Monday VARCHAR(45) NOT NULL COMMENT '',
            Tuesday VARCHAR(45) NOT NULL COMMENT '',
            Wednesday VARCHAR(45) NOT NULL COMMENT '',
            Thursday VARCHAR(45) NOT NULL COMMENT '',
            Friday VARCHAR(45) NOT NULL COMMENT '',
            Saturday VARCHAR(45) NOT NULL COMMENT '',
            Sunday VARCHAR(45) NOT NULL COMMENT '')"""

    # Execute the SQL command to create the table
    cursor.execute(sql)

    # Disconnect from the server
    database.close()
    print("Database and Table Created")

except Exception as e:
    print("\n[ Error ]\n\t Error Message:\t", e, "\n")
    sys.exit(1)
