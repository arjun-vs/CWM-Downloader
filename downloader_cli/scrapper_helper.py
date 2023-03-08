import os

import requests
import tqdm
from bs4 import BeautifulSoup
from timeit import default_timer as timer

from utils import CodeWithMoshUtil

from rich.style import Style

from rich.console import Console

import datetime

console = Console()

INFO_STYLE = Style(color="blue", blink=False, bold=True)
SUCCESS_STYLE = Style(color="green", blink=False, bold=True)
DANGER_STYLE = Style(color="red", blink=False, bold=True)


class CodeWithMoshDownloader(CodeWithMoshUtil):
    def __init__(self, url):
        self.url = url
        self.session = self.initialize_session()
        self.page_timeout = 60

    def soup_html_parser(self, page_url=None):
        if page_url:
            page = self.session.get(page_url, timeout=self.page_timeout)
            return BeautifulSoup(page.content, "html.parser")
        page = self.session.get(self.url, timeout=self.page_timeout)
        return BeautifulSoup(page.content, "html.parser")

    def extract_lecture_urls_for_course(self):
        try:
            soup = self.soup_html_parser()
            lecture_urls = [x.get("data-lecture-url") for x in soup.select("li")]
            final_list = []
            for item in lecture_urls:
                if item != None:
                    formatted_url = "https://codewithmosh.com" + item
                    final_list.append(formatted_url)
            return final_list
        except Exception as e:
            return False

    def extract_download_link(self, page_url):
        try:
            soup = self.soup_html_parser(page_url)
            download_link = (
                soup.find(
                    "div", {"class": "lecture-attachment lecture-attachment-type-video"}
                )
                .find("div", {"class": "video-options"})
                .find("a", {"class": "download"})
                .get("href")
            )
            return download_link
        except Exception as e:
            return False

    def fetch_folder_name(self):
        try:
            soup = self.soup_html_parser()
            return (
                soup.find("section", {"class": "lecture-page-layout"}).find("h2").text
            )
        except Exception:
            return False

    def download_single_file(self, url, dest_folder):
        from cli import show_inquirer_prompt
        from cli import start_cli

        r = requests.get(url, stream=True)
        file_size = int(r.headers["Content-Length"])
        local_filename = (
            r.headers["Content-Disposition"].split("=")[-1].replace('"', "")
        )

        user_input = show_inquirer_prompt(
            message="Please select any options",
            choices=[
                f"Download {local_filename} :: {self.convert_size(file_size)}",
                "Restart Downloader",
                "Exit Downloader",
            ],
        )

        if user_input == f"Download {local_filename} :: {self.convert_size(file_size)}":
            cwd = os.getcwd()
            if not os.path.exists(os.path.join(cwd, dest_folder)):
                os.makedirs(os.path.join(cwd, dest_folder))
            file_path = os.path.join(
                os.path.join(cwd, dest_folder),
                local_filename,
            )
            chunk_size = 1024
            progress_bar_num = int(file_size / chunk_size)
            console.print(
                f"Now Downloading: {local_filename} || File Size: {self.convert_size(file_size)}",
                style=INFO_STYLE,
            )
            start = timer()

            with open(file_path, "wb") as fp:
                for chunk in tqdm.tqdm(
                        r.iter_content(chunk_size=chunk_size),
                        total=progress_bar_num,
                        unit="KB",
                        desc="",
                        leave=True,
                ):
                    fp.write(chunk)
            end = timer()
            elapsed_time = end - start
            return elapsed_time
        elif user_input == "Restart Downloader":
            start_cli()
        elif user_input == "Exit Downloader":
            exit()
        else:
            raise Exception("Invalid input received!")

    def download_multiple_files(self, urls, dest_folder):
        total_filesize = 0
        cwd = os.getcwd()
        if not os.path.exists(os.path.join(cwd, dest_folder)):
            os.makedirs(os.path.join(cwd, dest_folder))
        start = timer()
        file_counter = 0
        for url in urls:
            if not self.extract_download_link(page_url=url):
                continue
            dl_link = self.extract_download_link(page_url=url)
            file_counter += 1
            r = requests.get(dl_link, stream=True)
            file_size = int(r.headers["Content-Length"])
            local_filename = (
                r.headers["Content-Disposition"].split("=")[-1].replace('"', "")
            )
            console.print(
                f"Now Downloading: {local_filename} || File Size: {self.convert_size(file_size)}",
                style=INFO_STYLE,
            )
            file_path = os.path.join(
                os.path.join(cwd, dest_folder), f"{file_counter}_{local_filename}"
            )
            chunk_size = 1024
            progress_bar_num = int(file_size / chunk_size)

            with open(file_path, "wb") as fp:
                for chunk in tqdm.tqdm(
                        r.iter_content(chunk_size=chunk_size),
                        total=progress_bar_num,
                        unit="KB",
                        desc="",
                        leave=True,
                ):
                    fp.write(chunk)
            console.print(
                f"Successfully Downloaded {local_filename}!", style=SUCCESS_STYLE
            )

            total_filesize += file_size
        end = timer()
        elapsed_time = end - start
        return total_filesize, elapsed_time, file_counter

    def get_multiple_download_prompt(self, url, dest_folder):
        from cli import show_inquirer_prompt

        r = requests.get(url, stream=True)
        console.print(
            "NOTE: You are going to download an entire Course. Make sure your connection is stable. If any error occurs you need to download the entire playlist again!",
            style=DANGER_STYLE,
        )
        user_input = show_inquirer_prompt(
            message="Please select any options",
            choices=[
                f"Download {dest_folder}",
                "Restart Downloader",
                "Exit Downloader",
            ],
        )
        return user_input


def download_single_lecture_video():
    from cli import start_cli

    url = input("Enter the URL of the lecture video you wish to download: \n")
    try:
        console.print("Initializing...", style=INFO_STYLE)
        downloader = CodeWithMoshDownloader(url=url)
        console.print("Fetching download URL...", style=INFO_STYLE)
        dl_link = downloader.extract_download_link(page_url=url)
        f = downloader.download_single_file(dl_link, "SingleLectureFilesDownloads")
        console.print(
            f"Successfully Downloaded the file || Elapsed time: {str(datetime.timedelta(seconds=f))} (approx.)",
            style=SUCCESS_STYLE,
        )
        start_cli()

    except Exception as e:
        console.print(
            f"Exception while trying to download. Please check if provided URL is correct! Or check if the configuration.json file is valid! {e.__str__()}",
            style=DANGER_STYLE,
        )


def download_multiple_lecture_videos():
    from cli import start_cli

    util = CodeWithMoshUtil()
    url = input(
        "Enter the URL of the any lecture from the course you wish to download: \n"
    )
    try:
        console.print("Initializing...", style=INFO_STYLE)
        downloader = CodeWithMoshDownloader(url=url)

        user_input = downloader.get_multiple_download_prompt(
            url, downloader.fetch_folder_name()
        )
        if user_input == f"Download {downloader.fetch_folder_name()}":
            console.print("Fetching download URL(s)...", style=INFO_STYLE)
            urls = downloader.extract_lecture_urls_for_course()
            if not urls:
                console.print("Issue fetching download link", style=DANGER_STYLE)
                return
            f = downloader.download_multiple_files(urls, downloader.fetch_folder_name())
            console.print(
                f"Successfully downloaded the Course {downloader.fetch_folder_name()}|| Total file download size: {util.convert_size([0])} || Elapsed time for complete download: {str(datetime.timedelta(seconds=f[1]))} (approx.)|| Total files downloaded: {f[2]} "
            )
            start_cli()
        elif user_input == "Restart Downloader":
            start_cli()
        elif user_input == "Exit":
            exit()
        else:
            raise Exception("Invalid Input received!")
    except Exception as e:
        console.print(
            f"Exception while trying to download. Please check if provided URL is correct! : {e.__str__()}",
            style=DANGER_STYLE,
        )
