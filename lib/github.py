import os
import csv
import requests
import re
from lib.models import Commit, Tag, Issue, PullRequest

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

def fetch_prs(
    repository_url: str,
    page: int = 1,
    per_page: int = 100,
) -> list[PullRequest]:
  params = {
    'state': 'all',
    'page': page,
    'per_page': per_page,
  }

  url = prepare_url(repository_url, 'pulls')
  headers = prepare_headers()

  response = requests.get(url, headers=headers, params=params)
  data = response.json()

  return [
    PullRequest(
      id=item['id'],
      title=item['title'],
      body=item['body'],
      state=item['state'],
      created_at=item['created_at'],
      closed_at=item['closed_at'],
      merged_at=item['merged_at']
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

  issues = []
  for item in data:
    if 'pull_request' not in item.keys():
      issues.append(Issue(
        id=item['id'],
        title=item['title'],
        body=item['body'],
        state=item['state'],
        created_at=item['created_at'],
        closed_at=item['closed_at'],
        pull_request=item.get('pull_request', None),
      ))
  
  return issues

  return [
    Issue(
      id=item['id'],
      title=item['title'],
      body=item['body'],
      state=item['state'],
      created_at=item['created_at'],
      closed_at=item['closed_at'],  
      pull_request=item.get('pull_request', None),
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
  print(data)

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

  with open('output.csv', 'w', encoding="utf-8") as file:
    file = csv.writer(file)

    while True:
      batch = fetcher(repository_url, page)
      file.writerows(batch)

      fetched = fetched + len(batch)
      print('n=' + str(fetched), end='\r')

      if len(batch) < 1:
        break

      page = page + 1