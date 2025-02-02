import os
import re
import asyncio
from pathlib import Path
import httpx
import datetime

# Global configuration for your main repository
USERNAME = os.environ.get("GITHUB_USERNAME", "candelakechkian")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPOSITORY", f"{USERNAME}/candelakechkian")
BASE_GITHUB_URL = f"https://github.com/{REPO}/blob/main"

# Global configuration for your TIL repository
TIL_REPO = os.environ.get("TIL_REPO", "candelakechkian/TIL")
TIL_BASE_URL = f"https://github.com/{TIL_REPO}/blob/main"

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

# Get the 5 most recently created repos (as HTML list items)
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

# Get the 5 most recently updated repos (as HTML list items)
async def get_latest_updated_repos(client: httpx.AsyncClient) -> str:
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    url = f"https://api.github.com/users/{USERNAME}/repos"
    params = {"sort": "updated", "direction": "desc", "per_page": "5"}
    response = await client.get(url, headers=headers, params=params)
    response.raise_for_status()
    repos = response.json()
    html_lines = []
    for repo in repos:
        updated_date = repo.get("updated_at", "")[:10]
        html_lines.append(f'<li><a href="{repo["html_url"]}">{repo["name"]}</a> - {updated_date}</li>')
    return "\n".join(html_lines)

# Get the 5 most recent TIL files from your TIL repository (as HTML list items)
async def get_latest_tils(client: httpx.AsyncClient) -> str:
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    # List the contents of the TIL repository (assumes files are in the root)
    contents_url = f"https://api.github.com/repos/{TIL_REPO}/contents"
    response = await client.get(contents_url, headers=headers)
    response.raise_for_status()
    files = response.json()
    # Filter for Markdown files
    til_files = [f for f in files if f.get("type") == "file" and f["name"].endswith(".md")]
    if not til_files:
        return "No TIL files found."
    
    # For each file, get its latest commit info to retrieve the commit date.
    async def get_file_commit_info(file):
        commits_url = f"https://api.github.com/repos/{TIL_REPO}/commits?path={file['path']}&per_page=1"
        commit_resp = await client.get(commits_url, headers=headers)
        commit_resp.raise_for_status()
        commits = commit_resp.json()
        if not commits:
            return None
        commit_date = commits[0]["commit"]["committer"]["date"]
        return {
            "name": file["name"],
            "path": file["path"],
            "html_url": file["html_url"],
            "commit_date": commit_date,
        }
    
    tasks = [get_file_commit_info(file) for file in til_files]
    commit_infos = await asyncio.gather(*tasks, return_exceptions=True)
    valid_infos = []
    for info in commit_infos:
        if isinstance(info, Exception) or info is None:
            continue
        valid_infos.append(info)
    
    # Sort files by commit_date (most recent first)
    valid_infos.sort(key=lambda x: x["commit_date"], reverse=True)
    latest_five = valid_infos[:5]
    
    html_lines = []
    for info in latest_five:
        commit_dt = datetime.datetime.fromisoformat(info["commit_date"].replace("Z", "+00:00"))
        date_str = commit_dt.strftime("%Y-%m-%d")
        title = Path(info["name"]).stem
        url = info["html_url"] or f"{TIL_BASE_URL}/{info['name']}"
        html_lines.append(f'<li><a href="{url}">{title}</a> - {date_str}</li>')
    
    return "\n".join(html_lines)

# Main function
async def main():
    # Adjust the path as needed; this assumes your script is in a subfolder (e.g., "scripts/")
    readme_path = Path(__file__).parent.parent / "README.md"
    async with httpx.AsyncClient() as client:
        latest_repos, latest_updated_repos, latest_tils = await asyncio.gather(
            get_latest_repos(client),
            get_latest_updated_repos(client),
            get_latest_tils(client)
        )
    
    content = readme_path.read_text(encoding="utf-8")
    content = replace_chunk(content, "latest_repos", latest_repos)
    # We replace the marker "latest_releases" with the output from get_latest_updated_repos
    content = replace_chunk(content, "latest_releases", latest_updated_repos)
    content = replace_chunk(content, "latest_tils", latest_tils)
    readme_path.write_text(content, encoding="utf-8")
    print("README.md updated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
