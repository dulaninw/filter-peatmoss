import os
import requests
import json
import pandas as pd

API_OK = 0
API_ERROR = 1

GITHUB_TOKEN = "0";#Github TOKEN HERE

def get_commit_shas(owner:str, repo:str, filepath:str):
    try:
        url = f'https://api.github.com/repos/{owner}/{repo}/commits'
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}
        params = {'path': filepath, 'per_page': 100}
        r = requests.get(url, params=params, headers=headers)
    except:
        print(f'Error getting commits for {owner}/{repo}/{filepath}')
        return [], API_ERROR
    
    if (isinstance(r.json(), list)):
        return [commit['sha'] for commit in r.json() if isinstance(commit, dict)], API_OK;
    else:
        return [], API_ERROR



def get_prs_for_commit(owner:str, repo:str, commit_sha:str):
    try:
        url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/pulls'
        headers = {'Authorization': f'token {GITHUB_TOKEN}', 'Accept': 'application/vnd.github.groot-preview+json'}
        params = {'per_page': 100}
        response = requests.get(url, headers=headers)
        return response.json(), API_OK
    except:
        print(f"Error getting PRs for {owner}/{repo}/commits/{commit_sha}")
        return [], API_ERROR        


        
def get_pr_review_comments(owner:str, repo:str, pr_number:str):
    try:
        url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/comments'
        headers = {'Authorization': f'token {GITHUB_TOKEN}', 'Accept': 'application/vnd.github+json'}
        params = {'per_page': 100}
        response = requests.get(url, params=params, headers=headers)
        return response.json(), API_OK
    except:
        print(f"Error getting PR review comments for {owner}/{repo}/pulls/{pr_number}")
        return [], API_ERROR
    
def get_issue_comments(owner:str, repo:str, issue_number:str):
    try:
        url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments'
        headers = {'Authorization': f'token {GITHUB_TOKEN}', 'Accept': 'application/vnd.github+json'}
        params = {'per_page': 100}
        response = requests.get(url, params=params, headers=headers)
        return response.json(), API_OK
    except:
        print(f"Error getting issue review comments for {owner}/{repo}/pulls/{issue_number}")
        return [], API_ERROR
    
    
def main():        
    files_to_check = [f for f in os.listdir("processed/") if ".csv" in f]
    files_to_check = files_to_check[27:]
    for file in files_to_check:
        print(file)
        df = pd.DataFrame(columns={'2_repo_url','1_file_path','0_creation_date','3_pr_comment', '4_pull/issue_num'})
        with open(f"processed/{file}", "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                split_up = line.split("/")
                owner = split_up[1]
                repo = split_up[2]
                filepath = "/".join(split_up[3:])
                filepath = filepath[0:-1]
                commit_shas, api_result = get_commit_shas(owner, repo, filepath)
                repo_url = "/".join(split_up[0:3])
                if (len(commit_shas) > 0):
                    pr_numbers = []
                    for commit_sha in commit_shas:
                        prs, api_result = get_prs_for_commit(owner, repo, commit_sha)
                        if (len(prs) > 0):
                            try:
                                for pr in prs:
                                    url = pr['url']
                                    url_split = url.split("/")
                                    pr_num = url_split[len(url_split)-1]
                                    pr_numbers.append(pr_num)
                            except:
                                    print(json.dumps(pr))
                                    continue
                    for pr_num in pr_numbers:
                        #print(pr_num)
                        pr_review_comments = get_pr_review_comments(owner, repo, pr_num)
                        if pr_review_comments[0] != []:
                            for review in pr_review_comments[0]:
                                try:
                                    df.loc[len(df.index)] = [repo_url, filepath, review['created_at'], review['body'], pr_num]
                                except:
                                    print(review) 
                        issue_comments = get_issue_comments(owner, repo, pr_num)
                        if issue_comments[0] != []:
                            for issue in issue_comments[0]:
                                try:
                                    df.loc[len(df.index)] = [repo_url, filepath, issue['created_at'], issue['body'], pr_num]
                                except:
                                    print(issue)
        df.columns = ['repo_url', 'filepath', 'Creation Date', 'PR Comment', 'PR/Issue Number']
        fname = file.replace(".csv", "")
        df.to_csv(f"pull requests/{fname}_prs.csv", index=False)
    
if __name__ == "__main__":
    main()