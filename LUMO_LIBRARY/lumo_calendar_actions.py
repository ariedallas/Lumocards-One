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


def create_event(dict_event, dt_parser):
    new_event = {}
    new_event["summary"] = dict_event.get("summary")
    new_event["start"] = dt_parser.start_G_format
    new_event["end"] = dt_parser.end_G_format

    if dict_event["description"] != "none":
        new_event["description"] = dict_event["description"]

    if dict_event["location"] != "none":
        new_event["location"] = dict_event["location"]

    try:
        service = l_cal_utils.get_google_service()
        event = service.events().insert(calendarId="primary",
                                        body=new_event,
                                        ).execute()

        return True

    except:
        return False


def update_event_simple(updated_event: dict, var_id: str, target):
    try:
        service = l_cal_utils.get_google_service()
        event = service.events().get(calendarId="primary",
                                     eventId=var_id).execute()

        event[target] = updated_event[target]

        updated_G_event = service.events().update(calendarId="primary",
                                                eventId=event["id"],
                                                body=event).execute()
        return True, updated_G_event[target]


    except HttpError as error:
        return False, error


def delete_event(var_id: str) -> None:
    try:
        service = l_cal_utils.get_google_service()
        service.events().delete(calendarId="primary", eventId=var_id).execute()

    except HttpError as error:
        print("This event was (likely) already deleted.")
        print(error)


def confirm_event_deleted(var_id: str) -> None:
    pass


if __name__ == '__main__':
    print("Hello from main")
