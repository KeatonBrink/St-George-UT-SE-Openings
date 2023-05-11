import os
import sqlite3
from datetime import date

def loadData():
    pass

def storeData(websiteData):
    conn = sqlite3.connect(createDB())
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE companies (
            name TEXT PRIMARY KEY,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    cursor.execute('''
        CREATE TABLE postings (
            id INTEGER PRIMARY KEY,
            company TEXT NOT NULL REFERENCES companies(name),
            job TEXT NOT NULL,
            place TEXT NOT NULL
        )
        ''')
    for key, values in websiteData.items():
        print(key)
        print(values)
        cursor.execute('''
            INSERT INTO companies (name) VALUES (?)
            ''', (key,))
        for value in values:
            cursor.execute('''
            INSERT INTO postings (company, job, place) VALUES (?, ?, ?)
            ''', (key, value[0], value[1]))
    conn.commit()
    conn.close()

def createDB():
    today = str(date.today())
    dbFile = today + ".db"
    dbPath = os.path.join("Data", dbFile)
    if os.path.exists(dbPath):
        os.remove(dbPath)
    return dbPath
    

def filterData():
    pass