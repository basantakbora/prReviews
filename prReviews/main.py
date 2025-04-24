import base64
import os
import subprocess

import requests
import google.generativeai as genai
from google.generativeai import GenerativeModel
from diff_match_patch import diff_match_patch

# --- Configuration ---
BITBUCKET_API_BASE_URL = "https://api.bitbucket.org/2.0"
BITBUCKET_USERNAME = ""
BITBUCKET_PASSWORD = ""
BITBUCKET_REPO_OWNER = "company id"
BITBUCKET_REPO_SLUG = "repo name"
PR_ID = "pr id"  # You'll need to get this dynamically

GEMINI_API_KEY = ""
GEMINI_MODEL_NAME = "gemini model"


# --- Authentication ---
def get_basic_auth_header(username, password):
    auth_string = f"{username}:{password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    return {"Authorization": f"Basic {encoded_auth}"}


# --- Bitbucket API Interactions ---
def fetch_pr_info(repo_owner, repo_slug, pr_id, auth_header):
    url = f"{BITBUCKET_API_BASE_URL}/repositories/{repo_owner}/{repo_slug}/pullrequests/{pr_id}"
    response = requests.get(url, headers=auth_header)
    response.raise_for_status()  # Raise an exception for bad status codes
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


# --- Code Difference Analysis ---
def get_code_difference(diff_text):
    dmp = diff_match_patch()
    patches = dmp.patch_fromText(diff_text)
    # We are interested in the changes themselves, not the context lines
    diffs = []
    for patch in patches:
        diffs.extend(patch.diffs)
    return diffs


def format_diff_for_gemini(diffs):
    formatted_diff = ""
    for operation, text in diffs:
        if operation == 1:  # Insertion
            formatted_diff += f"Added: {text}\n"
        elif operation == -1:  # Deletion
            formatted_diff += f"Removed: {text}\n"
    return formatted_diff


# --- Gemini API Interaction ---
def analyze_code_with_gemini(diff_text):
    if not GEMINI_API_KEY:
        raise EnvironmentError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    prompt = f"""Please review the following code changes for business logic issues, potential bugs, and code smells. Provide specific feedback and suggestions for improvement.

```diff
{diff_text}
```"""
    response = model.generate_content(prompt)
    return response.text


# --- Main Workflow ---
if __name__ == "__main__":
    # Ensure necessary environment variables are set
    if not BITBUCKET_USERNAME or not BITBUCKET_PASSWORD:
        raise EnvironmentError("BITBUCKET_USERNAME and BITBUCKET_PASSWORD environment variables must be set.")

    auth_header = get_basic_auth_header(BITBUCKET_USERNAME, BITBUCKET_PASSWORD)

    try:
        print("Fetching pull request information...")
        pr_info = fetch_pr_info(BITBUCKET_REPO_OWNER, BITBUCKET_REPO_SLUG, PR_ID, auth_header)
        print(f"Pull Request Title: {pr_info['title']}")
        print("Fetching pull request diff...")
        diff_text = fetch_pr_diff(BITBUCKET_REPO_OWNER, BITBUCKET_REPO_SLUG, PR_ID, auth_header)
        if not diff_text.strip():
            print("No code changes found in this pull request.")
        else:
            print("Analyzing code changes with Gemini...")
            gemini_analysis = analyze_code_with_gemini(diff_text)
            print("\nGemini Analysis:")
            print(gemini_analysis)

            if gemini_analysis.strip():
                print("\nPosting Gemini's feedback as a comment on the pull request...")
                post_pr_comment(BITBUCKET_REPO_OWNER, BITBUCKET_REPO_SLUG, PR_ID, auth_header, gemini_analysis)
                print("Comment posted successfully.")
            else:
                print("Gemini did not find any issues or suggestions.")

    except requests.exceptions.RequestException as e:
        print(f"Error during Bitbucket API interaction: {e}")
    except EnvironmentError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
