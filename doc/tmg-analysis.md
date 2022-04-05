## Analysis using TMG parameters

### Input dataset
- 55 subjects
- 4 sets per subject
- 1 pre-exercise and 1 post-exercise measurement per set
- 1000 data points per measurement (1 second of data a 1 kHz sampling)
(Described more thoroughly in `data-used-for-analysis.md`.)

There are (55 subjects) * (4 sets/subject) * (1 pre-exercise measurement + 1 post-exercise measurement) = 55 * 4 * 2 = 440 measurements in the dataset.

### Analysis
- Compute TMG parameters of all measurements.
  Implementation: algorithms in `tmg.py`.
- Compute time derivative (RDD) of all TMG measurements.
  Implementation: `np.gradient(tmg_signal, dt)`, where `dt` is the spacing in time between samples in `tmg_signal`, which is 1 millisecond.
- Compute RDD paramaters of all RDD signals.
  Implementation: algorithms in `tmg.py`.

### Preliminary outputted data
For each subject, create a TMG parameter CSV file with:
- Rows: TMG parameters
- Columns: Measurements
- Column headers contain:
  - Pre/Post exercise e.g. `PRE` or `POE`
  - The measurement's set number
  - The measurement's number in the TMG Excel from original measurement session (see `raw-data.md`)

### Data presented in article
For measurement set 1, 2, 3, 4
- Mean pre-ISQ value and post-ISQ value of each parameter averaged across all subjects.
  Implementation: `np.average`.
- Sample standard deviation of pre-ISQ value and post-ISQ value of each parameter across all subjects
  Implementation: `np.std` with `ddof=1`.
- `t`-statistic value from a dependent Student's t-test for paired samples comparing
  pre-ISQ value and post-ISQ value of each parameter across all subjects.
  Implementation: `scipy.stats.ttest_rel`.
- `p` value from above-described t-test.
  Implementation: `scipy.stats.ttest_rel`.
