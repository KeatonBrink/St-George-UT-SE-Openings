import requests
import mailgundata
from datetime import date

def send_email_notification(formattedUpdateData):
    return requests.post(
        f"https://api.mailgun.net/v3/{mailgundata.API_DOMAIN_NAME}/messages",
        auth=("api", mailgundata.API_KEY),
        data={"from": f"St. George Job Bot <mailgun@{mailgundata.API_DOMAIN_NAME}>",
              "to": [mailgundata.RECIEVER_EMAIL],
              "subject": f"New Local SE Job Update {date.today()}",
              "text": formattedUpdateData})