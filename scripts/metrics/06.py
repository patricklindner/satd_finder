from dotenv import load_dotenv
import sys

"""
Review to merge time.

[x] Function that retrieves all pull requests for a single repository.
[ ] Function that calculates the time between open pull-request and merge
[ ] Function that calculates the running average for review to merge time based on 30 days
"""
def main(file_path: str) -> None:
  pass

if __name__ == '__main__':
  load_dotenv()

  if len(sys.argv) < 2:
    print('Please provide an input file as first argument.')
    exit(1)

  file_path = sys.argv[1]
  main(file_path)