## Raw data

The project's raw data is stored in the directory `/data/excel-raw/`

### Raw exercise and measurement protocol 

One "measurement set" or just "set" consists of, in order:
- Either 1 or 8 pre-exercise TMG measurements, followed within 15 seconds by
- 8 reps of incline squats, followed within 12 seconds by
- Either 1 or 8 post-exercise TMG measurements, followed by
- 150 seconds of rest.

A full measurement session consists of 8 measurement sets per subject.

Subjects 1 through 16, inclusive, perform 8 pre-exercise and 8 post-exercise
TMG measurement per set, for a total of $ (8 sets) * (8 pre-exercise
measurements/set + 8 post-exercise measurements/set) = 128 measurements $

Subjects 17 through 54, inclusive, perform 1 pre-exercise and 1 post-exercise
TMG measurement per set for a total of... 

> (8 sets) * (1 pre-exercise measurement/set + 1 post-exercise measurement/set) = 16 measurements

### TMG measurement

Each individual measurement is a TMG measurement of the subject's rectus
femoris muscle, which returns a one-dimensional time series of muscle
displacement with respect to time, 1000 ms in duration and sampled at 1 kHZ for
a total of 1000 data points per measurement.
