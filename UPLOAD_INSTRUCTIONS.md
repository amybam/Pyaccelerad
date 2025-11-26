# Uploading to TestPyPI and PyPI

The package has been prepared following PyPA standards.

## Prerequisites

You need `twine` to upload packages.

```bash
pip install twine
```

## 1. Upload to TestPyPI

TestPyPI is a separate instance of PyPI for testing and experimentation.

1.  Register an account at [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/) (if you haven't already).
2.  Create an API token in your account settings.
3.  Run the following command:

```bash
python -m twine upload --repository testpypi dist/*
```

When prompted for username, use `__token__`.
When prompted for password, use your API token (starting with `pypi-`).

## 2. Verify Installation from TestPyPI

You can try installing your package from TestPyPI to ensure it works:

```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps pyaccelerad
```

*Note: We use `--no-deps` because TestPyPI might not have all the dependencies (like `pyradiance`) that the real PyPI has. You might need to install dependencies manually first.*

## 3. Upload to PyPI (Production)

Once you are satisfied:

1.  Register an account at [https://pypi.org/account/register/](https://pypi.org/account/register/).
2.  Create an API token.
3.  Run:

```bash
python -m twine upload dist/*
```

## Package Details

- **Configuration**: `pyproject.toml` (Modern standard)
- **License**: MIT (`LICENSE` file included)
- **Build Artifacts**: `dist/` folder contains the `.tar.gz` (Source) and `.whl` (Wheel).
