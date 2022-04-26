## Analysis overview

This document summarizes the full data pre-processing and analysis pipeline used in the study.

### 1. Raw data

We begin with raw TMG measurements for each subject.

- TMG measurement data is stored in TMG's Excel format, with one file per subject.
- Subjects 1-16 perform 8 measurement sets, with 1 pre-ISQ and 1 post-ISQ measurement per set (MPS).
- Subjects 17-54 perform 8 measurement sets, with 8 pre-ISQ and 8 post-ISQ measurement per set (MPS).

Jargon: MPS stands for "measurement per set" and ISQ stands for the "incline squat" conditioning exercise used in the study.

### 2. Data preprocessing

#### 2a. Convert Excel measurements to CSV

For all subjects:
- Convert raw Excel files to to CSV files.
- Separate measurements into pre-ISQ and post-ISQ measurements.
- For each subject, keep only first pre-ISQ and first post-ISQ measurement from each set.

For subjects 1-16:
- Create separate directory for each measurement set.
- Separate pre-ISQ and post-ISQ measurements in each set.

#### 2b. Process CSV for use with SPM

For each pre-ISQ/post-ISQ TMG measurement pair:
- Trim measurement to first 100 ms.
- Correct for filter artefact to mitigate non-physical SPM significance in first few milliseconds of each measurement.
- Optionally normalize to the displacement maximum value in the pair 
  (in practice this maximum occurs in the post-ISQ signal, but no a priori assumption is made).

### 3. Analysis

#### 3a. TMG parameter computation

- For 1MPS files: Create 1 pre/post-ISQ file per subject holding the TMG parameters from the first pre/post-ISQ measurement in each of the subject's measurement sets.
- For 8MPS files: Create 1 pre/post-ISQ directory per subject.
  Inside this directory, create 1 file per measurement set containing TMG parameters for all measurements in that set.

#### 3b. TMG parameter analysis

We use three test configurations, which compare pre-ISQ and post-ISQ TMG parameter values
1. across all subjects for each measurement set
1. for each subject across sets using the first measurement from each set (for all subjects)
1. for each subject and each set (for 8 MPS subjects only).

In each test configuration compute:
- Mean pre-ISQ value and post-ISQ value of each parameter
- Sample standard deviation of pre-ISQ value and post-ISQ value of each parameter 
- Percent change between pre- and post-ISQ value relative to pre-ISQ baseline
- `t`-statistic value from a dependent Student's t-test for paired samples comparing
  pre-ISQ value and post-ISQ value 
- `p` value from above-described t-test.

#### 3c. SPM analysis

In each of the three test configurations described for TMG parameter analysis:
- Perform an SPM paired t-test on the trimmed pre-exercise and post-exercise TMG signal pairs and save the resulting figure.
- Query or compute discrete parameters summarizing the SPM paired t-test.

### 4. Results for manuscript

#### 4a. Tables

Create a representative table comparing pre/post-ISQ TMG parameter values for:
- one subject in a given set (for an 8 MPS subject)
- one subject across eight sets (for a 1 MPS subject)
- across all subjects for a given set.

#### 4b. Figures

Create representative SPM paired t-test plots comparing pre/post-ISQ TMG signals for:
- one subject in a given set (for an 8 MPS subject)
- one subject across eight sets (for a 1 MPS subject)
- across all subjects for a given set.

