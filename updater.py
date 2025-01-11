import requests
import os
import zipfile
import logging
import time
import subprocess

GITHUB_REPO = "LeviFuzionz/drp"
VERSION_FILE = "version.txt"
CURRENT_VERSION_FILE = "current_version.txt"
UPDATE_URL = "https://github.com/LeviFuzionz/drp/archive/refs/heads/main.zip"
CHECK_INTERVAL = 3600  # Check for updates every hour (3600 seconds)
LOG_FILE = "update_log.txt"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])

def get_current_version():
    if os.path.exists(CURRENT_VERSION_FILE):
        with open(CURRENT_VERSION_FILE, "r") as file:
            return file.read().strip()
    return "0.0.0"

def get_latest_version():
    try:
        response = requests.get(f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{VERSION_FILE}")
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch the latest version: {e}")
        return "0.0.0"

def check_for_updates():
    logging.info("Checking for updates")
    current_version = get_current_version()
    latest_version = get_latest_version()
    if latest_version > current_version:
        logging.info(f"Update available: {latest_version}")
        return True
    return False

def apply_update():
    logging.info("Applying update")
    response = requests.get(UPDATE_URL)
    with open("update.zip", "wb") as file:
        file.write(response.content)
    with zipfile.ZipFile("update.zip", "r") as zip_ref:
        zip_ref.extractall(".")
    os.remove("update.zip")
    with open(CURRENT_VERSION_FILE, "w") as file:
        file.write(get_latest_version())
    logging.info("Update applied")

def check_and_push_changes():
    try:
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout:
            logging.info("Uncommitted changes detected, committing and pushing to GitHub")
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Auto-commit: Applying updates"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
        else:
            logging.info("No uncommitted changes detected")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to push changes: {e}")

def initialize_git_repo():
    if not os.path.exists(".git"):
        logging.info("Initializing new Git repository")
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        logging.info("New Git repository initialized")
        with open("repo_details.txt", "w") as file:
            file.write(f"Repository initialized at {os.getcwd()}\n")
            file.write(f"Remote URL: {GITHUB_REPO}\n")
            file.write(f"Branch: main\n")
        logging.info("Repository details logged in repo_details.txt")

def main():
    initialize_git_repo()
    while True:
        if check_for_updates():
            apply_update()
            check_and_push_changes()
        else:
            logging.info("No updates available")
        logging.info(f"Next check in {CHECK_INTERVAL // 60} minutes")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()