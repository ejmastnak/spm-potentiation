## Data

This directory holds the measurement data files used in this study.
The `excel-raw/` directory holds TMG measurements in their original form.
To reproduce the study's results, you must first convert the raw TMG measurements into text-based CSV files more conducive to further analysis.

### Generate remaining data programmatically

After downloading, this directory has the following structure:
```
data
├── excel-raw
├── LICENSE-CC-BY.md
└── README.md
```
But the directory structure should eventually look like this:
```
data
├── csv-for-spm-1mps
├── csv-for-spm-8mps
├── csv-raw-1mps
├── csv-raw-8mps
├── excel-raw
├── LICENSE-CC-BY.md
└── README.md
```
You are meant to generate the remaining files programmatically.
To do so,

1. Switch to the project's `src` directory
1. Read the `README.md` file in the `src` directory
1. Run the Python script `data_processing.py`, which will generate remaining data files based on the contents of the `excel-raw` directory.

