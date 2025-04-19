import dateutil.tz
from dateutil.relativedelta import relativedelta

import LUMO_LIBRARY.lumo_calendar_utils as l_cal_utils

from googleapiclient.errors import HttpError

def get_google_event_by_id(service, var_id):
    try:
        event_result = (service.events().get(
            calendarId="primary"
            , eventId=var_id)
                        .execute())

        return event_result

    except HttpError as error:
        print("An error has occurred ", error)

def update_event(var_id):
    try:
        retrieved_id_from_txt = "4v39giucjk61s9q23koofhfekd"

        service = l_cal_utils.get_google_service()
        event = service.events().get(calendarId="primary",
                                     eventId=retrieved_id_from_txt).execute()
        print()
        print("FROM UPDATER FUNCTION")
        print(f"ID {retrieved_id_from_txt} makes ->", event.get("summary"))

        event["colorId"] = 1
        # event["summary"] = "Desiree + Arie Continue to Collab on Little Ditty"

        updated_event = service.events().update(calendarId="primary", eventId=event["id"], body=event).execute()

        google_id = event["id"]
        return google_id


    except HttpError as error:
        print("An error happened: ", error)

def delete_event(var_id):
    try:
        service = l_cal_utils.get_google_service()
        service.events().delete(calendarId="primary", eventId=var_id).execute()
        print("see if event was deleted")

    except HttpError as error:
        print("This event was (likely) already deleted.")
        print(error)

if __name__ == '__main__':
    print("hello")
