import os
import re
import asyncio
from pathlib import Path
import httpx

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
async def get_latest_repos(client: httpx.AsyncClient, username: str, token: str) -> str:
    headers = {"Authorization": f"token {token}"} if token else {}
    url = f"https://api.github.com/users/{username}/repos"
    params = {"sort": "created", "direction": "desc", "per_page": "5"}
    response = await client.get(url, headers=headers, params=params)
    response.raise_for_status()
    repos = response.json()
    md_lines = []
    for repo in repos:
        md_lines.append(f"* [{repo['name']}]({repo['html_url']})")
    return "\n".join(md_lines)

# Get the 5 most recently updated repos
async def get_latest_releases(client: httpx.AsyncClient, username: str, token: str) -> str:
    headers = {"Authorization": f"token {token}"} if token else {}
    # Use the search API to list repositories that have releases.
    search_url = "https://api.github.com/search/repositories"
    query = f"user:{username} is:public has:releases"
    params = {"q": query, "sort": "updated", "order": "desc", "per_page": "5"}
    response = await client.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    repos = data.get("items", [])
    
    # For each repo, fetch its latest release concurrently
    tasks = []
    for repo in repos:
        repo_name = repo["name"]
        release_url = f"https://api.github.com/repos/{username}/{repo_name}/releases/latest"
        tasks.append(client.get(release_url, headers=headers))
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    md_lines = []
    for repo, resp in zip(repos, responses):
        if isinstance(resp, Exception):
            # In case of an error (for example, no release found), skip this repo.
            continue
        resp.raise_for_status()
        release = resp.json()
        tag = release.get("tag_name", "latest")
        published = release.get("published_at", "")[:10]
        html_url = release.get("html_url", repo["html_url"])
        md_lines.append(f"* [{repo['name']} {tag}]({html_url}) - {published}")
    return "\n".join(md_lines)

# Get the 5 most recent TIL files
async def get_latest_tils(client: httpx.AsyncClient) -> str:
    # Use a SQL query against the TIL JSON endpoint (adjust SQL if needed)
    sql = (
        "select path, replace(title, '_', '\\_') as title, url, topic, slug, created_utc "
        "from til order by created_utc desc limit 5"
    )
    params = {"sql": sql, "_shape": "array"}
    til_url = "https://til.simonwillison.net/tils.json"
    response = await client.get(til_url, params=params)
    response.raise_for_status()
    tils = response.json()
    md_lines = []
    for til in tils:
        date = til["created_utc"].split("T")[0]
        # Use the provided URL or reconstruct one from topic and slug
        url = til.get("url") or f"https://til.simonwillison.net/{til['topic']}/{til['slug']}"
        md_lines.append(f"* [{til['title']}]({url}) - {date}")
    return "\n".join(md_lines)

# Main function
async def main():
    username = os.environ.get("GITHUB_USERNAME", "candelakechkian")
    token = os.environ.get("GITHUB_TOKEN", "")  # Recommended to use a token to avoid rate limits
    
    readme_path = Path(__file__).parent.parent / "README.md"

    async with httpx.AsyncClient() as client:
        latest_repos, latest_releases, latest_tils = await asyncio.gather(
            get_latest_repos(client, username, token),
            get_latest_releases(client, username, token),
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
