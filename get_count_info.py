import os
import pandas as pd

num_files = 0
write_file = open("data_counts.txt", "w", encoding="utf-8", errors='ignore')
processed_files = [f for f in os.listdir("processed/") if ".csv" in f]
for file in processed_files:
    with open(f"processed/{file}", "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if (line == "\n"):
                continue
            num_files += 1
#print(num_files)
write_file.write("NOTE: Duplicate commits/PRs are counted twice.\nThis is because there can be two files that are under the same commit/PR, and there two datapoints for the commit/PR, one for each file\n\n")
write_file.write(f"Number of files with PTM usage: {num_files}\n\n\n")


#print("\n\n\n")
num_commits = 0
commit_files = [f for f in os.listdir("commits/") if ".csv" in f]
commit_sent = ""
for file in commit_files:
    df = pd.read_csv(f"commits/{file}", index_col=False)
    #print(f"{file}: {len(df.index)}")
    commit_sent += f"{file}: {len(df.index)}\n"
    num_commits += len(df.index)
#print("\n\n\n")
write_file.write(f"Total Number of Commits: {num_commits}\n\n")
write_file.write(commit_sent)
write_file.write("\n\n\n")


num_prs = 0
pr_sent = ""
pr_files = [f for f in os.listdir("pull requests/") if ".csv" in f]
for file in pr_files:
    df = pd.read_csv(f"pull requests/{file}", index_col=False)
    #print(f"{file}: {len(df.index)}")
    pr_sent += f"{file}: {len(df.index)}\n"
    num_prs += len(df.index)
write_file.write(f"Total Number of PR Messages/Conversations: {num_prs}\n\n")
write_file.write(pr_sent)
