## Source code

This directory holds all code used to process and analyze the project's measurement data and to generate figures and tables.
The source code is written in Python 3.

### Dependencies

You will need to install the following software to reproduce the study's results on your local computer.

- [Python 3](https://python.org/): the programming language in which the project is written
- [NumPy](https://numpy.org/): a Python package we use for numerical routines and storing data
- [SciPy](https://scipy.org/): a Python package we use for statistical routines
- [Matplotlib](https://matplotlib.org/): a Python package for data visualization
- [Pandas](https://pandas.pydata.org/): a Python package we use for manipulation of tabular CSV and XLSX data
- [SPM1D](https://spm1d.org/): the standard Python package for 1D statistical parametric mapping
- [TMG-Biomechanics](https://github.com/ejmastnak/tmg): a Python package for time series analysis of tensiomyography measurements

If uncertain, we suggest installing Python from the [official website](https://python.org/).
After installing Python, each of the required Python packages can be installed with the `pip` package manager, which should ship by default with any up-to-date installation of Python 3.

### Reproducing results

The code is intentionally written to make results straightforward to reproduce.
That said, some experience working with Python would be helpful before installing dependencies and reproducing results---suggested prerequisites are (1) installing Python packages with `pip` and (2) running a Python file, either from the command line or using a graphical Python launcher.

1. Install all dependencies.
1. Clone this GitHub repository onto your local computer.
1. Navigate to the project's `src` directory.
1. Run each of the following Python files in the order they are listed.
   1. `data_preprocessing.py`
   1. `tmg_params.py`
   1. `tmg_stats.py`
   1. `spm_analysis.py`
   1. `make_tables.py`
   1. `make_figures.py`

### Source code structure

Here is a summary of how the code is organized:

- `constants.py`: organizes project-wide constants into one location.
- `data_preprocessing.py`: converts raw TMG measurements into text-based CSV files better suited to further analysis with SPM.
- `frontiers_utils.py`: miscellaneous utility functions most related to file I/O.
- `make_figures.py`: generates the figures used in the manuscript.
- `make_tables.py`: generates the LaTeX tables used in the manuscript.
- `plotting.py`: creates plots to help visualize data and results.
- `spm_analysis.py`: performs SPM analysis.
- `tmg_params.py`: computes twitch contraction parameters from TMG measurements.
- `tmg_stats.py`: performs statistical analysis of TMG contraction parameters.
- `xlsx_csv_conversion.py`: helper functions used to convert raw XLSX measurement files to CSV files.


