## Results

This directory holds the results of all analyses performed in this study, including:
- TMG twitch contraction parameters for all TMG measurements
- Statistical analysis of TMG contraction parameters before and after the conditioning exercise
- SPM analysis of TMG signals before and after the conditioning exercise
- Figures comparing pre/post-conditioning TMG signals and showing SPM test results

### Generate results programmatically

After downloading, this directory is empty except for the `README.md` file, with the following structure:
```
results
└── README.md
```
But the directory structure should eventually look like this:
```
results
├── README.md
├── spm-params-by-set-across-subj
├── spm-params-by-subj-across-sets-1mps
├── spm-params-by-subj-by-set-8mps
├── spm-plots-by-set-across-subj
├── spm-plots-by-subj-across-sets-1mps
├── spm-plots-by-subj-by-set-8mps
├── tmg-params-by-subj-1mps
├── tmg-params-by-subj-8mps
├── tmg-stats-by-set-across-subj
├── tmg-stats-by-subj-across-sets-1mps
└── tmg-stats-by-subj-by-set-8mps
```
You are meant to generate the results programmatically.
To do so,

1. First read through the `README.md` in the project's `data` directory and perform the data pre-processing steps described therein.
1. After generating data files, switch to the project's `src` directory.
1. Read the `README.md` file in the `src` directory.
1. Run following Python scripts in the `src` directory:
   1. `tmg-params.py`
   1. `tmg-stats.py`
   1. `spm-analysis.py`

   These scripts will generate the study's results using the content of the `data` directory.

