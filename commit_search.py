import subprocess
import satd_detector

repo_path = '../fordon'

class Commit:

    def __init__(self, summary):
        self.hash = hash
        self.summary = summary

def fetch_commits():
    result = subprocess.run(["git", "-C", repo_path, "log", "--pretty=format:%s"], stdout=subprocess.PIPE)
    commit_lines = result.stdout.decode("UTF-8").split("\n")
    commits = list()

    for line in commit_lines:
        result_array = line.split(",")
        commits.append(Commit(result_array[0]))

    return commits

def main():
    commits = fetch_commits()
    detector = satd_detector.get_instance()

    for commit in commits:
        detector.classify_prob_comment(commit.summary, tp=satd_detector.DEF_COMMIT)

if __name__ == '__main__':
    main()