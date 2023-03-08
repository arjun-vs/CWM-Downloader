import os
import pathlib
import json

import math
import secrets
import string

from requests import Session
from requests.utils import cookiejar_from_dict
from requests.structures import CaseInsensitiveDict
from rich.console import Console
from rich.style import Style

console = Console()

ERROR_STYLE = Style(color="red", blink=False, bold=True)

CREDENTIALS_FILE = pathlib.Path(os.path.join(os.getcwd(), "credentials.json"))


class CodeWithMoshUtil:
    def load_credentials(self):
        if not CREDENTIALS_FILE.exists():
            console.print(
                f"Failed to find credentials.json file in {os.getcwd()}",
                style=ERROR_STYLE,
            )
        return CREDENTIALS_FILE

    def get_credentials(self):
        credentials_file = self.load_credentials()
        credentials_dict = json.loads(credentials_file.read_text())
        if "headers" not in credentials_dict or "cookies" not in credentials_dict:
            console.print(
                "The contents in credentials.json are invalid.", style=ERROR_STYLE
            )
        return credentials_dict

    def initialize_session(self):
        try:
            session = Session()
            credentials = self.get_credentials()
            session.cookies = cookiejar_from_dict(credentials["cookies"])
            session.headers = CaseInsensitiveDict(credentials["headers"])
            return session
        except Exception:
            raise Exception(
                "Exception in initializing session. Check the credentials.json file!"
            )

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
