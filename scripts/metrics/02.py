from dotenv import load_dotenv
import sys

"""
Resolved issues / total issues ratio.

[x] Function that retrieves all issues for a single repository.
[ ] Function Function that counts the number of resolved issues / total issues per day
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