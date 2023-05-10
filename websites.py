import urllib

def scrape():
    websiteData = {}
    websiteData["tcn"] = tcnscrape()

def tcnscrape():
    url = "https://tcn.applytojob.com/"
    response = urllib.request.urlopen(url)
    webContent = response.read().decode('UTF-8')
    print(webContent)
    return webContent
