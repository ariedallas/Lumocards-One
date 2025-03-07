import collections
import datetime
import subprocess
import time

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_json_utils as l_json_utils
import LUMO_LIBRARY.lumo_menus as l_menus


class Data:

    @classmethod
    def load_data(cls):
        Data.settings = l_files.get_json_settings()
        Data.pom_settings = Data.settings["pomodoro"]
        Data.default = Data.pom_settings.get("default")
        Data.default_name = Data.default.title().replace("_", " ")
        Data.toggle_name = "Preset 2" if Data.default == "preset_1" else "Preset 1"
        Data.toggle_setting = "preset_2" if Data.default == "preset_1" else "preset_1"
        Data.default_marker = 0 if Data.default == "preset_1" else 1

        Data.p1_tuple = Data.pom_settings["pom_presets"].get("preset_1")
        Data.p2_tuple = Data.pom_settings["pom_presets"].get("preset_2")

        Data.p1_time, Data.p1_break = Data.p1_tuple[0], Data.p1_tuple[1]
        Data.p2_time, Data.p2_break = Data.p2_tuple[0], Data.p2_tuple[1]

        Data.default_timer = Data.pom_settings["pom_presets"].get(Data.default)

        Data.SETUP_MENU = [f"Preset 1:  {int(Data.p1_time)} min. / {int(Data.p1_break)} min. break",
                           f"Preset 2:  {int(Data.p2_time)} min. / {int(Data.p2_break)} min. break",
                           "Set custom pomodoro",
                           "Pomodoro settings",
                           "Log | stats"]

        Data.TIMER_MENU = ["Break for 7 min.",
                           "Break for 10 min.",
                           "Break for custom amount",
                           "Preset break, then start a new custom pomodoro",
                           "Log | stats"]

        Data.BREAK_MENU = ["Start next round / continue",
                           "Start new custom pomodoro",
                           "Log | stats"]

        Data.SETTINGS_MENU = [f"Toggle pomodoro default to ➝ {Data.toggle_name}",
                              "Edit Preset 1",
                              "Edit Preset 2"]


class Menu:
    def __init__(self, menu):
        self.menus_combined = l_menus.prep_menu(menu)
        self.dict_menu = self.menus_combined[0]
        self.list_menu = self.menus_combined[1]


    @classmethod
    def clear(cls):
        subprocess.run(["clear"], shell=True)
        print("\n\n")


    @classmethod
    def program_header(cls):
        print("POMODORO")
        print()


    def display(self, show_exit=True, show_quit=True, marker=None):
        if isinstance(marker, int):
            marked_line = self.list_menu[marker] + " ➝ (Default action)"
            list_menu_marked = self.list_menu.copy()
            list_menu_marked[marker] = marked_line
            l_animators.standard_interval_printer(list_menu_marked, speed_interval=0)
        else:
            l_animators.standard_interval_printer(self.list_menu, speed_interval=0)

        if show_quit or show_exit:
            print()

        if show_exit:
            l_animators.standard_interval_printer(l_menus.simple_exit, speed_interval=0)
        if show_quit:
            l_animators.standard_interval_printer(l_menus.quit_menu, speed_interval=0)

        if show_quit or show_exit:
            print()


    def prepend_update(self, option, var_menu):
        updated_menu = [option] + var_menu
        self.menus_combined = l_menus.prep_menu(updated_menu)
        self.dict_menu = self.menus_combined[0]
        self.list_menu = self.menus_combined[1]


    def lookup_user_choice(self, user_input):
        if user_input.upper() in self.dict_menu.keys():
            return self.dict_menu[user_input.upper()]
        elif user_input.lower() in {"q", "quit"}:
            return "QUIT"
        elif user_input.lower() in {"x", "exit"}:
            return "EXIT"
        elif user_input == "":
            return "DEFAULT"
        else:
            return None


    @staticmethod
    def ask(prompt, show_dflt_msg=True):
        if show_dflt_msg:
            print("  (To use default action, type 'return'"
                  "\n   or 'enter' without typing a letter first)")
            print()
        user_input = input(f"  {prompt} >  ")
        return user_input


    @staticmethod
    def validate_minutes(user_input):
        first_try = True
        while True:
            try:
                float_mins = float(user_input)
                return float_mins, first_try

            except ValueError as e:
                first_try = False
                print()
                l_animators.animate_text("  Try using only numbers (decimals OK)")
                user_input = input("  Set timer in minutes >  ")


    @staticmethod
    def ask_timer(prompt="  Set timer amount in minutes >  "):
        mins_timer = input(prompt)
        validated_on, first_try = Menu.validate_minutes(mins_timer)
        return validated_on, first_try


    @staticmethod
    def ask_break(prompt="  Set how long to take a break for >  "):
        mins_break = input(prompt)
        validated_break, _ = Menu.validate_minutes(mins_break)

        return validated_break


    @staticmethod
    def ask_pomodoro_ratio():
        validated_on, first_try = Menu.ask_timer()

        if not first_try:
            print()

        validated_break = Menu.ask_break()

        return validated_on, validated_break


class Pomodoro:
    round_counter_int = 0
    current_round = {}
    log = collections.deque()


    def __init__(self, mins_timer=None, mins_break=None):

        self.mins_timer = mins_timer
        self.mins_break = mins_break
        self.temp_1 = None
        self.temp_2 = None

        self.user_on_custom_break = False
        self.user_request_new_pomodoro = False
        self.setup_menu = Menu(Data.SETUP_MENU)
        self.timer_menu = Menu(Data.TIMER_MENU)
        self.break_menu = Menu(Data.BREAK_MENU)
        self.settings_menu = Menu(Data.SETTINGS_MENU)

        self.quit_marker = False
        self.exit_marker = False


    @classmethod
    def _update_json_settings(cls):
        l_json_utils.write_json(l_files.settings_fullpath, Data.settings)


    def _reload(self):
        self.setup_menu = Menu(Data.SETUP_MENU)
        self.settings_menu = Menu(Data.SETTINGS_MENU)


    @staticmethod
    def round_counter(func):
        def wrapper(*args, **kwargs):
            Pomodoro.round_counter_int += 1
            result = func(*args, **kwargs)
            return result


        return wrapper



    def round_updater(self, status):
        if status == "focus":
            Pomodoro.current_round["focus"] = self.mins_timer
        elif status == "break":
            Pomodoro.current_round["break"] = self.mins_break



    def run_setup_loop(self):

        while True:
            if self.quit_marker:
                break

            Menu.clear()
            Menu.program_header()
            self.setup_menu.display(show_exit=False, marker=Data.default_marker)
            user_input = Menu.ask("Select an option")
            user_choice = self.setup_menu.lookup_user_choice(user_input)

            if user_choice == "QUIT":
                break

            if not user_choice:
                print()
                l_animators.animate_text("  unrecognized option", finish_delay=.5)

                continue

            self.setup_router(user_choice)

        print()
        l_animators.animate_text("  Quit Lumo: Pomodoro", finish_delay=.5)


    def setup_router(self, user_choice):
        if user_choice == "DEFAULT":
            self.mins_timer, self.mins_break = Data.default_timer[0], Data.default_timer[1]
            self.timer_menu.prepend_update(f"Preset break: {self.mins_break} min.", Data.TIMER_MENU)
            self.run_timer_loop()
        elif user_choice == f"Preset 1:  {int(Data.p1_time)} min. / {int(Data.p1_break)} min. break":
            self.mins_timer, self.mins_break = Data.p1_time, Data.p1_break
            self.timer_menu.prepend_update(f"Preset break: {self.mins_break} min.", Data.TIMER_MENU)
            self.run_timer_loop()
        elif user_choice == f"Preset 2:  {int(Data.p2_time)} min. / {int(Data.p2_break)} min. break":
            self.mins_timer, self.mins_break = Data.p2_time, Data.p2_break
            self.timer_menu.prepend_update(f"Preset break: {self.mins_break} min.", Data.TIMER_MENU)
            self.run_timer_loop()
        elif user_choice == "Set custom pomodoro":
            self.set_custom_pomodoro()
            self.timer_menu.prepend_update(f"Preset break: {self.mins_break} min.", Data.TIMER_MENU)
            self.run_timer_loop()
        elif user_choice == "Pomodoro settings":
            self.go_settings()
        else:  # Log | stats
            Pomodoro.display_log()


    def timer_router(self, user_choice):
        if user_choice == "DEFAULT":
            pass
        elif user_choice == f"Preset break: {self.mins_break} min.":
            pass
        elif user_choice == "Break for 7 min.":
            self.mins_break = 7
            self.user_on_custom_break = True
        elif user_choice == "Break for 10 min.":
            self.mins_break = 10
            self.user_on_custom_break = True
        elif user_choice == "Break for custom amount":
            self.mins_break = Menu.ask_break()
            self.user_on_custom_break = True
        elif user_choice == "Preset break, then start a new custom pomodoro":
            self.user_request_new_pomodoro = True
        else:  # Log | stats
            Pomodoro.display_log()


    def break_router(self, user_choice):
        if user_choice == "DEFAULT":
            pass
        elif user_choice == "Start next round / continue":
            pass
        elif user_choice == "Start new custom pomodoro":
            self.set_custom_pomodoro()
        else:
            Pomodoro.display_log()


    def settings_router(self, user_choice):
        if user_choice == f"Toggle pomodoro default to ➝ {Data.toggle_name}":
            Data.pom_settings["default"] = Data.toggle_setting
            l_json_utils.write_json(l_files.settings_fullpath, Data.settings)
            Data.load_data()
            self._reload()
            l_animators.animate_text(f"  Default preset is now ➝ {Data.default_name}", finish_delay=1)
        elif user_choice == "Edit Preset 1":
            print()
            preset_1_timer, _ = Menu.ask_timer("  Preset 1, new timer amount? >  ")
            preset_1_break = Menu.ask_break("  Preset 1, new break amount? >  ")
            new_preset = [preset_1_timer, preset_1_break]
            Data.pom_settings["pom_presets"]["preset_1"] = new_preset

            l_json_utils.write_json(l_files.settings_fullpath, Data.settings)
            Data.load_data()
            self._reload()

            l_animators.animate_text(f"  Preset 1 reset", finish_delay=1)
        elif user_choice == "Edit Preset 2":
            pass
        else:
            pass


    def run_timer_loop(self):
        while True:
            if self.quit_marker:
                break
            elif self.exit_marker:
                # self.round_logger("exit from break")
                self.exit_marker = False
                break
            self.go_timer(self.mins_timer)

            if self.quit_marker:
                break
            elif self.exit_marker:
                # self.round_logger("exit from focus")
                self.exit_marker = False
                break
            self.go_break(self.mins_break)


    def set_custom_pomodoro(self):
        print()
        self.mins_timer, self.mins_break = Menu.ask_pomodoro_ratio()


    @round_counter
    def go_timer(self, mins):
        Menu.clear()
        Menu.program_header()
        print(f"    {self.mins_timer}")

        print("    .")
        time.sleep(.3)

        print("    .")
        time.sleep(.3)

        print("    .")
        time.sleep(.3)
        print()

        l_animators.animate_text("  Timer finished")
        print()
        self.round_updater("focus")
        self.round_logger("focus")

        while True:
            self.timer_menu.display(marker=0)
            user_input = Menu.ask("Select an option")
            user_choice = self.timer_menu.lookup_user_choice(user_input)

            if user_choice == "QUIT":
                self.quit_marker = True
                break
            elif user_choice == "EXIT":
                self.exit_marker = True
                break
            elif not user_choice:
                print()
                l_animators.animate_text("  unrecognized option", finish_delay=.5)
                Menu.clear()
                Menu.program_header()

                continue

            self.timer_router(user_choice)
            break


    def go_break(self, mins):
        Menu.clear()
        Menu.program_header()
        print(f"    {self.mins_break}")

        print("    _")
        time.sleep(.3)

        print("    _")
        time.sleep(.3)

        print("    _")
        time.sleep(.3)
        print()

        l_animators.animate_text("  Break finished")
        print()
        self.round_updater("break")
        self.round_logger("break")

        skip_menu = False

        if self.user_request_new_pomodoro:
            self.mins_timer, _ = Menu.ask_timer("  New timer amount? >  ")
            self.mins_break = Menu.ask_break("  New break amount? >  ")
            self.timer_menu.prepend_update(f"Preset break: {self.mins_break} min.", Data.TIMER_MENU)

            self.user_request_new_pomodoro = False
            skip_menu = True
            print()

        if self.user_on_custom_break:
            self.mins_break = Data.default_timer[1]
            self.user_on_custom_break = False

        while True:
            if skip_menu:
                break

            self.break_menu.display(marker=0)
            user_input = Menu.ask("Select an option")
            user_choice = self.break_menu.lookup_user_choice(user_input)

            if user_choice == "QUIT":
                self.quit_marker = True
                break
            elif user_choice == "EXIT":
                self.exit_marker = True
                break
            elif not user_choice:
                print()
                l_animators.animate_text("  unrecognized option", finish_delay=.5)
                Menu.clear()
                Menu.program_header()

                continue

            self.break_router(user_choice)
            break


    def go_settings(self):
        while True:
            Menu.clear()
            Menu.program_header()
            time.sleep(.2)

            self.settings_menu.display()
            user_input = Menu.ask("Select an option", show_dflt_msg=False)
            user_choice = self.settings_menu.lookup_user_choice(user_input)

            if user_choice == "QUIT":
                self.quit_marker = True
                break
            elif user_choice == "EXIT":
                self.exit_marker = True
                break
            elif not user_choice:
                print()
                l_animators.animate_text("  unrecognized option", finish_delay=.5)
                Menu.clear()

                continue

            self.settings_router(user_choice)
            break


    @classmethod
    def round_logger(cls, status):
        possible_text_focus = "min." if Pomodoro.current_round.get("focus") else ""
        possible_text_break = "min." if Pomodoro.current_round.get("break") else ""

        focus_text = f"Focus: {Pomodoro.current_round.get("focus")} {possible_text_focus}"
        break_text = f"Break: {Pomodoro.current_round.get("break")} {possible_text_break}"
        curr_round = f"Rnd{Pomodoro.round_counter_int} — {focus_text} | {break_text}"

        if status == "focus":
            Pomodoro.log.appendleft(curr_round)
        elif status == "break":
            Pomodoro.log.popleft()
            Pomodoro.log.appendleft(curr_round)
            Pomodoro.current_round = {}
        # elif status == "exit from focus":
        #     pass
        # elif status == "exit from break":
        #     Pomodoro.log.popleft()
        #     Pomodoro.log.appendleft(curr_round)
        #     Pomodoro.current_round = {}

    @classmethod
    def display_log(cls):
        today_date = datetime.date.today().strftime("%m/%d/%Y")

        Menu.clear()
        Menu.program_header()

        print("  Session Log:")
        print(f"  {today_date}")
        print()

        if not Pomodoro.log:
            l_animators.animate_text("  Nothing to display for this session")
        else:
            for record in Pomodoro.log:
                print(f"  {record}")

        print()
        Menu.ask("Type any key to continue", show_dflt_msg=False)



def main():
    Data.load_data()
    pomodoro = Pomodoro()
    pomodoro.run_setup_loop()


if __name__ == "__main__":
    main()
