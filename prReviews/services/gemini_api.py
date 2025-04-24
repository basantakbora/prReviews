import google.generativeai as genai
from services.config import GEMINI_API_KEY, GEMINI_MODEL_NAME
from services.prompts import CODE_REVIEW_PROMPT

def analyze_code_with_gemini(diff_text):
    if not GEMINI_API_KEY:
        raise EnvironmentError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    prompt = CODE_REVIEW_PROMPT.format(diff_text=diff_text)
    response = model.generate_content(prompt)
    return response.text