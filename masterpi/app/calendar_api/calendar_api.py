from pathlib import Path
from pickle import load
from pickle import dump

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from uuid import uuid4
from typing import Dict, List
from oauth2client import file, client, tools
from tzlocal import get_localzone
from datetime import datetime, date, timedelta


class CalendarApi:

    def __init__(self, title, description, attendee, start, duration):
        service = self.authorization()
        end = start + timedelta(hours=duration)
        self.event_states = self.add_event(title, description, attendee, 
                                            start.isoformat(), end.isoformat(), service)

    def authorization(self):
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds  = None
        token_file = Path("./credentials/token.pickle")

        if token_file.exists():
            with open(token_file, "rb") as token:
                creds = load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('./credentials/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file, "wb") as token:
                dump(creds, token)

        calendar_service = build("calendar", "v3", credentials =creds )

        return calendar_service

    def add_event(self, title, description, attendee, start, end, service: build):
        event = {"summary": title,
                 "start": {"dateTime": start, "timeZone": str(get_localzone())},
                 "end": {"dateTime": end, "timeZone": str(get_localzone())},
                 "description": description,
                 "attendees": [{"email": attendee}],
                 "reminders": {"useDefault": True}
                }
        event = service.events().insert(calendarId="primary", sendNotifications=True, body=event).execute()

        return event


# if __name__ == "__main__":
#     plan = CalendarApi("test", 
#                         "ádasdasdasdas",
#                         "tmq2706@gmail.com", 
#                         datetime.now(), 2)
#     print(plan.event_states)
