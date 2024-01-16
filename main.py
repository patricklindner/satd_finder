import dotenv
import csv
import os
import sys
import requests
import re

class Commit:
  def __init__(self, sha, message, date) -> None:
    self.sha = sha
    self.message = message
    self.date = date
  
  def __iter__(self):
    return iter([self.sha, self.message, self.date])

class Issue:
  def __init__(self, id, title, body, created_at, closed_at) -> None:
    self.id = id
    self.title = title
    self.body = body
    self.created_at = created_at
    self.closed_at = closed_at

  def __iter__(self):
    return iter([self.id, self.title, self.body, self.created_at, self.closed_at])

class Release:
  def __init__(self, id, created_at, published_at) -> None:
    self.id = id
    self.created_at = created_at
    self.published_at = published_at

  def __iter__(self):
    return iter([self.id, self.created_at, self.published_at])

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
Fetch commits from Github.
"""
def fetch_commits(
  repository_url: str, 
  page: int = 1, 
  per_page: int = 100,
) -> list[Commit]:
  params = {
    'page': page,
    'per_page': per_page,
  }

  url = prepare_url(repository_url, 'commits')
  headers = prepare_headers()

  response = requests.get(url, headers=headers, params=params)
  data = response.json()

  return [
    Commit(
      sha=item['sha'],
      message=item['commit']['message'],
      date=item['commit']['author']['date'],
    ) for item in data
  ] 

"""
Fetch issues from Github.
"""
def fetch_issues(
  repository_url: str,
  page: int = 1,
  per_page: int = 100,
) -> list[Issue]:
  params = {
    'state': 'closed',
    'page': page,
    'per_page': per_page,
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
Fetch releases from Github.
"""
def fetch_releases(
  repository_url: str, 
  page: int = 1, 
  per_page: int = 100,
) -> list[Release]:
  params = {
    'page': page,
    'per_page': per_page,
  }

  url = prepare_url(repository_url, 'releases')
  headers = prepare_headers()

  response = requests.get(url, headers=headers, params=params)
  data = response.json()

  return [
    Release(
      id=item['id'],
      created_at=item['created_at'],
      published_at=item['published_at'],
    ) for item in data
  ]

"""
Fetch the data from Github.
"""
def fetch_data(repository_url, fetcher):
  data = []
  page = 1

  while True:
    batch = fetcher(repository_url, page)
    data = data + batch

    if len(batch) < 100:
      break

    page = page + 1
  
  with open('output.csv', 'w') as file:
    file = csv.writer(file)
    file.writerows(data)

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
  fetch_data(repository_url, fetch_commits)

if __name__ == '__main__':
    main()