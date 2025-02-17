import math

from dateutil.relativedelta import relativedelta

from lumo_calendar_utils import (CalendarPageDay, CalendarPageWeek
                                ,get_day_blocks
                                ,get_time_window_2
                                ,parse_brackets
                                ,get_adjacent_month
                                ,today_date
                                ,curr_year
                                ,curr_month)


class CalendarInterface:

    def __init__(self):
        past_month = get_adjacent_month(curr_month, curr_year, "past", 1)
        next_month = get_adjacent_month(curr_month, curr_year, "next", 1)

        self.day_blocks_window = get_day_blocks()
        self.week_blocks_window = self.separate_by_weeks()

    def paginate_days(self):
        idx = self._get_idx_for_today()
        curr_day_block = self.day_blocks_window[idx]

        while True:
            curr_page = CalendarPageDay(curr_day_block)
            curr_page.display_day()

            print(" " * CalendarPageDay.l_margin, idx)
            print(" " * CalendarPageDay.l_margin, end=' ')

            user_input = input(">  ")

            shift, direction = parse_brackets(user_input)
            shift = shift if shift < 25 else 25

            if direction == "PAGE RIGHT":
                look_ahead_idx = idx + shift

                if look_ahead_idx < len(self.day_blocks_window) - 3:
                    idx += shift
                    curr_day_block = self.day_blocks_window[idx]
                else:
                    # Means the idx is nearing the right end of the 'buffered' events_block and needs to be updated
                    # Function grabs a group of 4 isoweeks, 'right'/future, relative to the current month in focus
                    big_shift = self._roll_forward()
                    idx -= big_shift
                    curr_day_block = self.day_blocks_window[idx]

            elif direction == "PAGE LEFT":
                look_ahead_idx = idx - shift

                if look_ahead_idx > 3:
                    idx -= shift
                    curr_day_block = self.day_blocks_window[idx]
                else:
                    # Means the idx is nearing the left end of the 'buffered' events block and needs to be updated
                    # Functions grabs a group of 4 isoweeks, 'left'/past, relative to the current date in focus
                    big_shift = self._roll_backward()
                    idx += big_shift
                    curr_day_block = self.day_blocks_window[idx]
            else:
                curr_day_block = self.day_blocks_window[idx]

    def paginate_weeks(self):
        idx = self._get_idx_for_curr_week()
        curr_week_block = self.week_blocks_window[idx]
        print(curr_week_block[0].events)

        while True:
            curr_page = CalendarPageWeek(curr_week_block)
            curr_page.display_day()

            print(" " * CalendarPageWeek.l_margin, idx)
            print(" " * CalendarPageWeek.l_margin, end=' ')

    def _get_idx_for_today(self):
        total_weeks = len(self.week_blocks_window)
        prior_weeks = round((total_weeks - 1) / 2)
        prior_days = prior_weeks * 7
        idx = prior_days + today_date.weekday()

        return idx

    def _get_idx_for_curr_week(self):
        total_weeks = len(self.week_blocks_window)
        center_idx = math.floor(total_weeks / 2)

        return center_idx

    def _roll_forward(self):
        curr_final_monday = self.week_blocks_window[-1][0]
        target_monday = curr_final_monday.date + relativedelta(weeks=1)

        start, end = get_time_window_2(target_monday, 4)
        future_events = get_day_blocks(time_min=start, time_max=end)

        idx_shift = len(future_events) - 1
        day_blocks_to_keep = self.day_blocks_window[28:]
        self.day_blocks_window = day_blocks_to_keep + future_events

        return idx_shift

    def _roll_backward(self):
        curr_first_monday = self.week_blocks_window[0][0]
        target_monday = curr_first_monday.date - relativedelta(weeks=4)

        start, end = get_time_window_2(target_monday, 4)
        past_events = get_day_blocks(time_min=start, time_max=end)

        idx_shift = len(past_events) - 1
        day_blocks_to_keep = self.day_blocks_window[:-28]
        self.day_blocks_window = past_events + day_blocks_to_keep

        return idx_shift

    def separate_by_weeks(self):
        separated_weeks = []
        num_weeks = round(len(self.day_blocks_window) / 7)
        for x in range(num_weeks):
            start = 7 * x
            end = (7 * x) + 7
            separated_weeks.append(self.day_blocks_window[start: end])

        return separated_weeks


if __name__ == "__main__":
    calendar_interface = CalendarInterface()
    calendar_interface.paginate_days()
    # calendar_interface.paginate_weeks()