"""
Utilities for locating Accelerad binaries on the system.
"""

import os
import shutil
import sys

# --- Default install location on Windows ---
DEFAULT_ACCELERAD_PATH = r"C:\Program Files\Accelerad\bin"


def get_accelerad_bin_path():
    """Return the path to the Accelerad binaries.

    Checks ACCELERAD_BIN environment variable first, then the default install
    location, then the system PATH.

    Returns:
        str or None: The path to the Accelerad binaries directory, or None if not found.
    """
    # --- Check environment variable ---
    env_path = os.environ.get("ACCELERAD_BIN")
    if env_path and os.path.exists(env_path):
        return env_path

    # --- Check default location ---
    if os.path.exists(DEFAULT_ACCELERAD_PATH):
        return DEFAULT_ACCELERAD_PATH

    # --- Check PATH (return None if not found) ---
    # We'll return None to indicate we couldn't find a specific directory,
    # but we can still try to run the command if it's in PATH.
    return None


def get_binary_path(binary_name):
    """Return the full path to a binary.

    Args:
        binary_name (str): The name of the binary to find.

    Returns:
        str or None: The full path to the binary, or None if not found.
    """
    bin_dir = get_accelerad_bin_path()

    if bin_dir:
        # --- If we found a directory, look for the binary there ---
        full_path = os.path.join(bin_dir, binary_name)

        # --- Check exact match first (e.g. script or already has extension) ---
        if os.path.exists(full_path):
            return full_path

        # --- Check with .exe extension on Windows ---
        if sys.platform == "win32":
            if os.path.exists(full_path + ".exe"):
                return full_path + ".exe"
            # --- Also check for .pl or .bat if needed, but let's stick to exe for now ---
            # or rely on shutil.which if not found here.

    # --- Fallback to shutil.which to find in PATH ---
    return shutil.which(binary_name)
