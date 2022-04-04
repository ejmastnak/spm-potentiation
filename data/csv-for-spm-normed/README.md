See description in `/doc/spm-analysis.py` for more context.

TLDR: This directory holds further-processed versions of the files 
in `/data/csv-processed` that are convenient for analysis with SPM.
The following modifications of `/data/csv-processed`  are made to generate this directory:
- Normalize
- Trim: use only first 100 ms of each normalized signal (store the 100 ms as a constant)
- Remove filter artifact
