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

### How the raw data was measured

One "measurement set" or just "set" consists of, in order:
- Either 1 or 8 pre-exercise TMG measurements, followed within 15 seconds by
- 8 reps of incline squats, followed within 12 seconds by
- Either 1 or 8 post-exercise TMG measurements, followed by
- 150 seconds of rest.

Each subject performed 8 measurement sets.
Subjects 1 through 16, inclusive, performd 8 pre-exercise and 8 post-exercise
TMG measurement per set, for a total of 
`(8 sets) * (8 pre-exercise measurements/set + 8 post-exercise measurements/set) = 128 measurements per subject`.

Subjects 17 through 54, inclusive, perform 1 pre-exercise and 1 post-exercise
TMG measurement per set for a total of
`(8 sets) * (1 pre-exercise measurement/set + 1 post-exercise measurement/set) = 16 measurements per subject`.

Each individual measurement is a TMG measurement of the subject's rectus
femoris muscle.
The TMG measurement is a one-dimensional time series of muscle
displacement with respect to time, 1000 ms in duration and sampled at 1 kHZ for
a total of 1000 data points per measurement.
