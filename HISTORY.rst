.. :changelog:

2.0.0 (January 2025)
++++++++++++++++++++

**Breaking Changes**

This is a major release with significant modernization. There is no backward compatibility with v1.x.

- **Python Version**: Minimum Python version increased from 3.6 to 3.9
  - Python 3.6, 3.7, and 3.8 are no longer supported
  - Python 3.9-3.13 are now tested and supported
  - Python 3.14 support planned once available

- **Dependency Updates**: All major dependencies updated to modern versions
  - NumPy: 1.19.2+ → 2.0.0+ (major version upgrade)
  - Matplotlib: 3.3.4+ → 3.9.0+
  - Astropy: 6.0.0+ → 6.1.0+
  - pytest: 6.2.4+ → 8.0.0+ (for development/testing)
  - Sphinx: 4.2.0 → 8.0.0+ (for documentation)
  - setuptools_scm: unversioned → 8.0+

**New Features**

- **Comprehensive Test Suite**: Expanded from 11 to 46 tests
  - Added scatter plot tests
  - Added logarithmic axis tests (xlog, ylog)
  - Added multiple subplot tests
  - Added error handling tests
  - Added command-line interface tests
  - Added auto_plot grouping and filtering tests
  - Achieved 92.55% code coverage

- **Code Coverage Integration**
  - Added pytest-cov configuration
  - Added CodeCov integration for CI/CD
  - Added subprocess coverage support
  - Coverage badges available on GitHub

- **Enhanced Testing Infrastructure**
  - Multi-version Python testing (3.9-3.13) in CI/CD
  - Added pytest-timeout for long-running tests
  - Added test result publishing to GitHub Actions
  - Added diagnostic test capabilities

- **Improved Documentation**
  - Added comprehensive Quickstart Guide
  - Documented all command-line options
  - Added Python API usage examples
  - Added scatter plot examples
  - Added logarithmic axis examples
  - Added multiple subplot examples
  - Added troubleshooting section
  - Added migration guide from v1.x

- **Module Execution Support**
  - vplot can now be run as a module: ``python -m vplot``

**Technical Improvements**

- Updated GitHub Actions workflows
  - Uses actions/setup-python@v5 (was v4)
  - Added flexible test result conditions
  - Added coverage data combination step
  - Expanded Python version testing matrix

- Modernized build configuration
  - Added comprehensive pyproject.toml
  - Configured pytest with modern options
  - Added Black code formatter configuration

- Improved test reliability
  - Fixed physical type capitalization handling
  - Added proper subprocess coverage
  - Fixed matplotlib override testing
  - Added proper cleanup in tests

**No API Changes**

Despite the major version bump, the Python API remains unchanged:

- All function names remain the same
- All parameter names remain the same
- All return types remain the same
- Existing scripts using vplot v1.x will work with v2.0 (if using Python 3.9+)

**Migration Guide**

To upgrade from v1.x:

1. Ensure Python 3.9 or higher is installed
2. Update vplot: ``python -m pip install --upgrade vplot``
3. Update dependencies if installing from source
4. No code changes required (API is unchanged)

If you require Python 3.6-3.8 support, continue using vplot v1.x:

.. code-block:: bash

    python -m pip install "vplot<2.0"

**Known Limitations**

- Some tests may fail with vplanet public version due to "(null)" unit handling
  - This is a known limitation in vplanet public version
  - Fixed in vplanet-private (will be migrated in future release)
  - Does not affect normal vplot usage

**Contributors**

- Rory Barnes
- Testing and modernization infrastructure

---

0.3.2 (Summer 2018)
+++++++++++++++++++

- Original release of vplot on PyPI.
