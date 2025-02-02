import os
import re
import asyncio
from pathlib import Path
import httpx
import datetime

# Global configuration variables
USERNAME = os.environ.get("GITHUB_USERNAME", "candelakechkian")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
# Use the GITHUB_REPOSITORY env variable (set by GitHub Actions) or default to your repo
REPO = os.environ.get("GITHUB_REPOSITORY", f"{USERNAME}/candelakechkian")
# Base URL to link to files on GitHub (assumes default branch is "main")
BASE_GITHUB_URL = f"https://github.com/{REPO}/blob/main"

def replace_chunk(content: str, marker: str, chunk: str, inline: bool = False) -> str:
    """
    Replace content between markers like:
      <!-- marker starts -->
      ... old content ...
      <!-- marker ends -->
    with new chunk.
    """
    pattern = re.compile(
        r"<!--\s*{} starts\s*-->.*<!--\s*{} ends\s*-->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n" + chunk.strip() + "\n"
    replacement = f"<!-- {marker} starts -->{chunk}<!-- {marker} ends -->"
    return pattern.sub(replacement, content)

# Get the 5 most recently created repos (output as HTML list items)
async def get_latest_repos(client: httpx.AsyncClient) -> str:
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    url = f"https://api.github.com/users/{USERNAME}/repos"
    params = {"sort": "created", "direction": "desc", "per_page": "5"}
    response = await client.get(url, headers=headers, params=params)
    response.raise_for_status()
    repos = response.json()
    html_lines = []
    for repo in repos:
        html_lines.append(f'<li><a href="{repo["html_url"]}">{repo["name"]}</a></li>')
    return "\n".join(html_lines)

# Get the 5 most recently updated repos with releases (output as HTML list items)
async def get_latest_releases(client: httpx.AsyncClient) -> str:
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    search_url = "https://api.github.com/search/repositories"
    query = f"user:{USERNAME} is:public has:releases"
    params = {"q": query, "sort": "updated", "order": "desc", "per_page": "5"}
    response = await client.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    repos = data.get("items", [])
    
    # For each repository, fetch its latest release concurrently
    tasks = []
    for repo in repos:
        repo_name = repo["name"]
        release_url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/releases/latest"
        tasks.append(client.get(release_url, headers=headers))
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    html_lines = []
    for repo, resp in zip(repos, responses):
        if isinstance(resp, Exception):
            if isinstance(resp, httpx.HTTPStatusError) and resp.response.status_code == 404:
                continue
            else:
                continue
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                continue
            else:
                raise
        release = resp.json()
        tag = release.get("tag_name", "latest")
        published = release.get("published_at", "")[:10]
        html_url = release.get("html_url", repo["html_url"])
        html_lines.append(f'<li><a href="{html_url}">{repo["name"]} {tag}</a> - {published}</li>')
    return "\n".join(html_lines)

# Get the 5 most recent TIL files from your local TIL directory (output as HTML list items)
async def get_latest_tils(client: httpx.AsyncClient) -> str:
    # Assuming your TIL Markdown files are stored in a folder named "TIL" at the repository root
    til_dir = Path(__file__).parent.parent / "TIL"
    if not til_dir.exists():
        return "No TIL directory found."
    
    til_files = list(til_dir.glob("*.md"))
    if not til_files:
        return "No TIL files found."
    
    til_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    latest_five = til_files[:5]
    
    html_lines = []
    for file in latest_five:
        mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime)
        date_str = mtime.strftime("%Y-%m-%d")
        title = file.stem
        url = f"{BASE_GITHUB_URL}/TIL/{file.name}"
        html_lines.append(f'<li><a href="{url}">{title}</a> - {date_str}</li>')
    return "\n".join(html_lines)

# Main function
async def main():
    # Adjust the path as needed; this assumes your script is in a subfolder (e.g., "scripts/")
    readme_path = Path(__file__).parent.parent / "README.md"

    async with httpx.AsyncClient() as client:
        latest_repos, latest_releases, latest_tils = await asyncio.gather(
            get_latest_repos(client),
            get_latest_releases(client),
            get_latest_tils(client)
        )
    
    content = readme_path.read_text(encoding="utf-8")
    content = replace_chunk(content, "latest_repos", latest_repos)
    content = replace_chunk(content, "latest_releases", latest_releases)
    content = replace_chunk(content, "latest_tils", latest_tils)
    readme_path.write_text(content, encoding="utf-8")
    print("README.md updated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
