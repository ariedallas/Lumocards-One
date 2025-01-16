import os
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import lumo_filehandler as l_files
import lumo_formatters as l_formatter
import lumo_animationlibrary as animators

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_creds():
	creds = None

	if os.path.exists("Z_CREDENTIALS/token.json"):
		creds = Credentials.from_authorized_user_file("Z_CREDENTIALS/token.json")

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())

		else:
			flow = InstalledAppFlow.from_client_secrets_file("Z_CREDENTIALS/credentials.json", SCOPES)
			creds = flow.run_local_server(port=0)

		with open("Z_CREDENTIALS/token.json", "w") as token:
			token.write(creds.to_json())

	return creds


def list_events(no_to_list, credentials):
	try:
		print()
		animators.animate_text("LIST EVENTS FUNCTION:")
		service = build("calendar", "v3", credentials=credentials)

		now = datetime.datetime.now().isoformat() + "Z"
		past = datetime.datetime(2024, 10, 27, 14, 0, 0).isoformat() + "Z"

		event_result = service.events().list(
			calendarId="primary",
			timeMin=past,
			maxResults=no_to_list,
			singleEvents=True,
			orderBy="startTime"
		).execute()

		events = event_result.get("items", [])

		if not events:
			print("No upcoming events found.")
			return

		for event in events:
			start = event["start"]
			print(event["summary"], start.get("dateTime"))

		print()


	except HttpError as error:
		print("An error has occurred ", error)


def create_gcal_event(credentials, formatted_card_title, card_steps):

	try:
		service_2 = build("calendar", "v3", credentials=credentials)

		now = datetime.datetime.now().isoformat() + "Z"
		card_steps_as_str = "\n".join(card_steps[:3])

		my_event = {
			'summary': formatted_card_title
			, 'location': '...'
			, 'description': card_steps_as_str
			, 'start': {
				'dateTime': f'{now}'
				, 'timeZone': 'America/Los_Angeles'
			}
			, 'end': {
				'dateTime': f'{now}'
				, 'timeZone': 'America/Los_Angeles'
			}
			, 'colorId': 7
		}

		run_event = service_2.events().insert(calendarId='primary', body=my_event).execute()

		generated_id = run_event.get('id')
		# animators.animate_text(f"Created Google Calendar Event with ID: {generated_id}")
		return generated_id


	except HttpError as error:
		print("Here's the error that has occurred: ", error)
		return None

def update_event(credentials):
	pass
	# try:
	#
	# 	service = build("calendar", "v3", credentials=credentials)
	#
	# 	retrieved_id_from_txt = '4v39giucjk61s9q23koofhfekd'
	#
	# 	event = service.events().get(calendarId='primary',
	# 								 eventId=retrieved_id_from_txt).execute()
	# 	print()
	# 	print("FROM UPDATER FUNCTION")
	# 	print(f"ID {retrieved_id_from_txt} makes ->", event.get("summary"))
	#
	# 	event['colorId'] = 1
	# 	# event['summary'] = 'Desiree + Arie Continue to Collab on Little Ditty'
	#
	# 	updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
	#
	# 	google_id = event['id']
	# 	return google_id
	#
	#
	# except HttpError as error:
	# 	print("An error happened: ", error)


def get_lines(card_abspath):

	with open(card_abspath, "r") as fin:
		lines = fin.readlines()
		filtered_out_calendarId = filter_for_Id(lines)

	return filtered_out_calendarId


def filter_for_Id(var_lines):
	id_line = None
	filtered_lines = []

	for line in var_lines:
		if '[GOOGLE API EVENT ID]' in line:
			id_line = line
		else:
			filtered_lines.append(line)

	if id_line:

		google_event_id = id_line.split(",")[1]
		return filtered_lines, google_event_id

	else:
		return var_lines, None


def append_id(id_to_txt, card_abspath):
	prefix_and_id = f"\n\n[GOOGLE API EVENT ID],{id_to_txt}"

	with open(card_abspath, "a") as fin:
		fin.writelines(prefix_and_id)


def delete_event_from_GCal(credentials, some_id):
	some_id = str(some_id)

	try:
		service = build("calendar", "v3", credentials=credentials)
		service.events().delete(calendarId='primary', eventId=some_id).execute()

	except HttpError as error:
		print("This event was already deleted.")
		print(error)


def unschedule_and_remove_localCardId(credentials, card_abspath):
	card_tuple = get_lines(card_abspath)
	cards_steps_isolated = card_tuple[0]
	card_event_id = card_tuple[1]

	delete_event_from_GCal(credentials, card_event_id)
	animators.animate_text("The card was deleted from the external (Google) calendar.")

	with open(card_abspath, "w") as fin:
		for line in cards_steps_isolated:
			print(line.strip())
			fin.writelines(line)

	animators.animate_text("The card is now unscheduled.")

def new_event_and_sync(credentials, card_file, card_abspath):

	card_tuple = l_formatter.path_to_card(card_file)
	card_title = card_tuple[0]
	card_title_formatted = l_formatter.format_card_title(card_title)
	card_steps = card_tuple[1]

	steps, possible_google_id = get_lines(card_abspath)

	if possible_google_id: # AND MAKE SURE TO ACTUALLY ACCESS THE CARD TO TEST IT EXISTS IN BOTH PLACES
		animators.animate_text(f"This card is already scheduled, with the ID: {possible_google_id}")

		return possible_google_id

	elif not possible_google_id:
		animators.animate_text("This card is not currently scheduled. Creating Google Calendar Event.")
		generated_id = create_gcal_event(credentials, card_title_formatted, card_steps)

		if generated_id:
			append_id(generated_id, card_abspath)

			return generated_id




if __name__ == "__main__":
	test_card = "L_LumogardenTestCalendarNoId.txt"
	test_card_abspath = os.path.join(l_files.cards_near_folder, test_card)

	print()


	returned_creds = get_creds()


	animators.animate_text("LIST ONE")
	list_events(credentials=returned_creds, no_to_list=3)


	# generated_id = new_event_and_sync(returned_creds, test_card, test_card_abspath)

	unschedule_and_remove_localCardId(credentials=returned_creds, card_abspath=test_card_abspath)

	animators.animate_text("LIST TWO")
	list_events(credentials=returned_creds, no_to_list=3)
	#
	# with open(test_card_abspath, "r") as fin:
	# 	animators.standard_interval_printer(fin.readlines())


