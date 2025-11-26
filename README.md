# Pyaccelerad

Pyaccelerad is a Python interface for [Accelerad](https://nljones.github.io/Accelerad/), designed to mimic the API of [Pyradiance](https://github.com/LBNL-ETA/pyradiance).

It wraps the Accelerad binaries (`accelerad_rpict`, `accelerad_rtrace`, etc.) allowing you to call them from Python.

## Installation

```bash
pip install .
```

## Requirements

**Accelerad Binaries**: You must have Accelerad installed.
By default, Pyaccelerad looks for binaries in:
`C:\Program Files\Accelerad\bin`

You can override this by setting the `ACCELERAD_BIN` environment variable to your Accelerad bin directory.

## Usage

```python
import pyaccelerad as pa

# Call accelerad_rpict
# Arguments are passed as flags.
# e.g. -ab 5 becomes ab=5
# Positional arguments are passed as a list.

# Example: accelerad_rpict -ab 5 -vf view.vf scene.oct
output_image_data = pa.rpict("scene.oct", ab=5, vf="view.vf")

# You can write the output to a file
with open("output.hdr", "wb") as f:
    f.write(output_image_data)
```

## Mapped Functions

The following functions are mapped to their Accelerad counterparts:

- `rpict` -> `accelerad_rpict`
- `rtrace` -> `accelerad_rtrace`
- `rcontrib` -> `accelerad_rcontrib`
- `rfluxmtx` -> `accelerad_rfluxmtx`
- `genBSDF` -> `accelerad_genBSDF`

## Notes on Binaries

Accelerad binaries are compiled against specific CUDA versions. Ensure your installed Accelerad version matches your hardware and drivers. Pyaccelerad does not bundle these binaries; it relies on your local installation.
