from dotenv import load_dotenv
from lib.github import fetch_tags, fetch_data
import sys

"""
Fetches tags from Github and outputs to output.csv.
"""
def main(repository_url: str) -> None:
  fetch_data(repository_url, fetch_tags)

if __name__ == '__main__':
  load_dotenv()

  if len(sys.argv) < 2:
    print('Please provide a repository URL as first argument.')
    exit(1)

  repository_url = sys.argv[1]
  main(repository_url)