## Measurement protocol

### Subjects 1-44
- Each subject is measured for 8 sets
- Set structure:
  - 1 baseline measurement
  - exercise
  - 1 potentiated measurement
  This makes for 2 measurements (1 baseline and 1 potentiated) per set
  and 16 measurements total.
- Note: subjects 28 and 29 are problematic: they contain 17 total measurements
  with no clear distinction between baseline and potentiation.

### Subjects 45-51
- Each subject is measured for 10-11 sets
  (Subjects 47 and 51 for 11, others for 10)
- Set structure:
  - 8 baseline measurement
  - exercise
  - 8 potentiated measurement
  This makes for 16 measurements per set and between 160 and 176 measurements total.

### Subjects 51-60
- Each subject is measured for 8 sets
- Set structure:
  - 8 baseline measurement
  - exercise
  - 8 potentiated measurement
  This makes for 16 measurements per set and 128 measurements total.


## excel-raw directory
Raw TMG measurement files for all subjects

### File naming convention
General syntax `{subject-ID}-{subject-initials}{TMG-timestamp}.xlsx`
Example: `1-BR20200910125909.xlsx`

### File structure
The standard TMG Excel measurement format; see also `Measurement protocol` above.


## csv-processed directory
This directory holds the same data in the `data-excel-raw` directory,
with the following processing performed:
- CSV format instead of Excel format
- All baseline and all potentiated measurements separated.
  Instead of a single `*.xlsx` file per subject, this directory contains one `*-base.csv` and one `*-pot.csv` per subject.
- For measurements containing 8 sets of 16 reps, (i.e. a measurement protocol with
  8 baseline reps followed by exercise followed by 8 potentiated reps) only 
  the first baseline and first potentiated rep of each measurement is retained.
- Files corresponding to dropped subjects are ommited (see notes in `names-id.csv`)

### File naming convention
General syntax `{subject-ID}-{subject-initials}{TMG-timestamp}-{base|pot}.csv`
Example: `1-BR20200910125909-base.csv`

Each subject will have both a `*-base.csv` and `*-pot.csv` file.

### File structure
Each column corresponds to a measurement.
The first row is a header storing the measurement number from the original TMG Excel file.

For example for `*-base.csv` files:
 - 1st column contains 1st baseline measurement of first set
 - 2nd column contains 1st baseline measurement of second set
 - ...and so on....
 - 8th column contains 1st baseline measurement of eighth set
Only the first 8 sets are used, even if higher sets were measured
as for subjects 45-51.
