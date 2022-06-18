import os
import datetime
import requests
import json
from dotenv import load_dotenv

load_dotenv()
my_bearer = os.getenv("BEARER")

headers = {
    "Authorization": f"Bearer {my_bearer}",
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json"
}

def isAlreadyCheckIn(user):
  url = "https://api.notion.com/v1/databases/" + os.getenv("DATABASE_ID") + "/query"
  getpayload = {
    "filter": {
        "and": [
            {
                "property": "date",
                "date": {
                    "equals" :datetime.datetime.now().strftime('%Y-%m-%d'),
                }
            },
            {
                "property": "Name",
                "title": {
                    "equals" : user
                }
            }
        ]
    }
  }
  response = requests.post(url, json=getpayload, headers=headers)
  rsObj =  json.loads(response.text)

  return len(rsObj["results"]) >= 1


def checkIn(user):
  url = "https://api.notion.com/v1/pages"
  payload = {
    "parent": {
        "database_id": os.getenv("DATABASE_ID")
    },
    "properties": {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": user
                    }
                }
            ]
        },
        "date": {
            "date" : {
                "start": datetime.datetime.now().strftime('%Y-%m-%d'),
                "end": None,
                "time_zone": None
            }
        }
    }
  }
  requests.post(url, json=payload, headers=headers)



