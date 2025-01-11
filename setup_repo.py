import requests
import json
import os
import base64

# Load GitHub username and token from environment variables
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Repository details
REPO_NAME = "drp"
REPO_DESCRIPTION = "Custom Discord Rich Presence application"
PRIVATE = False

def create_github_repo():
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": REPO_NAME,
        "description": REPO_DESCRIPTION,
        "private": PRIVATE
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 201:
        print(f"Repository '{REPO_NAME}' created successfully.")
        return True
    elif response.status_code == 422 and "name already exists" in response.json().get("message", ""):
        print(f"Repository '{REPO_NAME}' already exists. Please choose a different name.")
    else:
        print(f"Failed to create repository: {response.status_code}")
        print(response.json())
    return False

def create_file_in_repo(path, content, message="Initial commit"):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode()
    }
    
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 201:
        print(f"File '{path}' created successfully.")
    else:
        print(f"Failed to create file '{path}': {response.status_code}")
        print(response.json())

def setup_repository_structure():
    # Create a basic directory structure and essential files
    files = {
        "README.md": "# Custom Discord Rich Presence\n\nThis project is a custom Discord Rich Presence application.",
        "requirements.txt": "pypresence\ntkinter\nrequests",
        "src/main.py": "# Main entry point\n\nif __name__ == '__main__':\n    print('Hello, world!')",
        "src/gui.py": "# GUI code",
        "src/discord_rpc.py": "# Discord RPC code",
        "src/auth.py": "# Authentication code",
        "src/settings.py": "# Settings code",
        "src/notifications.py": "# Notifications code",
        "src/updater.py": "# Updater code",
        "src/background_service.py": "# Background service code",
        "src/privacy.py": "# Privacy code",
        "src/analytics.py": "# Analytics code",
        "src/utils/__init__.py": "# Utility functions and classes"
    }
    
    for path, content in files.items():
        create_file_in_repo(path, content)

if __name__ == "__main__":
    if GITHUB_USERNAME and GITHUB_TOKEN:
        if create_github_repo():
            setup_repository_structure()
    else:
        print("Please set the GITHUB_USERNAME and GITHUB_TOKEN environment variables.")