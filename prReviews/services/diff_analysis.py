from diff_match_patch import diff_match_patch

def get_code_difference(diff_text):
    dmp = diff_match_patch()
    patches = dmp.patch_fromText(diff_text)
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