import os
import pandas as pd
import requests

API_OK = 0
API_ERROR = 1

GITHUB_TOKEN = 

def get_commits_associated_with_repo_file(owner: str, repo: str, filepath: str):
    try:
        url = f'https://api.github.com/repos/{owner}/{repo}/commits'
        params = {'path': filepath, 'per_page': 100}
        r = requests.get(url, params=params)
    except:
        print(f'Error getting commits for {owner}/{repo}/{filepath}')
        return [], API_ERROR
    return r.json(), API_OK

def is_there_a_pr_associated_with_a_list_of_commits(owner: str, repo: str, commits: list):
    try:
        for commit in commits:
            url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit}/pulls'
            r = requests.get(url)
            if len(r.json()) > 0:
                return True, API_OK
    except:
        print(f'Error getting PRs for {owner}/{repo}/{commit}')
        return False, API_ERROR
    return False, API_OK

def get_remaining_api_requests():
    url = f'https://api.github.com/rate_limit'
    r = requests.get(url)
    return int(r.headers['X-RateLimit-Remaining'])

csv : pd.DataFrame  = pd.read_csv('merged.csv')
csv = csv.drop_duplicates()
headers = list(csv)
print(get_remaining_api_requests())
for index, row in csv.iterrows():

    # Get relevant data from row
    gh_url = row[headers[0]]
    owner = gh_url.split('/')[1]
    repo = gh_url.split('/')[2]
    filepath = row[headers[1]]

    # Commits for a file
    commits, api_result = get_commits_associated_with_repo_file(owner, repo, filepath)

    # Check to see if we are out of API requests
    if API_ERROR == api_result:
        if get_remaining_api_requests() == 0:
            print('No more API requests left')
            print(f"On record index {index}")
            break

    # Convert commits to list of sha's
    commit_list = [commit['sha'] for commit in commits]

    # Check to see if there is a PR associated with any of the commits related to the file
    there_is_a_pr, api_result = is_there_a_pr_associated_with_a_list_of_commits(owner, repo, commit_list)
    if API_ERROR == api_result:
        if get_remaining_api_requests() == 0:
            print('No more API requests left')
            print(f"On record index {index}")
            break
    
    # Filter the record if there is no PR associated with the file
    if there_is_a_pr is False:
        csv = csv.drop(index)

csv.to_csv('filtered.csv', index=False)

