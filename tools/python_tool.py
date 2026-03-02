import subprocess
import sys

def run_python(code: str, timeout: int = 10) -> str:
    """
    Execute Python code in a subprocess and return its output.

    Args:
        code: Python source code string to execute.
        timeout: Maximum seconds to allow execution (default: 10).

    Returns:
        Combined stdout + stderr as a single string.
    """

    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.strip()
        errors = result.stderr.strip()

        if output and errors:
            return f"OUTPUT:\n{output}\n\nSTDERR:\n{errors}"
        elif output:
            return output
        elif errors:
            return f"STDERR:\n{errors}"
        else:
            return "(No output produced)"

    except subprocess.TimeoutExpired:
        return f"ERROR: Code execution timed out after {timeout} seconds."
    except Exception as e:
        return f"ERROR: Failed to execute code — {str(e)}"
