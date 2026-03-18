import json
import os
from urllib.parse import urlparse

import requests
from rich.console import Console


class InstructorExamplesCopier:
    def __init__(
        self,
        remote_repo_folder: str,
        out_folder: str | None = None,
        repo: str | None = None,
        console: Console | None = None,
    ) -> None:
        # clean the remote_repo_folder to remove any non-ASCII characters that might cause issues.
        self.remote_repo_folder = self.clean_remote_repo_folder(remote_repo_folder)

        if out_folder:
            print(f"Output folder specified: {out_folder}")
        else:
            out_folder = "."
        # get the repository from settings or by the repo command.
        self.out_folder = out_folder
        if self.out_folder is None:
            self.out_folder = os.getcwd()
        self.repo = repo

        if repo:
            print(f"Repo specified: {repo}")
        else:
            self.settings_file = self.find_settings_file(out_folder)
            if self.settings_file:
                print(f"Found settings file at: {self.settings_file}, parsing...")
                self.settings = self.parse_settings()
                self.repo = self.settings.get("repo")

                print(repo)
            else:
                print(
                    "No settings file found. Please specify the --repo option or ensure "
                    "instructor_examples_settings.json file is in the folder tree."
                )

        # Initialize repo_owner and repo_name to None. They will be set if the repo URL is valid and can be parsed.
        self.repo_owner = None
        self.repo_name = None
        self.parse_repo_url()

    def clean_remote_repo_folder(self, remote_repo_folder: str) -> str:
        cleaned_remote_repo_folder = "".join(c for c in remote_repo_folder if ord(c) < 128)

        return cleaned_remote_repo_folder

    def parse_repo_url(self) -> None:
        """
        Parse the repository URL to extract the owner and repository name.
        This is a placeholder implementation. You can replace it with actual parsing logic.
        """
        if self.repo:
            # this is for github only.
            path = urlparse(self.repo).path.strip("/")
            owner, repo = path.split("/")[:2]
            self.repo_owner = owner
            self.repo_name = repo
        return None

    def copy_repo_contents(
        self,
        repo_folder: str | None = None,
        folder: str | None = None,
        branch: str | None = None,
    ) -> None:
        """
        Recursively copy all files and folders from the GitHub repo to the output folder.
        """
        if repo_folder is None:
            repo_folder = self.remote_repo_folder
        if folder is None:
            folder = self.out_folder + "/" + repo_folder
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        api = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{repo_folder}"
        if branch:
            api += f"?ref={branch}"

        print(f"Fetching: {api}")
        r = requests.get(api)
        r.raise_for_status()
        contents = r.json()
        # loop through the contents and download files or recurse into directories
        print("Downloading Folder:", repo_folder)
        for item in contents:
            if item["type"] == "file":
                file_url = item["download_url"]
                file_path = os.path.join(folder, item["name"])

                content = requests.get(file_url).content
                with open(file_path, "wb") as f:
                    f.write(content)
            elif item["type"] == "dir":
                subfolder = os.path.join(folder, item["name"])
                self.copy_repo_contents(
                    repo_folder=item["path"],
                    folder=subfolder,
                    branch=branch,
                )

    def parse_settings(self) -> dict:
        """
        Parse the settings from the found settings file.
        Returns a dictionary of settings if the file is found and valid, else returns an empty dictionary.
        """
        if not hasattr(self, "settings_file") or not self.settings_file:
            print("No settings file to parse.")
            return {}
        try:
            with open(self.settings_file) as f:
                settings = json.load(f)
                print(f"Parsed settings: {settings}")
                return settings
        except Exception as e:
            print(f"Error parsing settings file: {e}")
            return {}

    def find_settings_file(self, start_path: str | None = None) -> str | None:
        """
        Recursively search up the folder tree for the file instructor_examples_settings.json
        Returns the path to the file if found, else returns None.
        """
        print(
            "Searching for 'instructor_examples_settings.json' starting from:",
            start_path or os.getcwd(),
        )
        if start_path is None:
            start_path = os.getcwd()
        current_dir = os.path.abspath(start_path)

        while True:
            candidate = os.path.join(current_dir, "instructor_examples_settings.json")
            if os.path.isfile(candidate):
                return candidate
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                # Reached the root directory
                return None
            current_dir = parent_dir


def run(
    remote_repo_folder: str,
    repo: str,
    console: Console,
    out_folder: str | None = None,
) -> None:
    copier = InstructorExamplesCopier(
        remote_repo_folder=remote_repo_folder,
        out_folder=out_folder,
        repo=repo,
        console=console,
    )
    copier.copy_repo_contents()
