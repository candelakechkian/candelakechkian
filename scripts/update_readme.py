import os
import re
import asyncio
from pathlib import Path
import httpx
import datetime

# Configuration variables (set these at the top)
USERNAME = os.environ.get("GITHUB_USERNAME", "candelakechkian")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
# GITHUB_REPOSITORY is automatically set by GitHub Actions; if running locally, set a default:
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

# Get the 5 most recently created repos
async def get_latest_repos(client: httpx.AsyncClient) -> str:
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    url = f"https://api.github.com/users/{USERNAME}/repos"
    params = {"sort": "created", "direction": "desc", "per_page": "5"}
    response = await client.get(url, headers=headers, params=params)
    response.raise_for_status()
    repos = response.json()
    md_lines = []
    for repo in repos:
        md_lines.append(f"* [{repo['name']}]({repo['html_url']})")
    return "\n".join(md_lines)

# Get the 5 most recently updated repos (with releases)
async def get_latest_releases(client: httpx.AsyncClient) -> str:
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    # Use the search API to list repositories that have releases.
    search_url = "https://api.github.com/search/repositories"
    query = f"user:{USERNAME} is:public has:releases"
    params = {"q": query, "sort": "updated", "order": "desc", "per_page": "5"}
    response = await client.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    repos = data.get("items", [])
    
    # For each repo, fetch its latest release concurrently
    tasks = []
    for repo in repos:
        repo_name = repo["name"]
        release_url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/releases/latest"
        tasks.append(client.get(release_url, headers=headers))
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    md_lines = []
    for repo, resp in zip(repos, responses):
        # If the response is an exception, check if it's a 404 (no release exists); if so, skip.
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
        md_lines.append(f"* [{repo['name']} {tag}]({html_url}) - {published}")
    return "\n".join(md_lines)

# Get the 5 most recent TIL files from your local TIL directory
async def get_latest_tils(client: httpx.AsyncClient) -> str:
    # Assume your TIL Markdown files are in a folder named "TIL" at the repo root.
    til_dir = Path(__file__).parent.parent / "TIL"
    if not til_dir.exists():
        return "No TIL directory found."
    
    # List all Markdown files (*.md) in the TIL directory
    til_files = list(til_dir.glob("*.md"))
    if not til_files:
        return "No TIL files found."
    
    # Sort files by modification time (most recent first) and take the first five
    til_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    latest_five = til_files[:5]
    
    md_lines = []
    for file in latest_five:
        # Get the last modification date as a string
        mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime)
        date_str = mtime.strftime("%Y-%m-%d")
        # Use the filename (without extension) as the title
        title = file.stem
        # Build a URL pointing to the file on GitHub (assumes the file is under TIL/)
        url = f"{BASE_GITHUB_URL}/TIL/{file.name}"
        md_lines.append(f"* [{title}]({url}) - {date_str}")
        
    return "\n".join(md_lines)

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
