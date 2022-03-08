# Root directory with measurement data
ROOT_DATA_DIR = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/"

# Intial step in pipeline of processing data
INITIAL_DATA_DIR = ROOT_DATA_DIR + "csv-for-initial-analysis/"


# --------------------------------------------- #
# CSV data file row at which to begin reading data (0-indexed)
start_row = 1  

# The first row, assuming zero-based indexing, of TMG data to use for SPM analysis.
# Motivation: zero-th row is always zero, which causes zero-variance problems in SPM.
TMG_DATA_START_ROW_FOR_SPM = 1

# Number of rows to read after start_row is reached
max_rows = 100  

# IDK, probably an offset to add to a TMG displacement signal
displacement_offset = 0.0

# Whether to normalize a TMG such that its maximum value occurs at one
normalize = False

SPM_PARAM_NAMES = ["alpha",
        "threshold",
        "p value",
        "Significance start time [ms]",
        "Significance end time [ms]",
        "Centroid time [ms]",
        "Centroid t-value",
        "Maximum",
        "Area above threshold",
        "Area above x axis"]


# Names of TMG parameters
TMG_PARAM_NAMES = ["Dm:", "Td:", "Tc:", "Ts:", "Tr:", "P1:", "P2:", "P3:",
        "RDD Max:", "RDD Min:", "RDD Peak to Peak:",
        "RDD Max Time:", "RDD Min Time:", "Max to Min Time:"]

# Names of statistical quantities used to analyze TMG parameters
TMG_STAT_NAMES = ['base-avg', 'pot-avg', 'base-sample-std', 'pot-sample-std', 't-statistic', 't-test-p-value']


# BEGIN DUMP FROM TMG PROJECT
# --------------------------------------------- #-

# The first row (assuming zero-based row indexing) containing 
# TMG signal data in a standard TMG format Excel file.
TMG_DATA_START_ROW = 24

# Time in milliseconds between successive points in a TMG signal (which is sampled at 1kHz)
TMG_DT = 1

# Maximum number of rows (datapoints) of the TMG signal to analyze.
# Also the number of milliseconds to analyze, assuming 1kHz sampling.
TMG_MAX_ROWS = 500  

# The number of points to use for interpolating polynomial when estimating 
# the times of the TMG parameters td, tc, ts and tr
TIME_INTERP_WINDOW_SIZE = 2  

# [ms] time granularity to use when interpolating td, tc, ts and tr times
TIME_INTERP_DT = 0.01  

# Occasionally TMG signal will have artificial, filter-induced local maxima in
# the first few data points that can be confusing when finding Dm. This 
# parameter is used to reject any local maxima that occur before 
REJECT_TMG_PEAK_INDEX_LESS_THAN = 8

# Number of points to use on either side of extrema when interpolating
EXTREMA_INTERP_WINDOW_SIZE = 2  

# [ms] time granularity to use when interpolating extrema (generally of rdd signal)
EXTREMA_INTERP_DT = 0.01  

# Names of TMG parameters
TMG_PARAM_NAMES = ["Dm:", "Td:", "Tc:", "Ts:", "Tr:", "P1:", "P2:", "P3:",
        "RDD Max:", "RDD Min:", "RDD Peak to Peak:",
        "RDD Max Time:", "RDD Min Time:", "Max to Min Time:"]

# Names of statistical quantities used to analyze TMG parameters
TMG_STAT_NAMES = ['base-avg', 'pot-avg', 'base-sample-std', 'pot-sample-std', 't-statistic', 't-test-p-value']

# BEGIN CONVERSION MODE CONSTANTS
# --------------------------------------------- #
# Input: One TMG-formatted Excel file
# Output: One CSV file holding all measurements in the Excel file
#         in exactly the same order as they appear in the Excel file.
VERBATIM = 1

# Input: One TMG-formatted Excel file
# Output: Two CSV files:
#         One file holds all baseline measurements in the measurement session.
#         One file holds all potentiated measurements in the measurement session.
# All baseline measurements are clumped into one CSV file and all
# potentiated measurements are clumped into a separate CSV file.
SEPARATE_PRE_AND_POST = 2

# Input: One TMG-formatted Excel file
# Output: Two CSV files PER MEASUREMENT SET in Excel file:
#         One file holds baseline measurements in that set.
#         One file holds potentiated measurements in that set.
#         Creates (2 times the number of sets in Excel file) CSV files total.
# The Excel file is divided into sets, and each set is further
# divided into baseline and potentiated measurements.
PRE_POST_BY_SET_ALL_REPS = 3

# Input: One TMG-formatted Excel file
# Output: Two CSV files:
#         One file holds the FIRST baseline measurement of each set.
#         One file holds the FIRST potentiated measurement of each set.
# The Excel file is divided into sets, and each set is further
# divided into baseline and potentiated measurements, but only
# the first rep of each set is saved to the outputted CSV file.
PRE_POST_BY_SET_FIRST_REP = 4
# --------------------------------------------- #
