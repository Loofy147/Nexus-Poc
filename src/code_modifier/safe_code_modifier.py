import os
import black
import isort
import ast
from typing import Dict
import tempfile
from pylint import epylint as lint
import bandit.core.config
import bandit.core.manager
import bandit.core.constants
import git
from datetime import datetime

class GitManager:
    """Handles all Git operations for version control and auditing."""
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        try:
            self.repo = git.Repo(self.repo_path)
            print(f"Git Manager: Git repository initialized successfully at '{self.repo_path}'.")
        except git.InvalidGitRepositoryError:
            print(f"Git Manager: ERROR - Invalid Git repository at '{self.repo_path}'.")
            self.repo = None

    def create_and_checkout_branch(self, branch_name: str) -> bool:
        if not self.repo:
            return False
        try:
            # Create and checkout a new branch
            new_branch = self.repo.create_head(branch_name)
            new_branch.checkout()
            print(f"Git Manager: Created and checked out new branch '{branch_name}'.")
            return True
        except Exception as e:
            print(f"Git Manager: Failed to create branch '{branch_name}': {e}")
            return False

    def commit_changes(self, files: list, message: str) -> bool:
        if not self.repo:
            return False
        try:
            self.repo.index.add(files)
            self.repo.index.commit(message)
            print(f"Git Manager: Committed changes with message: '{message}'.")
            return True
        except Exception as e:
            print(f"Git Manager: Failed to commit changes: {e}")
            return False

class EnterpriseCodeModifier:
    """
    Production-grade code modifier with a multi-stage validation pipeline.
    This initial implementation focuses on the core pipeline structure
    and deterministic, safe code generation.
    """
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.src_path = "/app/src_code"
        repo_path = os.environ.get("GIT_REPO_PATH", "/app")
        self.git_manager = GitManager(repo_path=repo_path)
        print("Enterprise Code Modifier: Initialized.")

    def apply_modification(self, modification_request: Dict) -> Dict:
        """
        Main modification pipeline with enterprise guarantees.
        """
        print(f"Enterprise Code Modifier: Starting modification pipeline for service '{modification_request.get('service')}'.")

        # Phase 1: Validate Request
        if not self._validate_request(modification_request):
            return {"status": "FAILED", "reason": "Invalid request."}

        target_file = os.path.join(self.src_path, modification_request['service'], "app.py")

        # Phase 2: Generate Code Change (Simulated)
        code_change = self._generate_code_change(target_file, modification_request)
        if not code_change:
            return {"status": "FAILED", "reason": "Code generation failed."}

        # Phase 3 & 4: Security Scan & Quality Gate (Placeholders for next step)
        if not self._security_scan(code_change['modified']):
            return {"status": "FAILED", "reason": "Security scan failed."}

        if not self._quality_check(code_change['modified']):
            return {"status": "FAILED", "reason": "Quality gate failed."}

        # If all checks pass, commit the change to a new branch
        branch_name = f"feature/nexus-auto-mod-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        if not self.git_manager.create_and_checkout_branch(branch_name):
            return {"status": "FAILED", "reason": "Could not create Git branch."}

        try:
            with open(target_file, "w") as f:
                f.write(code_change['modified'])

            commit_message = f"feat(autonomous): Apply '{modification_request['type']}' to {modification_request['service']}\n\n{modification_request['description']}"
            if self.git_manager.commit_changes(files=[target_file], message=commit_message):
                print(f"Enterprise Code Modifier: Successfully committed modification to branch '{branch_name}'.")
                return {"status": "SUCCESS", "file": target_file, "branch": branch_name}
            else:
                return {"status": "FAILED", "reason": "Git commit failed."}

        except IOError as e:
            print(f"Enterprise Code Modifier: Failed to write modification to file: {e}")
            return {"status": "FAILED", "reason": f"File write error: {e}"}

    def _validate_request(self, request: Dict) -> bool:
        """Validates the incoming modification request."""
        required_keys = ["service", "type", "description"]
        if not all(key in request for key in required_keys):
            print(f"Enterprise Code Modifier: Validation failed. Missing keys. Request: {request}")
            return False
        print("Enterprise Code Modifier: Request validated successfully.")
        return True

    def _generate_code_change(self, target_file: str, request: Dict) -> Dict:
        """
        Generates a deterministic, safe code change based on the request.
        For this PoC, it adds a placeholder decorator to the main query handler.
        """
        print("Enterprise Code Modifier: Generating code change.")
        try:
            with open(target_file, "r") as f:
                original_code = f.read()
        except IOError as e:
            print(f"Enterprise Code Modifier: Could not read target file '{target_file}': {e}")
            return None

        # Use AST to safely find the function to modify
        tree = ast.parse(original_code)
        modified = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'query_handler':
                # Add a placeholder decorator
                node.decorator_list.insert(0, ast.Name(id='placeholder_cache_decorator', ctx=ast.Load()))
                modified = True
                break

        if not modified:
            print("Enterprise Code Modifier: Could not find target function 'query_handler' to modify.")
            return None

        # Add the placeholder decorator function definition at the top of the file
        decorator_code = "def placeholder_cache_decorator(f):\n    def wrapper(*args, **kwargs):\n        # TODO: Implement real caching logic\n        return f(*args, **kwargs)\n    return wrapper\n\n"

        modified_code_unformatted = decorator_code + ast.unparse(tree)

        # Format with black and isort
        formatted_code = black.format_str(modified_code_unformatted, mode=black.FileMode())
        formatted_code = isort.code(formatted_code)

        print("Enterprise Code Modifier: Code change generated and formatted.")
        return {
            "original": original_code,
            "modified": formatted_code,
            "file": target_file
        }

    def _security_scan(self, code: str) -> bool:
        """
        Performs a security scan using Bandit.
        Rejects code with MEDIUM or HIGH severity issues.
        """
        print("Enterprise Code Modifier: Running security scan with Bandit...")
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
                tmp_file.write(code)
                filepath = tmp_file.name

            b_config = bandit.core.config.BanditConfig()
            b_mgr = bandit.core.manager.BanditManager(b_config, "custom")
            b_mgr.discover_files([filepath])
            b_mgr.run_tests()

            os.remove(filepath)

            # Check for high or medium severity issues
            for issue in b_mgr.results:
                if issue.severity >= bandit.core.constants.MEDIUM:
                    print(f"Enterprise Code Modifier: SECURITY FAILED. Issue: {issue.text}, Severity: {issue.severity}, File: {issue.fname}")
                    return False

            print("Enterprise Code Modifier: Security scan passed.")
            return True
        except Exception as e:
            print(f"Enterprise Code Modifier: An error occurred during security scan: {e}")
            return False

    def _quality_check(self, code: str) -> bool:
        """
        Performs a quality check using Pylint.
        Rejects code with a score below a configured threshold.
        """
        print("Enterprise Code Modifier: Running quality check with Pylint...")
        quality_threshold = self.config.get("pylint_threshold", 8.0)

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
                tmp_file.write(code)
                filepath = tmp_file.name

            (pylint_stdout, pylint_stderr) = lint.py_run(f'{filepath} --output-format=text', return_std=True)

            os.remove(filepath)

            # Extract the score from the output
            output = pylint_stdout.getvalue()
            score_line = [line for line in output.split('\n') if "Your code has been rated at" in line]
            if not score_line:
                print("Enterprise Code Modifier: Could not parse Pylint score.")
                return False

            score = float(score_line[0].split(" at ")[1].split("/")[0])
            print(f"Enterprise Code Modifier: Pylint score is {score}/{10.0}. Threshold is {quality_threshold}.")

            if score < quality_threshold:
                print(f"Enterprise Code Modifier: QUALITY FAILED. Score {score} is below threshold {quality_threshold}.")
                return False

            print("Enterprise Code Modifier: Quality check passed.")
            return True
        except Exception as e:
            print(f"Enterprise Code Modifier: An error occurred during quality check: {e}")
            return False