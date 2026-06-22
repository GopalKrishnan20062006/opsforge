import re
import subprocess


def get_test_summary():
    try:
        result = subprocess.run(["pytest"], capture_output=True, text=True)

        output = result.stdout

        summary = {
            "status": "passed" if result.returncode == 0 else "failed",
            "total": 0,
            "passed": 0,
            "failed": 0,
        }

        match = re.search(r"(\d+)\s+passed", output)
        if match:
            summary["passed"] = int(match.group(1))

        match = re.search(r"(\d+)\s+failed", output)
        if match:
            summary["failed"] = int(match.group(1))

        summary["total"] = summary["passed"] + summary["failed"]

        return summary

    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_lint_summary():

    try:

        result = subprocess.run(["ruff", "check", "."], capture_output=True, text=True)

        return {
            "status": "passed" if result.returncode == 0 else "failed",
            "tool": "ruff",
        }

    except Exception as e:

        return {"status": "error", "error": str(e)}
