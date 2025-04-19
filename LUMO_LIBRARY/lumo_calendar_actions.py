from typing import (Any,
                    Optional)

from googleapiclient.errors import HttpError

import LUMO_LIBRARY.lumo_calendar_utils as l_cal_utils


def get_google_event_by_id(service: Any,
                           var_id: str) -> Any:
    try:
        event_result = (service.events().get(
            calendarId="primary"
            , eventId=var_id)
                        .execute())

        return event_result

    except HttpError as error:
        print("An error has occurred ", error)

def update_event(var_id: str) -> Optional[str]:
    try:
        service = l_cal_utils.get_google_service()
        event = service.events().get(calendarId="primary",
                                     eventId=var_id).execute()

        print("FROM UPDATER FUNCTION")
        print(f"ID {var_id} makes ->", event.get("summary"))

        # updated_event = service.events().update(calendarId="primary", eventId=event["id"], body=event).execute()
        #
        # google_id = event["id"]
        # return google_id  
        return var_id


    except HttpError as error:
        print("An error happened: ", error)

def delete_event(var_id: str) -> None:
    try:
        service = l_cal_utils.get_google_service()
        service.events().delete(calendarId="primary", eventId=var_id).execute()
        print("see if event was deleted")

    except HttpError as error:
        print("This event was (likely) already deleted.")
        print(error)

def confirm_event_deleted(var_id: str) -> None:
    pass

if __name__ == '__main__':
    service = l_cal_utils.get_google_service()
    a = update_event("11")
    print(a)

