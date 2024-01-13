import dotenv
import os
import sys
import requests
import re

class Issue:
  def __init__(self, id, title, body, created_at, closed_at) -> None:
    self.id = id
    self.title = title
    self.body = body
    self.created_at = created_at
    self.closed_at = closed_at

"""
Load the Github authentication token from the environment.
"""
def load_github_token() -> str:
  return os.getenv('GITHUB_TOKEN')

"""
Prepare the Github API url.
"""
def prepare_url(repository_url: str, endpoint: str) -> str:
  pattern = r"https://github\.com/(.+)/(.+)"
  match = re.match(pattern, repository_url)

  return 'https://api.github.com/repos/' + match.group(1) + '/' + match.group(2) + '/' + endpoint

"""
Prepare the Github API headers.
"""
def prepare_headers() -> dict:
  return {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer ' + load_github_token(),
    'X-Github-Api-Version': '2022-11-28',
  } 

"""
Fetch issues from Github.
"""
def fetch_issues(repository_url: str) -> list[Issue]:
  params = {
    'state': 'closed',
  }

  url = prepare_url(repository_url, 'issues')
  headers = prepare_headers()

  response = requests.get(url, headers=headers, params=params)
  data = response.json()

  return [
    Issue(
      id=item['id'],
      title=item['title'],
      body=item['body'],
      created_at=item['created_at'],
      closed_at=item['closed_at'],  
    ) for item in data
  ]

"""
Entrypoint.
"""
def main() -> None:
  dotenv.load_dotenv()

  if len(sys.argv) < 2:
    print('Please provide a repository URL as first argument.')
    exit(1)
    
  # The repository URL is passed as the first argument
  repository_url = sys.argv[1]
  issues = fetch_issues(repository_url)

  print(len(issues))

if __name__ == '__main__':
    main()