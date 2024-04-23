import os
import requests
import json
import pandas as pd

API_OK = 0
API_ERROR = 1

GITHUB_TOKEN = #your Github token

def get_commits_associated_with_repo_file(owner: str, repo: str, filepath: str):
    try:
        url = f'https://api.github.com/repos/{owner}/{repo}/commits'
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}
        params = {'path': filepath, 'per_page': 100}
        r = requests.get(url, params=params, headers=headers)
    except:
        print(f'Error getting commits for {owner}/{repo}/{filepath}')
        return [], API_ERROR
    return r.json(), API_OK

#df = pd.DataFrame(columns={'2_repo_url','1_file_path','0_commit_date','3_commit_message'})

files_to_check = [f for f in os.listdir("processed/") if ".csv" in f]

files_to_check = files_to_check[26:]
for file in files_to_check:
    print(file)
    df = pd.DataFrame(columns={'2_repo_url','1_file_path','0_commit_date','3_commit_message'})
    with open(f"processed/{file}", "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            split_up = line.split("/")
            owner = split_up[1]
            repo = split_up[2]
            filepath = "/".join(split_up[3:])
            filepath = filepath[0:-1]
            commits, API_ERROR = get_commits_associated_with_repo_file(owner, repo, filepath)
            if (len(commits) > 0):
                for commit in commits:
                    try:
                        commit_info = commit["commit"]
                        commit_date = commit_info["committer"]["date"]
                        message = commit_info["message"]
                        repo_url = "/".join(split_up[0:3])
                        df.loc[len(df.index)] = [repo_url, filepath, commit_date, message]
                    except:
                        print(json.dumps(commit))
                        continue
    df.columns = ['repo_url', 'filepath', 'commit_date', 'message']
    fname = file.replace(".csv", "")
    df.to_csv(f"commits/{fname}_commits.csv", index=False)

