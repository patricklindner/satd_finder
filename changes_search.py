import subprocess

repo_path = "../../IdeaProjects/testMine"
file_name = "one.txt"


class Commit:

    def __init__(self, hash, author, timestamp):
        self.hash = hash
        self.author = author
        self.timestamp = timestamp


def obtain_commits(file_name: str):
    result = subprocess.run(["git", "-C", repo_path, "log", "--pretty=format:%H,%an,%ad", "--", file_name], stdout=subprocess.PIPE)
    commit_lines = result.stdout.decode("UTF-8").split("\n")
    commits = list()

    for line in commit_lines:
        result_array = line.split(",")
        commits.append(Commit(result_array[0], result_array[1], result_array[2]))

    return commits


def obtain_changes_with_diff_filter(modifier: str, commit_hash: str, file_name: str):
    result = subprocess.run(["git", "-C", repo_path, "diff", f"--diff-filter={modifier}", commit_hash, "--", file_name], stdout=subprocess.PIPE)
    print(result.stdout.decode("UTF-8"))


def obtain_satds(commit: Commit, file_name: str):
    obtain_changes_with_diff_filter("M", commit.hash, file_name)


for commit in obtain_commits(file_name):
    print(f"checking {commit.hash} at {commit.timestamp}")
    obtain_satds(commit, file_name)

