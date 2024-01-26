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
  def __init__(self, id, title, body, state, created_at, closed_at) -> None:
    self.id = id
    self.title = title
    self.body = body
    self.state = state
    self.created_at = created_at
    self.closed_at = closed_at

  def __iter__(self):
    return iter([self.id, self.title, self.body, self.state, self.created_at, self.closed_at])

class Tag:
  def __init__(self, name, sha) -> None:
    self.name = name
    self.sha = sha

  def __iter__(self):
    return iter([self.name, self.sha])

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
    'state': 'all',
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
      state=item['state'],
      created_at=item['created_at'],
      closed_at=item['closed_at'],  
    ) for item in data
  ]

"""
Fetch tags from Github.
"""
def fetch_tags(
  repository_url: str, 
  page: int = 1, 
  per_page: int = 100,
) -> list[Tag]:
  params = {
    'page': page,
    'per_page': per_page,
  }

  url = prepare_url(repository_url, 'tags')
  headers = prepare_headers()

  response = requests.get(url, headers=headers, params=params)
  data = response.json()

  return [
    Tag(
      name=item['name'],
      sha=item['commit']['sha'],
    ) for item in data
  ]

"""
Fetch the data from Github.
"""
def fetch_data(repository_url, fetcher):
  page = 1
  fetched = 0

  with open('output.csv', 'w') as file:
    file = csv.writer(file)

    while True:
      batch = fetcher(repository_url, page)
      file.writerows(batch)

      fetched = fetched + len(batch)
      print('n=' + str(fetched), end='\r')

      if len(batch) < 100:
        break

      page = page + 1

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
  fetch_data(repository_url, fetch_tags)

if __name__ == '__main__':
    main()