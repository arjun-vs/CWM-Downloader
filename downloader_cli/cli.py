from scrapper_helper import (
    download_single_lecture_video,
    download_multiple_lecture_videos,
)

from rich.console import Console
import pyfiglet
import inquirer

console = Console()


# def start_cli():
#     print(pyfiglet.figlet_format("CWM - D", font="5lineoblique"))
#
#
#     user_input = show_prompt(
#         options=[
#             "Download a single video from URL",
#             "Download all videos from a course",
#             "Exit",
#         ]
#     )
#     if user_input == 0:
#         download_single_lecture_video()
#     elif user_input == 1:
#         download_multiple_lecture_videos()
#     elif user_input == 2:
#         exit()
#     else:
#         console.print(
#             "Invalid Input/Error Processing Input",
#             style=Style(color="red", blink=False, bold=True),
#         )


def start_cli():
    print(pyfiglet.figlet_format("CWM - D", font="5lineoblique"))

    user_input = show_inquirer_prompt(
        message="Please select any options",
        choices=[
            "Download a single video from URL",
            "Download all videos from a course",
            "Exit",
        ],
    )
    if user_input == "Download a single video from URL":
        download_single_lecture_video()
    elif user_input == "Download all videos from a course":
        download_multiple_lecture_videos()
    elif user_input == "Exit":
        exit()


# def show_prompt(options):
#     terminal_menu = TerminalMenu(options)
#     menu_entry_index = terminal_menu.show()
#     return menu_entry_index


def show_inquirer_prompt(message, choices):
    questions = [
        inquirer.List("user_input", message=message, choices=choices, carousel=True),
    ]
    answers = inquirer.prompt(questions)
    return answers.get('user_input')

