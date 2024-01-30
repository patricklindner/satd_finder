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
    name = path.split("/")[-1].split(".")[0].split("_")[0]

    DEF_LABELS = ['code|design-debt', 'requirement-debt', 'documentation-debt', 'test-debt']

    df = pd.read_csv(path, names=["mode", "ts", "commit_hash", "comment", "comment_type", "classification"])

    df = df.sort_values(by=["ts"], ascending=True)
    df = df.reset_index(drop=True)

    timestamps = df["ts"].unique()

    with open(f"../data/aggregated/{name}_aggregated.csv", mode="w") as result_file:
        writer = csv.writer(result_file)
        writer.writerow(["timestamp", *DEF_LABELS])
        for timestamp in timestamps:
            # for every unique timestamp find all comments
            comments_from_ts: DataFrame = df.loc[df['ts'] == timestamp]
            counter = [0, 0, 0, 0]
            for idx, comment in comments_from_ts.iterrows():
                for index, label in enumerate(DEF_LABELS):
                    # count either up or down the respective SATD counter value
                    if comment["classification"] == label:
                        if comment["mode"] == "INSERT":
                            counter[index] = counter[index] + 1
                            break
                        elif comment["mode"] == "DELETE":
                            counter[index] = counter[index] - 1
                            break
                        else:
                            exit("Unknown mode")

            writer.writerow([timestamp, *counter])
