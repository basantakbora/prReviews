import requests
import base64
from services.config import BITBUCKET_API_BASE_URL


def get_basic_auth_header(username, password):
    auth_string = f"{username}:{password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    return {"Authorization": f"Basic {encoded_auth}"}


def fetch_pr_info(repo_owner, repo_slug, pr_id, auth_header):
    url = f"{BITBUCKET_API_BASE_URL}/repositories/{repo_owner}/{repo_slug}/pullrequests/{pr_id}"
    response = requests.get(url, headers=auth_header)
    response.raise_for_status()
    return response.json()


def fetch_pr_diff(repo_owner, repo_slug, pr_id, auth_header):
    url = f"{BITBUCKET_API_BASE_URL}/repositories/{repo_owner}/{repo_slug}/pullrequests/{pr_id}/diff"
    response = requests.get(url, headers=auth_header)
    response.raise_for_status()
    return response.text


def post_pr_comment(repo_owner, repo_slug, pr_id, auth_header, content):
    url = f"{BITBUCKET_API_BASE_URL}/repositories/{repo_owner}/{repo_slug}/pullrequests/{pr_id}/comments"
    headers = auth_header
    headers["Content-Type"] = "application/json"
    payload = {"content": {"raw": content}}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
