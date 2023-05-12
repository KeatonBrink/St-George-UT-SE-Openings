import os
import sqlite3
from datetime import date

DATABASE_NAME = os.path.join("Data", "database.db")
PREV_DB_NAME_FILE = os.path.join("Data", "previousdate.txt")

def loadData(prevDate):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Questionable use of dates (probably not compatible )
    cursor.execute('''
        SELECT company, job, place FROM postings WHERE created_at = ?
        ''', (prevDate,))
    result = cursor.fetchall()
    retDict = {}
    for item in result:
        retDict[item[0]] = []
    for item in result:
        retDict[item[0]].append([item[1], item[2]])
    # Debugging
    print(retDict)
    return retDict


def storeData(websiteData):
    if not os.path.exists(DATABASE_NAME):
        initializeDB = True
    else:
        initializeDB = False
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    if initializeDB:
        cursor.execute('''
            CREATE TABLE postings (
                id INTEGER PRIMARY KEY,
                company TEXT NOT NULL,
                job TEXT NOT NULL,
                place TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            ''')
    for key, values in websiteData.items():
        for value in values:
            cursor.execute('''
            INSERT INTO postings (company, job, place) VALUES (?, ?, ?)
            ''', (key, value[0], value[1]))
    conn.commit()
    conn.close()
    

def filterData(webData):
    # Load name of last db file
    prevData = ""
    with open(PREV_DB_NAME_FILE, "r", encoding="utf-8") as f:
        prevDate = f.read()
    with open(PREV_DB_NAME_FILE, "w", encoding="utf-8") as f:
        f.write(str(date.today()))
    if prevDate == date.today():
        return ""
    storeData(webData)
    if prevDate == "":
        print("No data, sending all jobs through email")
        return emailFormattedData(webData)
    # Load contents of last data update into correct format
    prevData = loadData(prevDate)
    # Zipper compare contents, generating new job information

def emailFormattedData(webData):
    formattedString = "Here are your job updates:\n"
    for key, values in webData.items():
        formattedString += "\n" + key + "-\n"
        for value in values:
            formattedString += "\t" + value[0] + ", " + value[1] + "\n"
    return formattedString