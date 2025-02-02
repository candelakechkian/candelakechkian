import os
import requests

USERNAME = "candelakechkian"
API_BASE = "https://api.github.com"

def get_latest_repos():
    """Fetches the latest public repositories created."""
    url = f"{API_BASE}/users/{USERNAME}/repos?sort=created&per_page=5&type=public"
    repos = requests.get(url).json()
    return [f"- [{repo['name']}]({repo['html_url']}) - Created {repo['created_at'][:10]}"
            for repo in repos if not repo.get("private", True)][:5]

def get_latest_releases():
    """Fetches the latest releases across all public repositories."""
    url = f"{API_BASE}/users/{USERNAME}/repos?per_page=100&type=public"
    repos = requests.get(url).json()

    return [
        f"- [{repo['name']} {release['tag_name']}]({release['html_url']}) - Released {release['published_at'][:10]}"
        for repo in repos if not repo.get("private", True)
        for release in [requests.get(f"{API_BASE}/repos/{USERNAME}/{repo['name']}/releases/latest").json()]
        if isinstance(release, dict) and "tag_name" in release][:5]
  
def get_latest_til():
  """Fetches the latest TIL files created."""
  return [
    f"- [{file['name']}]({file['html_url']})"
    for file in requests.get(f"{API_BASE}/repos/{USERNAME}/TIL/contents").json()
    if file.get("type") == "file"][:5]

def update_readme():
    """Updates README.md with latest repos, releases, and TIL."""
    with open("README.md", "r") as file:
        readme = file.readlines()

    start_repos = readme.index("<!-- LATEST_REPOS_START -->\n") + 1
    end_repos = readme.index("<!-- LATEST_REPOS_END -->\n")

    start_releases = readme.index("<!-- LATEST_RELEASES_START -->\n") + 1
    end_releases = readme.index("<!-- LATEST_RELEASES_END -->\n")

    start_til = readme.index("<!-- LATEST_TIL_START -->\n") + 1
    end_til = readme.index("<!-- LATEST_TIL_END -->\n")

    readme[start_repos:end_repos] = [f"{line}\n" for line in get_latest_repos()]
    readme[start_releases:end_releases] = [f"{line}\n" for line in get_latest_releases()]
    readme[start_til:end_til] = [f"{line}\n" for line in get_latest_til_files()]

    with open("README.md", "w") as file:
        file.writelines(readme)

if __name__ == "__main__":
    update_readme()
