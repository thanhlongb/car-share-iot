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
    """ This class create the google calenar api for adding event to the calendar
    """

    def __init__(self):
        """ Constructor for the class

        :param str title: title of the event
        :param str description: description of the event
        :param str attendee: email of the user
        :param datetime start: time start event
        :param int duration: duration of car booked 

        """
        self.service = self.authorization()
        # end = start + timedelta(hours=duration)
        # self.event_states = self.add_event(title, description, attendee, 
        #                                     start.isoformat(), end.isoformat(), service)

    def authorization(self):
        """
        Authorize the token and create a Google Calendar service

        :return: calendar service
        """

        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds  = None
        
        token_file = Path("app/calendar_api/credentials/token.pickle")
        # print(token_file)
        if token_file.exists():
            with open(token_file, "rb") as token:
                creds = load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('app/calendar_api/credentials/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file, "wb") as token:
                dump(creds, token)

        calendar_service = build("calendar", "v3", credentials =creds )

        return calendar_service

    def add_event(self, title, description, attendee, start, duration):
        """
        Add event to the calendar

        :param str title: title of the event
        :param str description: description of the event
        :param str attendee: email of the user
        :param datetime start: time start event
        :param int duration: duration of car booked 
        :param service: the calendar service

        :return: an event object
        :rtype: Event


        """
        end = start + timedelta(hours=duration)
        event = {"summary": title,
                 "start": {"dateTime": start.isoformat(), "timeZone": str(get_localzone())},
                 "end": {"dateTime": end.isoformat(), "timeZone":str(get_localzone())},
                 "description": description,
                 "attendees": [{"email": attendee}],
                 "reminders": {"useDefault": True}
                }
        event = self.service.events().insert(calendarId="primary", sendNotifications=True, body=event).execute()

        return event

    
    def delete_event(self, event_id):
        '''
        This function delete calendar event

        :param str event_id: id of deleted event
        '''
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()
