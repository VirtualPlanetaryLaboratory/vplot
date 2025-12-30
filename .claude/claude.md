The vplot repository is the tool of plotting individual simulation results. It has two primary purposes: 1) as a CLI tool that pops up figures that show a variable's value as a function of time, and 2) a Python package that compliments matplolib by modifyng that output to have a specific font and access to a standardized color pallete. Note that as currently implemented, vplot overrides matplotlib functions, so it is of critical importance that no vplot formatting be installed in a permanent fashion on any account. It shall only work in scripts in which it has been explcitly imported.

---

# Modernization Plan (v2.0.0)

## Overview

Modernize the vplot package (571 lines across 5 modules) to meet current standards and align with VPL project style guide. This is a comprehensive overhaul addressing dependencies, code style, testing, and documentation.

## Objectives

1. **Modernize Dependencies**: Update to NumPy 2.0+, Matplotlib 3.9+, Astropy 6.1+, pytest 8.0+, Sphinx 8.0+
2. **Expand Testing**: Add 15+ new tests covering scatter plots, auto_plot validation, command-line interface, error handling
3. **Review Logic**: Address HACK/TODO comments, verify unit conversion logic, improve error messages
4. **Update Style**: Convert entire codebase to Hungarian notation per VPL style guide

## Key Decisions

- ✅ Convert to Hungarian notation (e.g., `auto_plot()` → `flistAutoPlot()`, `bodies` → `listBodies`)
- ✅ Keep global matplotlib.figure.Figure override (works as intended)
- ✅ Relax 20-line rule for cohesive complex logic (only split where it improves clarity)
- ✅ Support Python 3.9-3.14 (drop 3.6-3.8)
- ❌ No backward compatibility (major v2.0 release)
- **✅ CRITICAL: Do NOT use Hungarian notation for matplotlib override parameters** (preserve standard matplotlib syntax for users)

## Hungarian Notation Strategy

**General Rule**: Apply Hungarian notation throughout the codebase.

**Exception - Matplotlib Compatibility**: Do NOT apply Hungarian notation to:
1. VPLOTFigure class parameters that users pass (e.g., `xlog`, `ylog`, `max_label_length`, `mpl_units`, `auto_legend`)
2. VPLOTFigure instance attributes that correspond to these parameters
3. Function parameters that match standard matplotlib conventions (e.g., `FigureClass`, `array`)

**Rationale**: vplot is a drop-in matplotlib enhancement. Users should only need to remember matplotlib syntax. Internal variables and non-user-facing code should use Hungarian notation.

**Examples**:
- ✅ User API: `plt.figure(xlog=True)` - KEEP AS-IS
- ✅ Internal variables: `bSingleBody`, `listBodies`, `sUnit` - CONVERT
- ✅ Function names: `flistAutoPlot()`, `fnAddLabels()` - CONVERT
- ✅ Internal helpers: `ftupleGetArrayInfo()` - CONVERT

## Implementation Stages

### Stage 1: Dependency Updates (2-4 hours) ⬜ NOT STARTED

**Files to update:**
1. [setup.py](setup.py:22-28) - Update install_requires to numpy>=2.0.0, matplotlib>=3.9.0, astropy>=6.1.0, setuptools_scm>=8.0
2. [environment.yml](environment.yml) - Update to python>=3.9,<3.15, numpy>=2.0.0, pytest>=8.0.0, sphinx>=8.0.0
3. [.github/workflows/tests.yml](.github/workflows/tests.yml:15-21) - Remove Python 3.6-3.8, add 3.13-3.14
4. [pyproject.toml](pyproject.toml) - Add pytest configuration

**Verification**: Run existing tests with new dependencies, fix any NumPy 2.0 compatibility issues.

### Stage 2: Documentation Infrastructure (2-3 hours) ⬜ NOT STARTED

**Create:**
1. [docs/quickstart.rst](docs/quickstart.rst) - NEW: Installation, basic API, CLI usage, common use cases
2. [docs/index.rst](docs/index.rst) - Add quickstart to toctree
3. [HISTORY.rst](HISTORY.rst) - Add v2.0.0 release notes

### Stage 3: Hungarian Notation Conversion (8-12 hours) ⬜ NOT STARTED

**Convert in dependency order:**

#### 3.1 [vplot/colors.py](vplot/colors.py) (5 lines)
- `red` → `sRed`, `orange` → `sOrange`, `pale_blue` → `sPaleBlue`, `dark_blue` → `sDarkBlue`, `purple` → `sPurple`

#### 3.2 [vplot/figure.py](vplot/figure.py) (374 lines - MOST CRITICAL)
- Module functions: `_get_array_info()` → `ftupleGetArrayInfo()`, `figure_wrapper()` → `fnFigureWrapper()`
- **VPLOTFigure parameters**: KEEP AS-IS (xlog, ylog, max_label_length, mpl_units, auto_legend)
- **VPLOTFigure instance attributes**: KEEP AS-IS
- Internal methods: `_ax_observer()` → `fnAxObserver()`, `_add_labels()` → `fnAddLabels()`, `_format_axes()` → `fnFormatAxes()`
- Internal variables: Apply Hungarian notation (booleans→b, lists→list, strings→s, etc.)

#### 3.3 [vplot/auto_plot.py](vplot/auto_plot.py) (135 lines)
- Function: `auto_plot()` → `flistAutoPlot()`
- Parameters: `path`→`sPath`, `sysname`→`sSysname`, `group`→`sGroup`, `bodies`→`listBodies`, `params`→`listParams`, `show`→`bShow`
- Fix typos: "Kewyord" → "Keyword"

#### 3.4 [vplot/command_line.py](vplot/command_line.py) (37 lines)
- Function: `_entry_point()` → `fnEntryPoint()`
- Update call to `flistAutoPlot()`

#### 3.5 [vplot/__init__.py](vplot/__init__.py) (20 lines)
- Update imports for new function names

#### 3.6 [setup.py](setup.py:30)
- Update entry point: `"vplot=vplot.command_line:fnEntryPoint"`

### Stage 4: Test Conversion & Expansion (6-8 hours) ⬜ NOT STARTED

#### 4.1 Convert existing tests
- [tests/test_figure.py](tests/test_figure.py) - Convert variable names, update function calls
- [tests/test_autoplot.py](tests/test_autoplot.py) - Convert to `flistAutoPlot()`

#### 4.2 Add tests to test_figure.py
1. `test_scatter()` - Basic scatter with metadata
2. `test_scatter_two_bodies()` - Multi-body scatter
3. `test_mixed_plot_scatter()` - Combined plot/scatter
4. `test_xlog()` / `test_ylog()` - Logarithmic axes (use `xlog=True`, `ylog=True`)
5. `test_incompatible_y_types()` - Error handling
6. `test_multiple_subplots()` - Multi-axis figures

#### 4.3 Expand test_autoplot.py
1. `test_autoplot_return_values()` - Validate return type
2. `test_autoplot_group_type()` / `_param()` / `_none()` - Grouping modes
3. `test_autoplot_filter_bodies()` / `_params()` - Filtering
4. `test_autoplot_invalid_group()` - Error handling
5. `test_autoplot_xlog()` / `_ylog()` - Log axes

#### 4.4 Create [tests/test_command_line.py](tests/test_command_line.py) - NEW
1. `test_entry_point_exists()` - CLI available
2. `test_command_line_group()` - Arguments work

**Target**: 90%+ code coverage

### Stage 5: Logical Review & Cleanup (2-3 hours) ⬜ NOT STARTED

#### 5.1 Address HACK comments
- Line 105: Update to "Override ax.scatter to preserve metadata in Quantity arrays."
- Line 360: Update to "Override matplotlib.figure.Figure globally to enable automatic labeling."
- Line 363: Clearer explanation of plt.figure wrapper

#### 5.2 Address TODO comments
- figure.py line 135: Create GitHub issue for imshow support
- tests.yml line 37: Remove TODO (vplanet is required)

#### 5.3 Verify unit conversion logic
- Test with multiple units of same physical type
- Verify NumPy 2.0 + Matplotlib 3.9+ compatibility

#### 5.4 Verify physical type extraction
- Test with Astropy 6.1+ compatibility

### Stage 6: Optional Function Refactoring (4-6 hours) ⬜ OPTIONAL

Split only if improves clarity:
- `flistAutoPlot()` helpers: `flistGetParams()`, `flistPlotByType()`, etc.
- `fnAddLabels()` helpers: `ftupleGetPhysicalType()`, `fsGetUnit()`, etc.

### Stage 7: Documentation Completion (4-6 hours) ⬜ NOT STARTED

1. Update all docstrings with Hungarian parameter names
2. Update API documentation
3. Update example notebooks (4 files in docs/notebooks/)
4. Update README.md (Python version badge, test count, v2.0 note)
5. Complete HISTORY.rst

### Stage 8: Final Validation (3-4 hours) ⬜ NOT STARTED

1. Automated: pytest, vplot --help, sphinx-build
2. Multi-version: Python 3.9 + 3.14, macOS + Linux
3. Manual: Import, plot, CLI, scatter, docs
4. Release: Tag v2.0.0, GitHub release, PyPI

## Critical Files (Priority Order)

1. **[vplot/figure.py](vplot/figure.py)** - 374 lines, most complex
2. **[vplot/auto_plot.py](vplot/auto_plot.py)** - 135 lines, primary API
3. **[setup.py](setup.py)** - Dependencies and entry point
4. **[tests/test_figure.py](tests/test_figure.py)** - Convert and expand
5. **[environment.yml](environment.yml)** - Conda environment

## Progress Tracking

Use checkboxes to track completion:
- ⬜ Stage 1: Dependencies
- ⬜ Stage 2: Documentation infrastructure
- ⬜ Stage 3: Hungarian conversion
- ⬜ Stage 4: Testing
- ⬜ Stage 5: Cleanup
- ⬜ Stage 6: Refactoring (optional)
- ⬜ Stage 7: Docs completion
- ⬜ Stage 8: Validation

**Time Estimate**: 31-46 hours focused work, 1-2 weeks calendar time

## Notes

- Breaking release v2.0.0, no backward compatibility
- Matplotlib parameter names preserved for user convenience
- NumPy 2.0 may require array operation fixes
- Global matplotlib override is intentional and correct