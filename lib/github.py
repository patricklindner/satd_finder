import os
import csv
import requests
import re
from lib.models import Commit, Tag, Issue

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