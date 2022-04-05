## Simplified data used for the Frontiers article

### Simplification procedure
Only a small selection of the originally measured data described in `raw-data.md` is used the study presented in the Frontiers article.
For all subjects:
- Only the first four measurement sets are considered for analysis.
- Only the first pre-exercise and first post-exercise measurement is considered for analysis.

Result: 4 pre-exercise and 4-post-exercise measurements per subject.

### Dropped subjects
The followed subjects are not considered for analysis:
- 17
- 22
- 25
- 27
- 28
- 29
The result is a total of 61 - 6 = 55 subjects in the final dataset.

### Summary of dataset
- 55 subjects
- 4 sets per subject
- 1 pre-exercise and 1 post-exercise measurement per set
- 1000 data points per measurement (1 second of data a 1 kHz sampling)

### Directory
The simplified data is stored as CSV files in the directory `/data/data-for-analysis/`.
- One pre-ISQ and one post-ISQ CSV file per subject
- Each file contains four columns; these columns hold the first pre-ISQ or post-ISQ measurement from each of the subject's first four measurement sets.
- Column headers contain:
  - The measurement's set number
  Example: `S1-M2`
