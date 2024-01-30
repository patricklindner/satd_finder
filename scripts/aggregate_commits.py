import pandas as pd
import sys
import csv

from pandas import DataFrame

if __name__ == '__main__':
    """
    This script, counts all SATD from the comments input file. Therefore, it counts one up for an inserted comment, 
    and one down for a deleted one for the respective type of SATD.
    :param sys.argv[1]: location of the comments input file
    """

    path = sys.argv[1]
    name = path.split("/")[-1].split(".")[0]

    df = pd.read_csv(path, names=["commit_hash", "description", "date"])

    df = df.sort_values(by=["date"], ascending=True)
    df = df.reset_index(drop=True)

    timestamps = df["date"].unique()

    with open(f"data/aggregated_commits/{name}_aggregated.csv", mode="w") as result_file:
        writer = csv.writer(result_file)
        writer.writerow(["date", "number_commits"])
        for timestamp in timestamps:
            # for every unique timestamp find all commits
            commits_from_ts: DataFrame = df.loc[df['date'] == timestamp]

            writer.writerow([timestamp, len(commits_from_ts)])
