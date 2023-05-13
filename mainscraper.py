#!/usr/bin/env python3

import websites
import datastorage
from updateemail import send_email_notification

def main():
   webData = websites.scrape()
   updates = datastorage.filterData(webData)
   if updates != "":
      send_email_notification(updates)


if __name__ == "__main__":
   main()
