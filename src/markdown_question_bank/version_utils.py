import os
import subprocess
from markdown_question_bank import __version__

def get_version_and_commit(project_root=None):
    """
    Returns (version, commit_id) from __version__ and git, or ("unknown", "unknown") if not found.
    """
    version = getattr(__import__('markdown_question_bank'), '__version__', 'unknown')
    commit = "unknown"

    if project_root is None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    try:
        commit = subprocess.check_output([
            "git", "rev-parse", "--short", "HEAD"
        ], cwd=project_root, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        print("Warning: Could not determine git commit. Using 'unknown'.")
    return version, commit

def write_version_file(outdir, version, commit):
    with open(os.path.join(outdir, "VERSION.txt"), "w") as f:
        f.write(f"question-bank version: {version}\n")
        f.write(f"git commit: {commit}\n")
