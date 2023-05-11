import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Sample websiteData:
# {
    # "tcn": [["SWE", "St George, UT"], ... ],
    # ...
    # "website": [["Job Title", "Location", "Department"]]
# }

timeDelay = .5

def scrape():
    websiteData = {}
    websiteData["tcn"] = tcnscrape()
    websiteData["zonos"] = zonosscrape()
    websiteData["vasion"] = vasionscrape()
    websiteData["wilson"] = wilsonscrape()
    websiteData["busybusy"] = busybusyscrape()
    for key, value in websiteData.items():
        print(key)
        print(value)

def tcnscrape():
    url = "https://tcn.applytojob.com/"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error grabbing tcn webpage")
        return []
    webContent = response.text
    soup = BeautifulSoup(webContent, "html.parser")
    listItems = soup.find_all("li", class_="list-group-item")
    retItems = []
    for item in listItems:
        itemSplit = item.text.split("\n")
        curEntry = []
        for piece in itemSplit:
            if piece != "":
                curEntry.append(piece.strip())
                if len(curEntry) >= 2:
                    break
        retItems.append(curEntry)
    # print(retItems)
    return retItems

def zonosscrape():
    return []

def vasionscrape():
    url = "https://apply.workable.com/vasion/#jobs"
    driver = webdriver.Firefox()
    driver.get(url)
    print(driver.title)
    time.sleep(timeDelay)
    posts = driver.find_elements(By.CLASS_NAME, "styles--1vo9F")
    retItems = []
    for post in posts:
        try:
            curPosition = post.find_element(By.CLASS_NAME, "styles--3TJHk").find_element(By.TAG_NAME, "span").text
            curLocation = post.find_element(By.CLASS_NAME, "styles--1_T3H ").text
            curCombo = [curPosition, curLocation]
            retItems.append(curCombo)
        except:
            print("Error vasion grabbing post")
    # print(retItems)
    driver.close()
    return retItems

def wilsonscrape():
    url = "https://wilsonelectronics.applicantpro.com/jobs/"
    driver = webdriver.Firefox()
    driver.get(url)
    print(driver.title)
    time.sleep(timeDelay)
    posts = driver.find_elements(By.CLASS_NAME, "strip-side-borders")
    retItems = []
    for post in posts:
        try:
            curPosition = post.find_element(By.TAG_NAME, "h4").text
            curLocation = post.find_element(By.TAG_NAME, "li").text
            retItems.append([curPosition, curLocation])
        except:
            print("Error wilson grabbing post")
    driver.close()
    return retItems

def busybusyscrape():
    url = "https://busybusy.com/careers/"
    driver = webdriver.Firefox()
    driver.get(url)
    print(driver.title)
    time.sleep(timeDelay)
    page = driver.find_element(By.TAG_NAME, "body")
    retItems = []
    page = page.text.split("\n")
    for index in range(len(page)):
        if "St. George, UT" in page[index]:
            retItems.append([page[index-1].strip(), page[index].strip()])
    driver.close()
    return retItems