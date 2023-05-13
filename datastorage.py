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
                created_at DATE NOT NULL DEFAULT CURRENT_DATE
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
    newData = {}
    for curKey, curValues in webData.items():
        if curKey in prevData:
            curSValues = sorted(curValues, key = lambda x: (x[0], x[1]))
            prevSValues = sorted(prevData[curKey], key = lambda x: (x[0], x[1]))
            cSVIndex = 0
            pSVIndex = 0
            newData[curKey] = []
            while cSVIndex < len(curSValues) and pSVIndex < len(prevSValues):
                if curSValues[cSVIndex][0] != prevSValues[pSVIndex][0]:
                    if cSVIndex < len(curSValues) - 1 and curSValues[cSVIndex+1][0] == prevSValues[pSVIndex][0]:
                        newData[curKey].append(curSValues[cSVIndex])
                        cSVIndex += 2
                        pSVIndex += 1
                    elif pSVIndex < len(prevSValues) - 1 and prevSValues[pSVIndex+1][0] == curSValues[cSVIndex][0]:
                        pSVIndex += 2
                        cSVIndex += 1
                        # Basically the default case where more than one thing different sequentially.
                        # This could be updated to be more concise, but it is more or less fine.
                    else: 
                        newData[curKey] = curSValues[cSVIndex:]
                        cSVIndex = len(curSValues)
                        pSVIndex = len(prevSValues)
                else:
                    pSVIndex += 1
                    cSVIndex += 1
            while cSVIndex < len(curSValues):
                newData[curKey].append(curSValues[cSVIndex])
            if len(newData[curKey]) == 0:
                newData.pop(curKey)
        elif len(curValues) > 0:
            newData[curKey] = curValues
    if len(newData) == 0:
        return ""
    return emailFormattedData(webData)


def emailFormattedData(webData):
    formattedString = "Here are your job updates:\n"
    for key, values in webData.items():
        formattedString += "\n" + key + "-\n"
        for value in values:
            formattedString += "\t" + value[0] + ", " + value[1] + "\n"
    return formattedString