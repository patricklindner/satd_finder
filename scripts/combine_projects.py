import os

import pandas as pd
from pandas import DataFrame

def combine_datasets(base_dir, output_file, get_name):
    combined = DataFrame()
    for file in os.listdir(base_dir):
        name = get_name(file)
        df = pd.read_csv(base_dir+file)
        df.insert(0, "project", name)
        combined = pd.concat([combined, df])
    combined = combined.set_index("timestamp")
    print(combined)
    combined.to_csv(output_file)


combine_datasets("data/aggregated_satd/", "data/satds.csv", lambda file: file.split("/")[-1].split(".")[0].split("_")[0])
combine_datasets("data/releases/", "data/releases.csv", lambda file: file.split("/")[-1].split(".")[0].split("-")[0])
combine_datasets("data/commits_local_repo/", "data/commits.csv", lambda file: file.split("/")[-1].split(".")[0])




