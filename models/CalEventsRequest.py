from models import Event
import datetime
import os.path
import os
from dotenv import load_dotenv

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

load_dotenv()
SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH")

class CalEventsRequest():
    def __init__(self) -> None:
        events: list[Event] = self._get_upcoming_API()
        self._events_dict: list[dict[str, str]] = [event.to_dict() for event in events]

    @property
    def events(self) -> dict[Event]:
        return self._events_dict

    def _format_date(self, start, end):
        start_date_obj = datetime.datetime.fromisoformat(start)
        end_date_obj = datetime.datetime.fromisoformat(end)

        # IF SAME-DAY EVENT
        if start_date_obj.date() == end_date_obj.date():
            # IF EVENT IS TODAY
            if start_date_obj.date() == datetime.datetime.today().date():
                return f"{start_date_obj.time().strftime("%I:%M %p")} - {end_date_obj.time().strftime("%I:%M %p")}"
            
            # IF EVENT IS SAME-DAY BUT IN FUTURE
            else:
                return f"{start_date_obj.date().strftime("%a, %b %d")} | {start_date_obj.time().strftime("%I:%M %p")} - {end_date_obj.time().strftime("%I:%M %p")}"


        # IF EVENT IS MULTI-DAY or ALL-DAY
        else:
            difference = start_date_obj - end_date_obj
            is_all_day = difference == datetime.timedelta(days=-1)
            if is_all_day:
                return f"{start_date_obj.date().strftime("%a, %b %d")}"
            
            return f"{start_date_obj.date().strftime("%a, %b %d")} - {end_date_obj.date().strftime("%a, %b %d")}"

    def _get_upcoming_API(self) -> list[Event]:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # token_path = os.path.join(script_dir, "token.json")
        # creds_path = os.path.join(script_dir, "credentials.json")
        # SERVICE_ACCOUNT_PATH = os.path.join(script_dir, "service.json")

        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=SCOPES)

        # FOR USER CREDENTIALS INSTEAD OF SERVER

        # if os.path.exists("./token.json"):
        #   creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # # If there are no (valid) credentials available, let the user log in.
        # if not creds or not creds.valid:
        #   if creds and creds.expired and creds.refresh_token:
        #     creds.refresh(Request())
        #   else:
        #     flow = InstalledAppFlow.from_client_secrets_file(
        #         creds_path, SCOPES
        #     )
        #     creds = flow.run_local_server(port=0)
        #   # Save the credentials for the next run
        #   with open(token_path, "w") as token:
        #     token.write(creds.to_json())

        try:
            self._service = build("calendar", "v3", credentials=creds)

            # Call the Calendar API
            self._now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

            tomorrow = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
            self._midnight_tomorrow = tomorrow.replace(hour=23, minute=59, second=59, microsecond=0).isoformat(timespec="seconds")

            print("Getting the upcoming 10 events")

            self._event_objs = []

            calendar_ids = [
                            "imjamesonzeller@gmail.com", 
                            "58da859ee90a0c2d692d6027060e94268b65e3643267614f71b5772b1b2178d1@group.calendar.google.com",
                            "918757d470383d7acb40e0b1cb103a3a12ba5175b048c085ccf91c026cb1a46f@group.calendar.google.com"
                        ]

            for calendar_id in calendar_ids:
                self._request_api(calendar_id)

            self._sort_and_truncate_events()
            return self._remove_tomorrow_events()
        
        except HttpError as error:
            print(f"An error occurred: {error}")

    def _request_api(self, id: str) -> None:
        events_result = (   
            self._service.events()
            .list(
                # calendarId="primary",
                # ^^^ FOR USER CREDS INSTEAD OF SERVER
                calendarId=id,
                timeMin=self._now,
                timeMax=self._midnight_tomorrow,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
    
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            events = []

        for event in events:
            name = event["summary"]

            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            date = self._format_date(start, end)

            event_obj = Event(name, date, start)
            self._event_objs.append(event_obj)

    def _sort_and_truncate_events(self) -> None:
        self._event_objs.sort()
        self._event_objs = self._event_objs[:10]

    def _remove_tomorrow_events(self) -> list[Event]:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        events = []

        for event in self._event_objs:
            events.append(event)
            event_date = datetime.datetime.fromisoformat(event.trueStart).date()

            if event_date == tomorrow:
                break
        
        return events