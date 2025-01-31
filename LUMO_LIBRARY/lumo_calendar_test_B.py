import os
import datetime
import subprocess
import calendar
import sys

# from enum import Enum

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


cal = calendar.Calendar()
curr_year, curr_month, curr_day = l_files.today.year, l_files.today.month, l_files.today.day
monthdays = [d for d in cal.itermonthdays(year=curr_year, month=curr_month) if d != 0]
curr_month_max = max(monthdays)

# class Month(Enum):
# 	JAN = 1
# 	FEB = 2
# 	MAR = 3
# 	APR = 4
# 	MAY = 5
# 	JUN = 6
# 	JUL = 7
# 	AUG = 8
# 	SEP = 9
# 	OCT = 10
# 	NOV = 11
# 	DEC = 12


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


def list_events(credentials):
	try:
		print()
		animators.animate_text("LIST EVENTS FUNCTION:")
		service = build("calendar", "v3", credentials=credentials)

		# now = datetime.datetime.now().isoformat() + "Z"
		month_start = datetime.datetime(year=curr_year, month=curr_month, day=1).isoformat() + "Z"
		month_end   = datetime.datetime(year=curr_year, month=curr_month, day=curr_month_max).isoformat() + "Z"


		event_result = service.events().list(
			calendarId="primary",
			timeMin=month_start,
			timeMax=month_end,
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

def percenter(percentage, number):

	perc_as_dec = percentage / 100
	return round(number * perc_as_dec)

superlist = ['one', 'two', 'three', 'four']


class CalendarPageDay:
	t_size = os.get_terminal_size()
	total_width = int(t_size.columns)
	content_width = percenter(70, total_width)
	left_margin = round((total_width - content_width) / 2)

	EVENTS_WIDTH = 86
	events_line = "-" * EVENTS_WIDTH
	l_margin = round((total_width - EVENTS_WIDTH) / 2)
	l_margin_line = "-" * l_margin

	line = ("-" * content_width)

	def __init__(self, date, events):
		self.name = "Calendar Page"
		self.date = date
		self.events = events


	def cal_header(self):
		print('{0:^{width}}\n'.format(self.date, width=CalendarPageDay.total_width))
		print('{0:^{width}}'.format(CalendarPageDay.line, width=CalendarPageDay.total_width))
		print()

	# print('{0:^{width}}'.format(content_width, width=width))

	@staticmethod
	def get_start_and_end(var_event):
		start_time, end_time = var_event['start time'], var_event['end time']
		return start_time, end_time

	@staticmethod
	def row_style_1(var_sel, var_event, var_start_t, var_end_t):
		left = "{:>{width}}".format(" ", width=percenter(25, CalendarPageDay.total_width))
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
		print('{0:^{width}}\n'.format(group, width=CalendarPageDay.total_width))

	def display_day(self):
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
		CalendarPageDay.row_style_2("[A]", event_name, start, end)
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[-]", "--- --- ---", "     ", "     ")
		CalendarPageDay.row_style_2("[A]", "something I'll do another time", start, end)
		CalendarPageDay.row_style_2("[A]", "something I'll do soon", start, end)


def paginate(list_of_days):
	idx = 0
	current_page = list_of_days[idx]


	while True:
		current_page.display_day()
		# print("{:^{width}}".format(CalendarPageDay.events_line, width=CalendarPageDay.total_width))
		print(" " * CalendarPageDay.l_margin, idx)
		print(" " * CalendarPageDay.l_margin, end=' ')
		user_input = input(">  ")

		if user_input == "]" and idx < 2:
			idx += 1
			current_page = list_of_days[idx]

		elif user_input == "[" and idx > 0:
			idx -= 1
			current_page = list_of_days[idx]

		else:
			current_page = list_of_days[idx]


def get_month_events():
	creds = get_creds()

	list_events(creds)

	return []

if __name__ == "__main__":
	test_card = "TestCalNoId.txt"
	test_card_abspath = os.path.join(l_files.cards_near_folder, test_card)

	curr_month_events = get_month_events()



	# sample_page = CalendarPageDay(date="FRIDAY: DECEMBER 14, 2025"
	# 							 ,events=[{'name': 'Places with Cameron and Phil'
	# 								  ,'start time': '14:00'
	# 								  ,'end time': '15:30'}])
	#
	# sample_page_2 = CalendarPageDay(date="FRIDAY: DECEMBER 15, 2025"
	# 							 ,events=[{'name': 'Blah super blah'
	# 								  ,'start time': '14:00'
	# 								  ,'end time': '15:30'}])
	#
	# sample_page_3 = CalendarPageDay(date="FRIDAY: DECEMBER 16, 2025"
	# 							 ,events=[{'name': '... another thing thing'
	# 								  ,'start time': '21:00'
	# 								  ,'end time': '23:00'}])
	#
	# sample_pages = [sample_page, sample_page_2, sample_page_3]

	# paginate(sample_pages)

# ------------------------------------- END / MISC BELOW -------------------------------------- #

# print("{:{fill}<50}".format("hello", fill="*"))
# print("{0:{width}}{:<8}{:<}{}".format(


	# list_events(5, creds)n
	# list_events(credentials=returned_creds, no_to_list=3)

