from datetime import datetime

from event import Event
from google_calendar import GoogleCalendar
from attendee import Attendee

class CalendarApi:

    def __init__(self,
                email='tminhquang00@gmail.com', 
                credentials_path='./credentials/credentials.json'):
        self.email = email
        self.credential_path = credentials_path
        self.calendar = GoogleCalendar(self.email, self.credential_path)

    def create_attendee(self, guestEmail):
        attendee = Attendee(guestEmail)
        return attendee

    def create_event(self, event_title, start, description, attendees):
        event = Event(event_title, start, description, attendees)
        return event

    def send_invitation(self, event):
        self.calendar.add_event(event)
