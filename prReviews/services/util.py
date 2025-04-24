class CodeUtils:
    @staticmethod
    def extract_code_from_diff(diff_content, file_path):
        lines = diff_content.splitlines()
        code_lines = []
        in_code_block = False
        for line in lines:
            if line.startswith("+++ b/" + file_path):
                in_code_block = True
                continue
            if in_code_block and line.startswith("+") and not line.startswith("+++"):
                code_lines.append(line[1:])  # Remove the "+" prefix
        return "\n".join(code_lines)
