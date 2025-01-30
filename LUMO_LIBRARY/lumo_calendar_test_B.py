import os
import datetime
import subprocess

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import lumo_filehandler as l_files
import lumo_formatters as l_formatter
import lumo_animationlibrary as animators

SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds_file = os.path.join(l_files.credentials_folder, "credentials.json")
token_file = os.path.join(l_files.credentials_folder, "token.json")

def get_creds():
	creds = None

	if os.path.exists(token_file):
		creds = Credentials.from_authorized_user_file(token_file)

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())

		else:
			flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
			creds = flow.run_local_server(port=0)

		with open(token_file, "w") as token:
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

	card_tuple = l_formatter.filename_to_card(card_file)
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

def percent(percentage, number):

	perc_as_dec = percentage / 100
	return round(number * perc_as_dec)

superlist = ['one', 'two', 'three', 'four']


class CalendarPageDay:
	t_size = os.get_terminal_size()
	width = int(t_size.columns)
	line = ("-" * round((width * .8)))
	content_width = ("-" * round((width * .7)))

	def __init__(self, date, events):
		self.name = "Calendar Page"
		self.date = date
		self.events = events


	def cal_header(self):
		print('{0:^{width}}\n'.format(self.date, width=CalendarPageDay.width))
		print('{0:^{width}}'.format(CalendarPageDay.line, width=CalendarPageDay.width))

	# print('{0:^{width}}'.format(content_width, width=width))

	@staticmethod
	def get_start_and_end(var_event):
		start_time, end_time = var_event['start time'], var_event['end time']
		return start_time, end_time

	@staticmethod
	def row_style_1(var_sel, var_event, var_start_t, var_end_t):
		left = "{:>{width}}".format(" ", width=percent(25, CalendarPageDay.width))
		selector = "{:<{width}}".format(var_sel, width=8)
		event = "• {:<{width}}".format(var_event, width=50)
		time = "{} —— {}".format(var_start_t, var_end_t)

		print(left, selector, event, time)

	@staticmethod
	def row_style_2(var_sel, var_event, var_start_t, var_end_t):
		selector = "{:<{width}}".format(var_sel, width=10)
		event = "• {:<{width}}".format(var_event, width=60)
		time = "{} —— {}".format(var_start_t, var_end_t)

		group = selector + event + time
		print('{0:^{width}}\n'.format(group, width=CalendarPageDay.width))

	def print_sample_page(self):
		start, end = CalendarPageDay.get_start_and_end(self.events[0])
		event_name = self.events[0].get('name')

		subprocess.run(['clear'], shell=True)

		self.cal_header()
		CalendarPageDay.row_style_2("[A]", event_name, start, end)
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[A]", "something I'll do another time", start, end)
		CalendarPageDay.row_style_2("[A]", "something I'll do soon", start, end)



def paginate(calendar):

	idx = 0

	while True:
		user_input = input("  >")

		if user_input == "]":
			idx += 1
			# subprocess.run('clear', shell=True)
			calendar.print_sample_page()
			print(idx)
		elif user_input == "[" and idx > 0:
			idx -= 1
			# subprocess.run('clear', shell=True)
			calendar.print_sample_page()
			print(idx)
		else:
			# subprocess.run('clear', shell=True)
			calendar.print_sample_page()
			print(idx)






if __name__ == "__main__":
	test_card = "TestCalNoId.txt"
	test_card_abspath = os.path.join(l_files.cards_near_folder, test_card)


	sample_page = CalendarPageDay(date="FRIDAY: DECEMBER 14, 2025"
								 ,events=[{'name': 'Places with Cameron and Phil'
									  ,'start time': '14:00'
									  ,'end time': '15:30'}])

	# sample_page.print_sample_page()
	paginate(sample_page)




	# print("{0:{width}}{:<8}{:<}{}".format(
	# 	" "
	# 	,"[A]"
	# 	,"[B]"
	# 	,"[C]"
	# 	, width=30
	# 	, sample_dt_dict['name']
	# ))


	# creds = get_creds()
	# print(creds)
	#
	# list_events(5, creds)
	# animators.animate_text("LIST ONE")
	# list_events(credentials=returned_creds, no_to_list=3)


	# generated_id = new_event_and_sync(returned_creds, test_card, test_card_abspath)

	# unschedule_and_remove_localCardId(credentials=returned_creds, card_abspath=test_card_abspath)
	#
	# animators.animate_text("LIST TWO")
	# list_events(credentials=returned_creds, no_to_list=3)
	#
	# with open(test_card_abspath, "r") as fin:
	# 	animators.standard_interval_printer(fin.readlines())


