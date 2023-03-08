from scrapper_helper import (
    download_single_lecture_video,
    download_multiple_lecture_videos,
)

from rich.console import Console
import pyfiglet
import inquirer

console = Console()


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


def show_inquirer_prompt(message, choices):
    questions = [
        inquirer.List("user_input", message=message, choices=choices, carousel=True),
    ]
    answers = inquirer.prompt(questions)
    return answers.get("user_input")
