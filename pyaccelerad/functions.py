"""
Core functions for calling Accelerad binaries with Pyradiance-compatible signatures.
"""

import os
import pathlib
import subprocess
from typing import Sequence, Optional, Union
from .bin import get_binary_path
from .wrapper import run_accelerad_command

# --- Try to import pyradiance for fallback ---
try:
    import pyradiance
    HAS_PYRADIANCE = True
except ImportError:
    HAS_PYRADIANCE = False
    pyradiance = None


def _is_accelerad_available(binary_name):
    """Check if the specified Accelerad binary is available."""
    return get_binary_path(binary_name) is not None


def rpict(
    view: Sequence[str],
    octree: Union[pathlib.Path, str],
    xres: Optional[int] = None,
    yres: Optional[int] = None,
    report: float = 0,
    report_file: Optional[pathlib.Path] = None,
    params: Optional[Sequence[str]] = None
) -> bytes:
    """Wrapper for rpict. Uses accelerad_rpict if available, otherwise pyradiance.rpict.

    Args:
        view (Sequence[str]): View parameters as a list of strings.
        octree (Union[pathlib.Path, str]): Path to the octree file.
        xres (Optional[int]): X resolution.
        yres (Optional[int]): Y resolution.
        report (float): Reporting interval in minutes.
        report_file (Optional[pathlib.Path]): File to write error reports to.
        params (Optional[Sequence[str]]): Additional parameters.

    Returns:
        bytes: The output of the command (usually image data).
    """
    binary = "accelerad_rpict"
    if _is_accelerad_available(binary):
        # --- Construct arguments for Accelerad ---
        args = []

        # --- View parameters ---
        if view:
            args.extend(view)

        # --- Params ---
        if params:
            args.extend(params)

        # --- Resolution ---
        if xres is not None:
            args.extend(["-x", str(xres)])
        if yres is not None:
            args.extend(["-y", str(yres)])

        # --- Report ---
        if report > 0:
            args.extend(["-t", str(report)])
        if report_file:
            args.extend(["-e", str(report_file)])

        # --- Octree (positional, usually last) ---
        args.append(str(octree))

        return run_accelerad_command(binary, args=args)

    elif HAS_PYRADIANCE:
        return pyradiance.rpict(view, octree, xres, yres, report, report_file, params)
    else:
        raise RuntimeError("Neither Accelerad nor Pyradiance is available.")


def rtrace(
    rays: bytes,
    octree: Union[pathlib.Path, str],
    header: bool = True,
    inform: str = 'a',
    outform: str = 'a',
    irradiance: bool = False,
    irradiance_lambertian: bool = False,
    outspec: Optional[str] = None,
    trace_exclude: str = '',
    trace_include: str = '',
    trace_exclude_file: Optional[Union[str, pathlib.Path]] = None,
    trace_include_file: Optional[Union[str, pathlib.Path]] = None,
    uncorrelated: bool = False,
    xres: Optional[int] = None,
    yres: Optional[int] = None,
    nproc: Optional[int] = None,
    params: Optional[Sequence[str]] = None,
    report: bool = False,
    version: bool = False
) -> bytes:
    """Wrapper for rtrace. Uses accelerad_rtrace if available, otherwise pyradiance.rtrace.

    Args:
        rays (bytes): Input rays.
        octree (Union[pathlib.Path, str]): Path to the octree file.
        header (bool): Whether to output header.
        inform (str): Input format.
        outform (str): Output format.
        irradiance (bool): Compute irradiance.
        irradiance_lambertian (bool): Compute Lambertian irradiance.
        outspec (Optional[str]): Output specification.
        trace_exclude (str): Materials to exclude from trace.
        trace_include (str): Materials to include in trace.
        trace_exclude_file (Optional[Union[str, pathlib.Path]]): File containing excluded materials.
        trace_include_file (Optional[Union[str, pathlib.Path]]): File containing included materials.
        uncorrelated (bool): Uncorrelated sampling.
        xres (Optional[int]): X resolution.
        yres (Optional[int]): Y resolution.
        nproc (Optional[int]): Number of processes.
        params (Optional[Sequence[str]]): Additional parameters.
        report (bool): Report progress.
        version (bool): Print version.

    Returns:
        bytes: The output of the command.
    """
    binary = "accelerad_rtrace"
    if _is_accelerad_available(binary):
        args = []

        # --- Header ---
        if not header:
            args.append("-h-")

        # --- Format (Combine inform and outform) ---
        if inform and outform:
            args.append(f"-f{inform}{outform}")

        # --- Irradiance ---
        if irradiance:
            args.append("-I")
            if irradiance_lambertian:
                args.append("+")  # --- -I+ ---
        elif irradiance_lambertian:
            args.append("-I+")

        # --- Output spec ---
        if outspec:
            args.extend(["-o", outspec])

        # --- Trace include/exclude ---
        if trace_exclude:
            args.extend(["-te", trace_exclude])
        if trace_include:
            args.extend(["-ti", trace_include])
        if trace_exclude_file:
            args.extend(["-tE", str(trace_exclude_file)])
        if trace_include_file:
            args.extend(["-tI", str(trace_include_file)])

        # --- Uncorrelated ---
        if uncorrelated:
            args.append("-u")

        # --- Resolution ---
        if xres is not None:
            args.extend(["-x", str(xres)])
        if yres is not None:
            args.extend(["-y", str(yres)])

        # --- Processes ---
        if nproc is not None:
            args.extend(["-n", str(nproc)])

        # --- Params (extra flags) ---
        if params:
            args.extend(params)

        # --- Octree (positional) ---
        args.append(str(octree))

        # --- Input rays (stdin) ---
        return run_accelerad_command(binary, args=args, input_data=rays)

    elif HAS_PYRADIANCE:
        return pyradiance.rtrace(
            rays, octree, header, inform, outform, irradiance, irradiance_lambertian,
            outspec, trace_exclude, trace_include, trace_exclude_file, trace_include_file,
            uncorrelated, xres, yres, nproc, params, report, version
        )
    else:
        raise RuntimeError("Neither Accelerad nor Pyradiance is available.")


def rfluxmtx(
    receiver: Union[str, pathlib.Path],
    surface: Optional[Union[str, pathlib.Path]] = None,
    rays: Optional[bytes] = None,
    params: Optional[Sequence[str]] = None,
    octree: Optional[Union[pathlib.Path, str]] = None,
    scene: Optional[Sequence[Union[pathlib.Path, str]]] = None
) -> bytes:
    """Wrapper for rfluxmtx.

    Args:
        receiver (Union[str, pathlib.Path]): Receiver surface or file.
        surface (Optional[Union[str, pathlib.Path]]): Surface name.
        rays (Optional[bytes]): Input rays.
        params (Optional[Sequence[str]]): Additional parameters.
        octree (Optional[Union[pathlib.Path, str]]): Path to octree.
        scene (Optional[Sequence[Union[pathlib.Path, str]]]): Scene files.

    Returns:
        bytes: The output of the command.
    """
    binary = "accelerad_rfluxmtx"
    if _is_accelerad_available(binary):
        args = []

        if params:
            args.extend(params)

        # --- Receiver and Surface ---
        # Note: Mapping logic is approximate based on usage patterns.
        args.append(str(receiver))
        if surface:
            args.append(str(surface))

        if octree:
            args.append(str(octree))

        if scene:
            args.extend([str(s) for s in scene])

        return run_accelerad_command(binary, args=args, input_data=rays)

    elif HAS_PYRADIANCE:
        return pyradiance.rfluxmtx(receiver, surface, rays, params, octree, scene)
    else:
        raise RuntimeError("Neither Accelerad nor Pyradiance is available.")


# --- Generic wrappers for missing functions ---
def rcontrib(*args, **kwargs):
    """Wrapper for rcontrib."""
    binary = "accelerad_rcontrib"
    if _is_accelerad_available(binary):
        # --- We can't easily map kwargs to flags without a defined signature ---
        # So we assume args are flags/positionals.
        return run_accelerad_command(binary, args=args, kwargs=kwargs)
    elif HAS_PYRADIANCE and hasattr(pyradiance, 'rcontrib'):
        return pyradiance.rcontrib(*args, **kwargs)
    else:
        # --- If pyradiance doesn't have it, and accelerad is missing, fail ---
        if not _is_accelerad_available(binary):
            raise RuntimeError(f"{binary} not found.")
        # --- If accelerad is present, we ran it above ---
        return run_accelerad_command(binary, args=args, kwargs=kwargs)


def genBSDF(*args, **kwargs):
    """Wrapper for genBSDF."""
    binary = "accelerad_genBSDF"
    if _is_accelerad_available(binary):
        return run_accelerad_command(binary, args=args, kwargs=kwargs)
    elif HAS_PYRADIANCE and hasattr(pyradiance, 'genBSDF'):
        return pyradiance.genBSDF(*args, **kwargs)
    else:
        if not _is_accelerad_available(binary):
            raise RuntimeError(f"{binary} not found.")
        return run_accelerad_command(binary, args=args, kwargs=kwargs)
