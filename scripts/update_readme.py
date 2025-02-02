import os
import requests
import re

USERNAME = "candelakechkian"
API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Accept": "application/vnd.github.v3+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

def fetch_data(url):
    """Helper function to fetch API data with error handling."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return []
    return response.json()

def get_latest_repos():
    """Fetches the latest public repositories created."""
    url = f"{API_BASE}/users/{USERNAME}/repos?sort=created&per_page=5&type=public"
    repos = fetch_data(url)
    return [f"- [{repo['name']}]({repo['html_url']}) - Created {repo['created_at'][:10]}" for repo in repos][:5]

def get_latest_releases():
    """Fetches the latest releases across public repositories."""
    url = f"{API_BASE}/users/{USERNAME}/repos?per_page=100&type=public"
    repos = fetch_data(url)
    releases = []
    for repo in repos:
        release = fetch_data(f"{API_BASE}/repos/{USERNAME}/{repo['name']}/releases/latest")
        if "tag_name" in release:
            releases.append(f"- [{repo['name']} {release['tag_name']}]({release['html_url']}) - Released {release['published_at'][:10]}")
    return releases[:5]

def get_latest_til():
    """Fetches the latest TIL files created."""
    url = f"{API_BASE}/repos/{USERNAME}/TIL/contents"
    files = fetch_data(url)
    return [f"- [{file['name']}]({file['html_url']})" for file in files if file.get("type") == "file"][:5]

def update_readme():
    """Updates README.md with latest repos, releases, and TIL."""
    with open("README.md", "r") as file:
        readme = file.read()

    replacements = {
        "LATEST_REPOS": "\n".join(get_latest_repos()),
        "LATEST_RELEASES": "\n".join(get_latest_releases()),
        "LATEST_TIL": "\n".join(get_latest_til())
    }

    for key, value in replacements.items():
        readme = re.sub(f"<!-- {key}_START -->(.*?)<!-- {key}_END -->",
                        f"<!-- {key}_START -->\n{value}\n<!-- {key}_END -->",
                        readme, flags=re.DOTALL)

    with open("README.md", "w") as file:
        file.write(readme)
