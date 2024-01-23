# St-George-UT-SE-Openings

A script for scraping SE jobs in St. George, entering them in a sqlite3 db, and emailing openings to a designated email.

# Installation

Requires mailgun api for emails, which is placed in a mailgundata.py file.

    API_KEY
    API_DOMAIN_NAME
    RECIEVER_EMAIL

Note, the reciever is your personal email that will recieve the updates.

Selenium and firefox is required for the scraping.

# Usage

Run with python3:

    python3 mainscraper.py

# To do

[] Finish website scraping
[x] Implment db system
[] Add comparison logic between old and new website scrape data
[x] Integrate emailing capabilities
