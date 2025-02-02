import os
import requests
import re

USERNAME = "candelakechkian"
API_BASE = "https://api.github.com"

def get_latest_repos():
    """Fetches the latest public repositories created."""
    url = f"{API_BASE}/users/{USERNAME}/repos?sort=created&per_page=5&type=public"
    response = requests.get(url)
    repos = response.json() if response.status_code == 200 else []
    return [
        f"- [{repo['name']}]({repo['html_url']}) - Created {repo['created_at'][:10]}"
        for repo in repos if not repo.get("private", True)
    ][:5]

def get_latest_releases():
    """Fetches the latest releases across public repositories."""
    url = f"{API_BASE}/users/{USERNAME}/repos?per_page=100&type=public"
    response = requests.get(url)
    repos = response.json() if response.status_code == 200 else []
    releases = []
    for repo in repos:
        repo_name = repo["name"]
        releases_url = f"{API_BASE}/repos/{USERNAME}/{repo_name}/releases/latest"
        release_response = requests.get(releases_url)
        if release_response.status_code == 200:
            release = release_response.json()
            if "tag_name" in release:
                releases.append(
                    f"- [{repo_name} {release['tag_name']}]({release['html_url']}) - Released {release['published_at'][:10]}"
                )
    return releases[:5]

def get_latest_til():
    """Fetches the latest TIL files created."""
    url = f"{API_BASE}/repos/{USERNAME}/TIL/contents"
    response = requests.get(url)
    files = response.json() if response.status_code == 200 else []
    return [
        f"- [{file['name']}]({file['html_url']})"
        for file in files if file.get("type") == "file"
    ][:5]

def update_readme():
    """Updates README.md with latest repos, releases, and TIL."""
    with open("README.md", "r") as file:
        readme = file.read()

    repos_data = "\n".join(get_latest_repos())
    releases_data = "\n".join(get_latest_releases())
    til_data = "\n".join(get_latest_til())

    readme = re.sub(
        r"<!-- LATEST_REPOS_START -->(.*?)<!-- LATEST_REPOS_END -->",
        f"<!-- LATEST_REPOS_START -->\n{repos_data}\n<!-- LATEST_REPOS_END -->",
        readme, flags=re.DOTALL)

    readme = re.sub(
        r"<!-- LATEST_RELEASES_START -->(.*?)<!-- LATEST_RELEASES_END -->",
        f"<!-- LATEST_RELEASES_START -->\n{releases_data}\n<!-- LATEST_RELEASES_END -->",
        readme, flags=re.DOTALL)

    readme = re.sub(
        r"<!-- LATEST_TIL_START -->(.*?)<!-- LATEST_TIL_END -->",
        f"<!-- LATEST_TIL_START -->\n{til_data}\n<!-- LATEST_TIL_END -->",
        readme, flags=re.DOTALL)

    with open("README.md", "w") as file:
        file.write(readme)
