## Analysis process

### Input dataset
- 55 subjects
- 4 sets per subject
- 1 pre-exercise and 1 post-exercise measurement per set
- 1000 data points per measurement (1 second of data a 1 kHz sampling)
(Described more thoroughly in `data-used-for-analysis.md`.)

### Data pre-processing: Normalization and trimming
**TODO:** Normalize TMG data in input dataset.
- Normalize
- Trim: use only first 100 ms of each normalized signal (store the 100 ms as a constant)
- Remove filter artifact
Save files on disk in the directory `/data/csv-for-spm/`

### Analysis
For each set:
- Perform an SPM paired t-test on the trimmed, normalized pre-exercise and post-exercise TMG signals across all subjects.
  Implementation:
  ```python
  t = spm1d.stats.ttest2(normed_post_data, normed_pre_data)
  ti = t.inference(alpha = 0.05, two_tailed=False)
  ```
- Query or compute discrete parameters summarizing above SPM paired t-test
  Implementation: `spm_analysis.py`

### Data presented in article
For each set:
- Two-axis (one row, two column) graph of above SPM t-test showing:
  - Axis 0: Mean normalized pre- and post-ISQ TMG signal across all subjects, with standard deviation clouds, with respect to time
  - Axis 1: SPM t-continuum with respect to time with threshold and significance clusters emphasized
- Discrete SPM parameters associated with above SPM paired t-test
