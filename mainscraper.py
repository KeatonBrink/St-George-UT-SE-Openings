import websites
import datastorage

def main():
   webData = websites.scrape()
   datastorage.storeData(webData)

if __name__ == "__main__":
   main()
