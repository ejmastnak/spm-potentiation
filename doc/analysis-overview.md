## Raw data

- TMG measurement data is stored in TMG's Excel format, with one file per subject
- Subjects 1-16 are measured for 8 sets, with 1 pre-ISQ and 1 post-ISQ measurement per set (MPS)
- Subjects 17-54 are measured for 8 sets, with 8 pre-ISQ and 8 post-ISQ measurement per set (MPS)

Jargon: MPS is used to mean "measurement per set" in this document. 

## Data preprocessing

### Convert Excel measurements to CSV

For subjects 1-60:
- Converts to CSV files
- Separates into pre-ISQ and post-ISQ
- For each subject, keeps only first pre-ISQ and first post-ISQ measurement form each set

For subjects 1-16:
- Create separate directory for each measurement
- Separates pre-ISQ and post-ISQ measurements in each set

### Process CSV for use with SPM
For each pre-ISQ/post-ISQ TMG measurement pair
- Trim to first 100 ms
- Filter modification to mitigate false SPM significance
- Normalize to the displacement maximum value in the pair 
  (in practice this maximum occurs in the post-ISQ signal, but no a priori assumption is made)

## Analysis

### TMG parameter computation

- 1MPS files: Create 1 pre/post-ISQ file per subject holding the TMG params from the first pre/post-ISQ measurement in each of the subjects measurement sets
- 8MPS files: Create 1 pre/post-ISQ directory per subject.
  Inside this directory, create 1 file per measurement set containing TMG parameters for all measurements in that set.

### TMG parameter analysis

Test configurations: compare pre-ISQ and post-ISQ TMG parameter values for...
- each subject and each set for sets 1-8 (8 MPS)
- each subject across sets using one measurement from each set (1 MPS)
- across all subjects for each set

In each test configuration compute:
- Mean pre-ISQ value and post-ISQ value of each parameter
- Sample standard deviation of pre-ISQ value and post-ISQ value of each parameter 
- Percent change between pre- and post-ISQ value relative to pre-ISQ baseline
- `t`-statistic value from a dependent Student's t-test for paired samples comparing
  pre-ISQ value and post-ISQ value 
- `p` value from above-described t-test.

### SPM analysis

Test configurations: compare pre-ISQ and post-ISQ TMG signals for...
- each subject and each set for sets 1-8 (8 MPS)
- each subject across sets using one measurement from each set (1 MPS)
- across all subjects for each set

In each test configuration:
- Perform an SPM paired t-test on the trimmed, normalized pre-exercise and post-exercise TMG signals
- Query or compute discrete parameters summarizing above SPM paired t-test

## Article output

### Tables

TMG parameters for representative pre-ISQ/post-ISQ comparision for:
- one subject and one set (8 MPS)
- one subject across eight sets (1 MPS)
- all subjects for a given set

### Tables

SPM paired t-test plots for representative pre-ISQ/post-ISQ comparision for:
- one subject and one set (8 MPS)
- one subject across eight sets (1 MPS)
- all subjects for a given set
