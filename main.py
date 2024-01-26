import dotenv
import csv
import sys
from github import  fetch_tags

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