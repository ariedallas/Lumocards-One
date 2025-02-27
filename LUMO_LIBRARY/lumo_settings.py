import pprint

import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_animationlibrary as l_animators

settings = l_files.get_json_settings()

def main():
    formatted_settings = ["SETTINGS", "\n"]
    for k, v in settings.items():
        formatted_settings.append(f"{k.upper()}:")
        formatted_settings.append(f"    {v}")

    l_animators.standard_interval_printer(formatted_settings)
    input("\n   ")


if __name__ == "__main__":
    main()
    # if isinstance(v, dict):
