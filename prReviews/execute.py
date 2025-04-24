import os
import requests
from services.config import BITBUCKET_REPO_OWNER, BITBUCKET_REPO_SLUG, PR_ID, BITBUCKET_USERNAME, BITBUCKET_PASSWORD
from services.bitbucket_api import get_basic_auth_header, fetch_pr_info, fetch_pr_diff, post_pr_comment
from services.gemini_api import analyze_code_with_gemini
from services.diff_analysis import get_code_difference, format_diff_for_gemini

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