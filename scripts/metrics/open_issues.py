from dotenv import load_dotenv
import pandas as pd
import sys
import datetime
import dateutil.parser as dp
import csv

"""
Number of open issues.

[x] Function that retrieves all issues for a single repository.
[ ] Function that counts the number of open issues per day
"""
def main(file_path: str) -> None:
  pass
  

def extractData(file_path: str) -> None:
  name = file_path.split('/')[-1].split('.')[0]
  df = pd.read_csv(file_path, names=['id', 'title', 'contents', 'state', 'created_at', 'closed_at', 'something', 'pull_request'])

  df_opened = df.copy()
  df_closed = df.copy()

  df_opened = df_opened.sort_values(by=['created_at'], ascending=True)
  df_closed = df_closed.sort_values(by=['closed_at'], ascending=True, na_position='last')

  opened_timestamps = list(map(datetimeToTimestamp, df_opened['created_at'].tolist()))
  closed_timestamps = list(map(datetimeToTimestamp, df_closed['closed_at'].tolist()))

  i = 0
  j = 0

  issue_counter = 0

  with open(f"data/aggregated_issues/{name}_aggregated.csv", mode="w", encoding="utf-8") as result_file:
    writer = csv.writer(result_file)
    writer.writerow(["date", "open_issues"])
    while (i < len(opened_timestamps)) and (j < len(closed_timestamps)):
      if opened_timestamps[i] <= closed_timestamps[j]:
        issue_counter += 1
        writer.writerow([opened_timestamps[i], issue_counter])
        i += 1
      elif (opened_timestamps[i] > closed_timestamps[j]) and closed_timestamps[j] >= 0:
        issue_counter -= 1
        writer.writerow([closed_timestamps[j], issue_counter])
        j += 1
      else:
        j += 1

def datetimeToTimestamp(date_time: str) -> float:
  if isinstance(date_time, str):
    parsed_dt = dp.parse(date_time)
    return parsed_dt.timestamp()
  return -1

if __name__ == '__main__':
  load_dotenv()

  if len(sys.argv) < 2:
    print('Please provide an input file as first argument.')
    exit(1)

  file_path = sys.argv[1]
  main(file_path)