import os
import requests
import pandas as pd

API_OK = 0
API_ERROR = 1

GITHUB_TOKEN =

def get_commits_associated_with_repo_file(owner, repo, filepath):
    try:
        url = f'https://api.github.com/repos/{owner}/{repo}/commits'
        params = {'path': filepath, 'per_page': 100}
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        commits = response.json()
        if isinstance(commits, list):
            return [commit['sha'] for commit in commits if isinstance(commit, dict)], API_OK
        else:
            return [], API_ERROR
    except requests.RequestException as e:
        print(f'Error: {e}')
        return [], API_ERROR

def is_there_a_pr_associated_with_a_commit(owner, repo, commit_sha):
    try:
        url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/pulls'
        headers = {'Authorization': f'token {GITHUB_TOKEN}', 'Accept': 'application/vnd.github.groot-preview+json'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return len(response.json()) > 0, API_OK
    except requests.RequestException as e:
        print(f'Error: {e}')
        return False, API_ERROR

def get_remaining_api_requests():
    try:
        url = 'https://api.github.com/rate_limit'
        response = requests.get(url)
        response.raise_for_status()
        return int(response.headers['X-RateLimit-Remaining'])
    except requests.RequestException as e:
        print(f'Error: {e}')
        return 0

def main():
    csv = pd.read_csv('merged.csv')
    csv.drop_duplicates(inplace=True)
    headers = list(csv)


    print("Remaining API Requests:", get_remaining_api_requests())

    for index, row in csv.iterrows():
        gh_url = row[headers[0]]
        # print("Iter:",  index)
        # Assuming the URL is of the format 'github.com/owner/repo'
        split_url = gh_url.split('/')
        if len(split_url) < 3:
            print(f"Invalid URL format at index {index}: {gh_url}")
            continue
        owner = split_url[-2]
        repo = split_url[-1]
        filepath = row[headers[1]]

        # Commits for a file
        commits, api_result = get_commits_associated_with_repo_file(owner, repo, filepath)

        # Check to see if we are out of API requests
        if api_result == API_ERROR:
            if get_remaining_api_requests() == 0:
                print('No more API requests left')
                print(f"On record index {index}")
                break

        pr_found = False
        for commit_sha in commits:
            there_is_a_pr, api_result = is_there_a_pr_associated_with_a_commit(owner, repo, commit_sha)
            if there_is_a_pr:
                # print("PR found:", index)
                pr_found = True
                break

            if api_result == API_ERROR and get_remaining_api_requests() == 0:
                print('No more API requests left')
                print(f"On record index {index}")
                break

        # Filter the record if there is no PR associated with the file
        if not pr_found:
            csv.drop(index, inplace=True)


    csv.to_csv('filtered.csv', index=False)

if __name__ == "__main__":
    main()
