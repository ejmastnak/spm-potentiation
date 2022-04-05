## Format
Some formatting specifications

### Column headers
For files in:
- `csv-processed`
- `tmg-params-by-subject`

The general form is
```sh
ID<subject_ID>-S<measurement_set_number>-M<measurement_number_in_raw_Excel>
```
Motivation: Excel file is a single sequence of measurements.
Specifying a measurement number in column headers of CSV file makes it easier to map between original Excel measurements and CSV files.
