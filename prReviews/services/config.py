import os

from dotenv import load_dotenv

load_dotenv()
# BITBUCKET_API_BASE_URL = "https://api.bitbucket.org/2.0"
# BITBUCKET_USERNAME = os.environ.get("BITBUCKET_USERNAME")
# BITBUCKET_PASSWORD = os.environ.get("BITBUCKET_PASSWORD")
# BITBUCKET_REPO_OWNER = ""
# BITBUCKET_REPO_SLUG = ""
# PR_ID = ""  # You'll need to get this dynamically
#
# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# GEMINI_MODEL_NAME = ""
BITBUCKET_API_BASE_URL = os.environ.get("BITBUCKET_API_BASE_URL", "https://api.bitbucket.org/2.0")
BITBUCKET_USERNAME = os.environ.get("BITBUCKET_USERNAME")
BITBUCKET_PASSWORD = os.environ.get("BITBUCKET_PASSWORD")
BITBUCKET_REPO_OWNER = os.environ.get("BITBUCKET_REPO_OWNER", "comapny id")
BITBUCKET_REPO_SLUG = os.environ.get("BITBUCKET_REPO_SLUG", "repo id")
PR_ID = os.environ.get("PR_ID", "pr id")  # You'll need to get this dynamically

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "model name")