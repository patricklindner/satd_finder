from dotenv import load_dotenv
from collections import defaultdict
import csv
from datetime import datetime
from lib.models import Commit
import sys

"""
Calculate the commit frequency.
"""
def main(file_path: str) -> None:
  frequency = defaultdict(int)

  with open(file_path, 'r') as file:
    reader = csv.reader(file)

    # Iterate over the rows within the CSV file.
    for row in reader:
      commit = Commit(*row)
      date = datetime.strptime(commit.date, '%Y-%m-%dT%H:%M:%S%z').date()

      frequency[date] += 1

  with open('output.csv', 'w') as file:
    file = csv.writer(file)

    for date, numberOfCommits in sorted(frequency.items()):
      file.writerow([date, numberOfCommits])

if __name__ == '__main__':
  load_dotenv()

  if len(sys.argv) < 2:
    print('Please provide an input file as first argument.')
    exit(1)

  file_path = sys.argv[1]
  main(file_path)