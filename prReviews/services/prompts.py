CODE_REVIEW_PROMPT = """Please review the following code changes in this pull request. Focus on identifying potential:

-go to each file and check line by line and comment
- Business logic errors or inconsistencies.
- Potential bugs, including edge cases and error handling.
- Code smells that might indicate maintainability issues or areas for simplification.
- Security vulnerabilities (if applicable to the code context).
- Areas where the code could be more readable and understandable.

Provide specific feedback and suggestions for improvement, referencing the lines of code where necessary..

```diff
{diff_text}
```"""
