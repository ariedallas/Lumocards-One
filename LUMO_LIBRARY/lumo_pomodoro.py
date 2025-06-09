import collections
import datetime
import os
import playsound3
import subprocess
import sys
import threading
import time

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_json_utils as l_json_utils
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs

selected_sound = os.path.join(l_files.sounds_folder, "block.mp3")


def play_sound(soundfile):
    playsound3.playsound(soundfile)


class Data:

    @classmethod
    def load_data(cls):
        Data.settings = l_files.get_json_settings()
        Data.pom_settings = Data.settings["pomodoro"]
        Data.default_preset = Data.pom_settings.get("default")
        Data.default_name = Data.default_preset.title().replace("_", " ")
        Data.default_marker = 0 if Data.default_preset == "preset_1" else 1

        Data.toggle_name = "Preset 2" if Data.default_preset == "preset_1" else "Preset 1"
        Data.toggle_setting = "preset_2" if Data.default_preset == "preset_1" else "preset_1"
        Data.p1_tuple = Data.pom_settings["pom_presets"].get("preset_1")
        Data.p2_tuple = Data.pom_settings["pom_presets"].get("preset_2")
        Data.p1_time, Data.p1_break = Data.p1_tuple[0], Data.p1_tuple[1]
        Data.p2_time, Data.p2_break = Data.p2_tuple[0], Data.p2_tuple[1]

        Data.default_timer = Data.pom_settings["pom_presets"].get(Data.default_preset)

        Data.SETUP_MENU = [f"Preset 1:  {int(Data.p1_time)} min. / {int(Data.p1_break)} min. break",
                           f"Preset 2:  {int(Data.p2_time)} min. / {int(Data.p2_break)} min. break",
                           "Set custom pomodoro",
                           "Pomodoro settings"]

        Data.FOCUS_MENU = ["Preset break:",
                           "Break for 7 min.",
                           "Break for 10 min.",
                           "Break for custom amount"]

        Data.BREAK_MENU = ["Start next round:",
                           "Start new custom pomodoro"]

        Data.SETTINGS_MENU = [f"Toggle pomodoro default to ➝ {Data.toggle_name}",
                              "Edit Preset 1",
                              "Edit Preset 2"]

        Data.TIMER_PAUSED_MENU = ["  [Any Key]  Resume timer", "  [X]  Exit"]
        Data.TIMER_RUNNING_MENU = ["  [Any Key]  Pause timer", "  [X]  Exit"]


    @staticmethod
    def valid_float(user_input):
        try:
            float(user_input.strip())
            return True
        except ValueError:
            return False


class Menu:
    def __init__(self, menu):
        self.menus_combined = l_menus_funcs.prep_menu_tuple(menu)
        self.dict_menu = self.menus_combined[0]
        self.list_menu = self.menus_combined[1]


    @classmethod
    def clear(cls):
        subprocess.run(["clear"], shell=True)
        print("\n")


    @classmethod
    def program_header(cls):
        print()
        print("POMODORO")
        print()


    def display(self,
                header_title,
                show_exit=True,
                show_quit=True,
                marker=None):

        if isinstance(marker, int):
            default_action_choice = self.list_menu[marker] + " ➝ (Default action)"
            list_menu_updated = self.list_menu.copy()
            list_menu_updated[marker] = default_action_choice

            print(f"  {header_title.title()}")
            print()
            l_animators.list_printer(list_menu_updated, indent_amt=2, speed_interval=0)
        else:
            print(f"  {header_title.title()}")
            print()
            l_animators.list_printer(self.list_menu, indent_amt=2, speed_interval=0)

        if show_quit or show_exit:
            print()

        if show_exit:
            l_animators.list_printer(l_menus_data.SIMPLE_EXIT_LIST, indent_amt=2, speed_interval=0)
        if show_quit:
            l_animators.list_printer(l_menus_data.QUIT_MENU_LIST, indent_amt=2, speed_interval=0)

        if show_quit or show_exit:
            print()


    def display_2(self, header_title,
                  addnl_text,
                  show_exit=True,
                  show_quit=True,
                  marker=0,
                  ):

        default_action_choice = f"{self.list_menu[marker]} {int(addnl_text)} mins ➝ (Default action)"
        list_menu_updated = self.list_menu.copy()
        list_menu_updated[marker] = default_action_choice

        print(f"  {header_title.title()}")
        print()
        l_animators.list_printer(list_menu_updated, indent_amt=2, speed_interval=0)

        if show_quit or show_exit:
            print()

        if show_exit:
            l_animators.list_printer(l_menus_data.SIMPLE_EXIT_LIST, indent_amt=2, speed_interval=0)
        if show_quit:
            l_animators.list_printer(l_menus_data.QUIT_MENU_LIST, indent_amt=2, speed_interval=0)

        if show_quit or show_exit:
            print()


    @staticmethod
    def simple_display(menu_options, marker=None):
        if isinstance(marker, int):
            default_action_choice = menu_options[marker] + " ➝ (Default action)"
            list_menu_updated = menu_options.copy()
            list_menu_updated[marker] = default_action_choice
            l_animators.list_printer(list_menu_updated, indent_amt=2, speed_interval=0)
        else:

            l_animators.list_printer(menu_options, indent_amt=2, speed_interval=0)


    def menu_update_prepend(self, option, var_menu):
        updated_menu = [option] + var_menu
        self.menus_combined = l_menus_funcs.prep_menu_tuple(updated_menu)
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
    def ask(prompt, show_help_msg=True):
        if show_help_msg:
            l_animators.list_printer(["To use default action, type 'return'",
                                      "or 'enter' without typing a letter first"]
                                     , indent_amt=2
                                     , speed_interval=0)
            print()
        user_input = input(f"  {prompt} >  ")
        val = user_input.strip()
        return val


    @staticmethod
    def validate_minutes(user_input):
        first_try = True
        while True:
            try:
                float_mins = float(user_input.strip())
                return float_mins, first_try

            except ValueError:
                first_try = False
                print()
                l_animators.animate_text("  Try using only numbers (decimals OK)")
                user_input = input("  How many minutes >  ")


    @staticmethod
    def ask_timer(prompt="  Set main timer amount in minutes >  "):
        focus_mins = input(prompt)
        val = focus_mins.strip()
        valid_focus_mins, first_try = Menu.validate_minutes(val)
        return valid_focus_mins, first_try


    @staticmethod
    def ask_break(prompt="  Set how long to take a break for >  "):
        break_mins = input(prompt)
        val = break_mins.strip()
        valid_break_mins, _ = Menu.validate_minutes(val)

        return valid_break_mins


    @staticmethod
    def ask_pomodoro_ratio():
        valid_focus_mins, first_try = Menu.ask_timer()

        if not first_try:
            print()

        valid_break_mins = Menu.ask_break()

        return valid_focus_mins, valid_break_mins


class TimerStandard:
    def __init__(self, initial_mins=0):
        self.initial_mins = initial_mins
        self.secs_elapsed = 0
        self.mins_remain = None
        self.completed = False


    def calculate_mins_remain(self):
        initial_secs = self.initial_mins * 60
        total_secs_remain = initial_secs - self.secs_elapsed
        mins_portion = total_secs_remain // 60
        secs_portion = total_secs_remain % 60
        secs_fraction = round(secs_portion / 60, 2)

        self.mins_remain = mins_portion + secs_fraction


    def format_mins_elapsed(self):
        mins_portion = self.secs_elapsed // 60
        secs_portion = self.secs_elapsed % 60

        return f"{mins_portion:02}:{secs_portion:02}"


    def running_menu(self):
        user_input = input("  ")
        val = user_input.strip().lower()

        if val == "x":
            return "EXIT"
        else:
            return "PAUSE"


    def pause_menu(self):
        paused_amt = self.format_mins_elapsed()

        Menu.clear()
        Menu.program_header()
        l_animators.animate_text(f"  Timer paused at {paused_amt} ...")
        print()
        Menu.simple_display(Data.TIMER_PAUSED_MENU, marker=0)

        user_input = input("  ")
        val = user_input.strip().lower()

        if val == "x":
            return "EXIT"
        else:
            return "RESUME"


    def countdown(self, var_mins, unit=1):
        base_mins = int(var_mins)
        remaining_whole_mins = base_mins
        clip_top_secs = None
        time_is_int = float.is_integer(var_mins)

        try:
            play_sound(selected_sound)
        except:
            print()
            print("  Tried to play a sound...")
            l_animators.list_printer(["But systems are not compatible"], indent_amt=2, finish_delay=.5)

        if not time_is_int:
            remaining_whole_mins = (base_mins - 1) if base_mins > 1 else None
            clip_top_mins = (var_mins - base_mins) + 1 if base_mins > 0 else (var_mins - base_mins)
            clip_top_secs = round(clip_top_mins * 60)

        if clip_top_secs:
            Menu.clear()
            Menu.program_header()
            l_animators.animate_text(f"  Timer currently on minute: {base_mins}+ ...")
            print()
            Menu.simple_display(Data.TIMER_RUNNING_MENU, marker=0)
            print("\n  >  ", end=" ")

            for n in range(clip_top_secs):
                self.secs_elapsed += 1
                if not self.is_running:
                    return
                time.sleep(unit)

        if remaining_whole_mins:
            for n in reversed(range(1, (remaining_whole_mins + 1))):
                Menu.clear()
                Menu.program_header()
                l_animators.animate_text(f"  Timer currently on minute: {n} ...")
                print()
                Menu.simple_display(Data.TIMER_RUNNING_MENU, marker=0)
                print("\n  >  ", end="")

                for s in range(60):
                    self.secs_elapsed += 1
                    if not self.is_running:
                        return
                    time.sleep(unit)

        self.completed = True

        Menu.clear()
        Menu.program_header()
        try:
            for n in range(3):
                play_sound(selected_sound)
        except:
            pass

        print("  Timer finished.\n  press any key to continue >  ", end="")

class TimerDev(TimerStandard):

    def __init__(self, initial_mins=0):
        super().__init__(initial_mins=0)


    def countdown(self, var_mins, unit=1):

        base_mins = int(var_mins)
        remaining_whole_mins = base_mins
        clip_top_secs = None
        time_is_int = float.is_integer(var_mins)

        try:
            play_sound(selected_sound)
        except:
            print()
            print("  Tried to play a sound...")
            l_animators.list_printer(["But systems are not compatible"], indent_amt=2, finish_delay=.5)

        if not time_is_int:
            remaining_whole_mins = (base_mins - 1) if base_mins > 1 else None
            clip_top_mins = (var_mins - base_mins) + 1 if base_mins > 0 else (var_mins - base_mins)
            clip_top_secs = round(clip_top_mins * 60)

        if clip_top_secs:
            Menu.program_header()
            print(f"Dev Timer: {base_mins}+ mins")
            time.sleep(.2)
            print()
            Menu.simple_display(Data.TIMER_RUNNING_MENU, marker=0)
            print("\n  >  ", end=" ")

            if not self.is_running:
                return

        if remaining_whole_mins:
            for n in reversed(range(1, (remaining_whole_mins + 1))):
                Menu.program_header()
                print(f"Dev Timer: {n} mins")
                time.sleep(.2)
                print()
                Menu.simple_display(Data.TIMER_RUNNING_MENU, marker=0)
                print("\n  >  ", end="")

                for s in range(60):
                    self.secs_elapsed += 1
                    if not self.is_running:
                        return

        self.completed = True

        Menu.clear()
        Menu.program_header()

        try:
            for n in range(3):
                play_sound(selected_sound)
        except:
            pass

        print("  Timer finished.\n  press any key to continue >  ", end="")





class PomodoroFlow:

    def __init__(self, timer, focus_mins=None, break_mins=None):

        self.focus_mins = focus_mins
        self.break_mins = break_mins

        self.setup_menu = Menu(Data.SETUP_MENU)
        self.focus_menu = Menu(Data.FOCUS_MENU)
        self.break_menu = Menu(Data.BREAK_MENU)
        self.settings_menu = Menu(Data.SETTINGS_MENU)

        self.user_single_use_break = False
        self.quit_marker = False
        self.exit_marker = False

        self.selected_timer = timer


    def _reload(self):
        self.setup_menu = Menu(Data.SETUP_MENU)
        self.settings_menu = Menu(Data.SETTINGS_MENU)


    def run_setup_loop(self):
        initial_launch = True

        while True:
            if self.quit_marker:
                break

            if initial_launch:
                initial_launch = False
            else:
                Menu.clear()

            Menu.program_header()
            self.setup_menu.display("setup menu", show_exit=False, marker=Data.default_marker)
            val = Menu.ask("Select an option")

            user_choice = self.setup_menu.lookup_user_choice(val)

            if user_choice == "QUIT":
                break

            elif user_choice == "EXIT":
                l_animators.animate_text("  'x' or 'exit' can't be used here", finish_delay=.5)
                continue

            elif not user_choice:
                print()
                l_animators.animate_text("  unrecognized option", finish_delay=.5)

                continue

            self.setup_router(user_choice)

        print()
        # NOTE: this feature is non-essential, but could be optional later
        # l_animators.animate_text_indented("Quit Lumo: Pomodoro", indent_amt=2, finish_delay=.5)


    def setup_router(self, user_choice):

        if user_choice == "DEFAULT":
            self.focus_mins, self.break_mins = Data.default_timer[0], Data.default_timer[1]
            self.focus_break_loop()
        elif user_choice == f"Preset 1:  {int(Data.p1_time)} min. / {int(Data.p1_break)} min. break":
            self.focus_mins, self.break_mins = Data.p1_time, Data.p1_break
            self.focus_break_loop()
        elif user_choice == f"Preset 2:  {int(Data.p2_time)} min. / {int(Data.p2_break)} min. break":
            self.focus_mins, self.break_mins = Data.p2_time, Data.p2_break
            self.focus_break_loop()
        elif user_choice == "Set custom pomodoro":
            self.set_custom_pomodoro()
            self.focus_break_loop()
        elif user_choice == "Pomodoro settings":
            self.go_settings()


    def breaktime_router(self, user_choice):
        if user_choice == "DEFAULT":
            pass
        elif user_choice == "Preset break:":
            pass
        elif user_choice == "Break for 7 min.":
            self.break_mins = 7
            self.user_single_use_break = True
        elif user_choice == "Break for 10 min.":
            self.break_mins = 10
            self.user_single_use_break = True
        elif user_choice == "Break for custom amount":
            self.break_mins = Menu.ask_break()
            self.user_single_use_break = True


    def continuation_router(self, user_choice):
        if user_choice == "DEFAULT":
            pass
        elif user_choice == "Start next round / continue":
            pass
        elif user_choice == "Start new custom pomodoro":
            self.set_custom_pomodoro()


    def settings_router(self, user_choice):
        if user_choice == f"Toggle pomodoro default to ➝ {Data.toggle_name}":
            Data.pom_settings["default"] = Data.toggle_setting
            l_json_utils.write_json(l_files.settings_fullpath, Data.settings)
            Data.load_data()
            self._reload()
            l_animators.animate_text(f"  Default preset is now ➝ {Data.default_name}", finish_delay=1)
        elif user_choice == "Edit Preset 1":
            print()
            preset_1_timer, _ = Menu.ask_timer("  Preset 1, new main timer amount? >  ")
            preset_1_break = Menu.ask_break("  Preset 1, new break amount? >  ")
            new_preset = [preset_1_timer, preset_1_break]
            Data.pom_settings["pom_presets"]["preset_1"] = new_preset

            l_json_utils.write_json(l_files.settings_fullpath, Data.settings)
            Data.load_data()
            self._reload()

            l_animators.animate_text(f"  Preset 1 reset", finish_delay=1)
        elif user_choice == "Edit Preset 2":
            print()
            preset_2_timer, _ = Menu.ask_timer("  Preset 2, new main timer amount? >  ")
            preset_2_break = Menu.ask_break("  Preset 2, new break amount? >  ")
            new_preset = [preset_2_timer, preset_2_break]
            Data.pom_settings["pom_presets"]["preset_2"] = new_preset

            l_json_utils.write_json(l_files.settings_fullpath, Data.settings)
            Data.load_data()
            self._reload()

            l_animators.animate_text(f"  Preset 2 reset", finish_delay=1)
        else:
            pass


    def set_custom_pomodoro(self):
        print()
        self.focus_mins, self.break_mins = Menu.ask_pomodoro_ratio()


    def focus_break_loop(self):
        while True:
            if self.quit_marker:
                break
            elif self.exit_marker:
                self.exit_marker = False
                break

            self.go_focus(self.focus_mins)

            if self.quit_marker:
                break
            elif self.exit_marker:
                self.exit_marker = False
                break

            self.go_break(self.break_mins)


    def run_timer(self):
        self.selected_timer.is_running = True
        self.selected_timer.completed = False
        self.selected_timer.secs_elapsed = 0
        self.selected_timer.calculate_mins_remain()

        while not self.selected_timer.completed:

            timer_thread = threading.Thread(target=self.selected_timer.countdown,
                                            args=(self.selected_timer.mins_remain, 1))
            timer_thread.start()

            running_outcome = self.selected_timer.running_menu()
            if running_outcome == "EXIT":
                self.selected_timer.is_running = False
                return


            elif running_outcome == "PAUSE" and not self.selected_timer.completed:
                self.selected_timer.is_running = False
                self.selected_timer.calculate_mins_remain()
                pause_outcome = self.selected_timer.pause_menu()

                if pause_outcome == "EXIT":
                    return

                elif pause_outcome == "RESUME":
                    self.selected_timer.is_running = True
                    continue


    def go_focus(self, var_mins):
        self.selected_timer.initial_mins = var_mins
        self.run_timer()

        Menu.clear()
        Menu.program_header()

        while True:
            self.focus_menu.display_2("focus completed", self.break_mins)
            val = Menu.ask("Select an option")
            user_choice = self.focus_menu.lookup_user_choice(val)

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

            self.breaktime_router(user_choice)
            break


    def go_break(self, var_mins):
        self.selected_timer.initial_mins = var_mins
        self.run_timer()

        Menu.clear()
        Menu.program_header()

        skip_menu = False

        if self.user_single_use_break:
            self.break_mins = Data.default_timer[1]
            self.user_single_use_break = False

        while True:
            if skip_menu:
                break
            self.break_menu.display_2("break completed", self.focus_mins)
            val = Menu.ask("Select an option")
            user_choice = self.break_menu.lookup_user_choice(val)

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

            self.continuation_router(user_choice)
            break


    def go_settings(self):
        while True:
            Menu.clear()
            Menu.program_header()

            self.settings_menu.display("settings")
            val = Menu.ask("Select an option", show_help_msg=False)
            user_choice = self.settings_menu.lookup_user_choice(val)

            if user_choice == "QUIT":
                self.quit_marker = True
                break
            elif user_choice == "EXIT":
                break
            elif not user_choice:
                print()
                l_animators.animate_text("  unrecognized option", finish_delay=.5)
                Menu.clear()

                continue

            self.settings_router(user_choice)
            break


def main(initial_mins_from_cli=None):
    Data.load_data()
    pomodoro = PomodoroFlow(timer=TimerStandard())

    if initial_mins_from_cli:
        focus_mins, break_mins = initial_mins_from_cli.minutes_focus, initial_mins_from_cli.minutes_break
        valid_focus, valid_break = Data.valid_float(focus_mins), Data.valid_float(break_mins)
        if not (valid_focus and valid_break):
            l_animators.animate_text_indented(f"Unable to make sense of {focus_mins} and {break_mins}",
                                              indent_amt=2)
            l_animators.animate_text_indented(f"Going to pomodoro menu...", indent_amt=2, finish_delay=.5)
            pass
        else:
            pomodoro.focus_mins, pomodoro.break_mins = float(focus_mins), float(break_mins)
            pomodoro.focus_break_loop()
            Menu.clear()

    pomodoro.run_setup_loop()


if __name__ == "__main__":
    main()
