""" 
This script performs SPM analysis of TMG data.
Input data: the per-subject TMG measurement files in `/data/csv-for-spm-normed/`

"""

# SPM paired t-test by set
"""
For each measurement set:
- Performs an SPM paired t-test comparing preprocessed pre-ISQ and post-ISQ
  TMG signals across all subjects and saves the resulting SPM plots.
- Queries from `spm1d` or directly computes discrete parameters 
  summarizing the above-described SPM paired t-test.

Input data: the per-subject measurement files in `/data/csv-for-spm-normed/`
Output data: 
    - Per-set CSV files in `/output/spm-params-by-set/`
      summarizing the results of the above-described statisical analysis.
    - Per-set JPG files storing a two-axis (one row, two column)
      graph the set's above-described SPM t-test and showing:
      - Axis 0: Mean normalized pre-ISQ and post-ISQ TMG signal across 
        all subjects, with standard deviation clouds, with respect to time.
      - Axis 1: SPM t-continuum with respect to time with threshold 
        and significance clusters emphasized.

"""
