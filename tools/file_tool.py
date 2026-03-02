import os

OUTPUT_DIR = "./output"


def write_file(filename: str, content: str) -> str:
    """
    Write text content to a file inside the safe output directory.

    Args:
        filename: Name of the file (e.g. 'result.txt'). No path separators allowed.
        content: Text content to write.

    Returns:
        Confirmation message with the saved file path.
    """
    # Sanitize: strip any directory components from filename
    safe_name = os.path.basename(filename)
    if not safe_name:
        return "ERROR: Invalid filename provided."

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, safe_name)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File saved successfully: {filepath}"
    except Exception as e:
        return f"ERROR: Could not write file — {str(e)}"