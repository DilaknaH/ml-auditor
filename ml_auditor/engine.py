import nbformat
import os
from ml_auditor.checkers import check_leakage, check_reproducibility, check_metrics
from ml_auditor.llm.explainer import get_explanation

class AuditorEngine:
    def __init__(self, file_path):
        self.file_path = file_path
        self.code_content = self._read_file()
        self.lines = self.code_content.split('\n')

    def _read_file(self):
        """Reads .ipynb or .py files."""
        try:
            if self.file_path.endswith('.ipynb'):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    nb = nbformat.read(f, as_version=4)
                code_cells = [cell.source for cell in nb.cells if cell.cell_type == 'code']
                return "\n\n".join(code_cells)
            
            elif self.file_path.endswith('.py'):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            else:
                return "Error: Unsupported file format."
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def calculate_score(self, issues):
        score = 100
        for issue in issues:
            sev = issue.get('severity', 'Low')
            if sev == 'Critical': score -= 30
            elif sev == 'High': score -= 20
            elif sev == 'Medium': score -= 10
            else: score -= 5
        return max(0, score)

    def get_code_snippet(self, line_number, context=3):
        start = max(0, line_number - 1 - context)
        end = min(len(self.lines), line_number - 1 + context + 1)
        return "\n".join(self.lines[start:end])

    def run_audit(self, api_key=None):
        if "Error" in self.code_content:
            return {"score": 0, "issues": [{"type": "File Error", "message": self.code_content}], "raw_code": ""}

        issues = []
        
        # Run Checkers
        issues.extend(check_leakage(self.code_content))
        issues.extend(check_reproducibility(self.code_content))
        issues.extend(check_metrics(self.code_content))

        score = self.calculate_score(issues)

        # Enhance with LLM if key provided
        if api_key:
            for issue in issues:
                line_no = issue.get('line', 1)
                snippet = self.get_code_snippet(line_no)
                issue['snippet'] = snippet
                
                # Call GPT
                explanation, fixed_code = get_explanation(issue, snippet, api_key)
                issue['llm_explanation'] = explanation
                issue['fixed_code'] = fixed_code
        
        return {
            "score": score,
            "issues": issues,
            "file_name": os.path.basename(self.file_path),
            "raw_code": self.code_content
        }
    