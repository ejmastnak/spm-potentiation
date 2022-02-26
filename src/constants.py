
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
