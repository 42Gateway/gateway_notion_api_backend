import datetime, json, os, requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



my_bearer = os.environ.get("BEARER")
headers = {
    "Authorization": f"Bearer {my_bearer}",
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json"
}

def isAlreadyCheckIn(user):
    url = "https://api.notion.com/v1/databases/" + os.environ.get("DATABASE_ID") + "/query"
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
            "database_id": os.environ.get("DATABASE_ID")
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


class CheckInView(APIView):
    def get(self, request):
        try:
            alreadyCheckIn = isAlreadyCheckIn(request.user)
        except:
            return Response('User Not Found', status=status.HTTP_404_NOT_FOUND)

        if alreadyCheckIn:
            return Response('Already Check In', status=status.HTTP_409_CONFLICT)

        try:
            checkIn(request.user)
        except:
            return Response('Database Not Found', status=status.HTTP_404_NOT_FOUND)

        return Response()