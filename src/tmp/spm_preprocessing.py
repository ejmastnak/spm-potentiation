import numpy as np

"""
A few functions used to pre-process biomechanical time series data
before application of SPM analysis.
"""

START_ROWS_TO_AVERAGE = 3  # number of initial data points to average over when fixing initial false potentiation

def process_pre_data(pre_data, normalize=False, position_offset=0.0):
    if pre_data is None:  # null check
        return

    if normalize: pre_data = pre_data / pre_data.max(axis=0)

    # Add vertical offset, which TODO in practice should be zero
    pre_data = pre_data + self.position_offset

    # Potentially reshape 1D column into 2D array (a matrix with one column)
    if len(pre_data.shape) == 1:
        pre_data = pre_data.reshape(-1, 1)

def process_post_data(pre_data, normalize=False, position_offset=0.0):
    if post_data is None:  # null check
        return

    if self.normalize: post_data = post_data / post_data.max(axis=0)
    post_data = post_data + self.position_offset

    # Potentially reshape 1D column into 2D array (a matrix with one column)
    if len(post_data.shape) == 1:
        post_data = post_data.reshape(-1, 1)

def get_time_offset():
    """
    Corrects for time offset from skipping the first row of the data files,
    which contain zero displacement.
    Motivation: avoid singularities in the SPM t-statistic due to zero variance.
    All time is thus offset proportionally to the number of rows skipped.

    This function assumes the standard 1kHz TMG sample rate, so each row is one millisecond.
    """
    return constants.start_row
