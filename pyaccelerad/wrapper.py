"""
Utilities for executing Accelerad commands.
"""

import subprocess
import os
from .bin import get_binary_path


class AcceleradError(Exception):
    """Exception raised for errors in Accelerad command execution."""
    pass


def run_accelerad_command(binary_name, args=None, kwargs=None, input_data=None, stream_output=False):
    """Executes an Accelerad command.

    Args:
        binary_name (str): Name of the binary (e.g., 'accelerad_rpict').
        args (list): Positional arguments.
        kwargs (dict): Keyword arguments to be converted to flags.
        input_data (bytes or str): Data to pipe to stdin.
        stream_output (bool): If True, returns the process object instead of waiting.

    Returns:
        subprocess.CompletedProcess or subprocess.Popen: The result of the command.
    """
    cmd_path = get_binary_path(binary_name)
    if not cmd_path:
        # --- If not found, try running it directly assuming it's in PATH ---
        cmd_path = binary_name

    command = [cmd_path]

    # --- Process kwargs into flags ---
    if kwargs:
        for key, value in kwargs.items():
            # --- Handle boolean flags ---
            if isinstance(value, bool):
                if value:
                    command.append(f"-{key}")
            else:
                command.append(f"-{key}")
                command.append(str(value))

    # --- Add positional arguments ---
    if args:
        command.extend([str(arg) for arg in args])

    # --- Prepare environment ---
    env = os.environ.copy()

    # --- Run command ---
    try:
        if stream_output:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE if input_data else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=False  # --- Keep as bytes for binary data ---
            )
            if input_data:
                if isinstance(input_data, str):
                    input_data = input_data.encode('utf-8')
                process.stdin.write(input_data)
                process.stdin.close()
            return process
        else:
            input_bytes = None
            if input_data:
                if isinstance(input_data, str):
                    input_bytes = input_data.encode('utf-8')
                else:
                    input_bytes = input_data

            result = subprocess.run(
                command,
                input=input_bytes,
                capture_output=True,
                env=env
            )

            if result.returncode != 0:
                raise AcceleradError(f"Command '{binary_name}' failed with error: {result.stderr.decode('utf-8', errors='replace')}")

            return result.stdout

    except FileNotFoundError:
        raise AcceleradError(f"Binary '{binary_name}' not found. Please ensure Accelerad is installed and in your PATH or configured correctly.")
