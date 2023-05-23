import os
import requests
import json

owner = "ANGELOANTU7"  # Replace with your GitHub username
repo = "intel-hack"  # Replace with your repository name

headers = {
    "Authorization": "Bearer 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",  # Replace with your GitHub access token
    "Accept": "application/vnd.github.v3+json"
}

def get_contributor_commit_counts():
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contributors = response.json()
        commit_counts = {}
        for contributor in contributors:
            author = contributor["author"]["login"]
            commits = contributor["total"]
            commit_counts[author] = commits
        return commit_counts
    else:
        return {}

def update_readme(commit_counts):
    with open("README.md", "r") as file:
        readme_content = file.read()

    # Find the commit statistics section in the README.md file
    start_marker = "## Commit Statistics"
    end_marker = "```"

    start_index = readme_content.find(start_marker)
    end_index = readme_content.find(end_marker, start_index)

    # Generate the commit statistics section content
    content = "\n".join(
        f"![{contributor}](https://img.shields.io/github/commit-activity/y/{owner}/{repo})" 
        for contributor in commit_counts
    )

    # Replace the existing commit statistics section with the updated content
    updated_readme = readme_content[:start_index + len(start_marker) + 1] + "\n\n" + content + "\n\n" + readme_content[end_index:]

    with open("README.md", "w") as file:
        file.write(updated_readme)

commit_counts = get_contributor_commit_counts()
update_readme(commit_counts)
