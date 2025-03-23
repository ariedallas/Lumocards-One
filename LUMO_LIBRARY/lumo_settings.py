import time

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_filehandler as l_files

settings = l_files.get_json_settings()


def main():
    formatted_settings = ["SETTINGS", "\n"]
    for k, v in settings.items():
        formatted_settings.append(f"{k.upper()}:")
        formatted_settings.append(f"    {v}")

    l_animators.list_printer(formatted_settings)
    time.sleep(.5)


if __name__ == "__main__":
    main()
