import numpy as np

"""
A few functions used to pre-process biomechanical time series data
before application of SPM analysis.
"""

START_ROWS_TO_AVERAGE = 3  # number of initial data points to average over when fixing initial false potentiation

def fix_false_spm_significance(pre_data, post_data):
    """
    Fixes issue of SPM showing significance regions for miniscule 
    (e.g. order 0.001 mm) differences between post-exercise and initial 
    measurements over the first few milliseconds of a TMG measurement.

    These differences arise from random artifacts from initial filtering, 
    and do not represent physical information.
    The differences are removed by subtracting the average of the difference 
    between pre and post-exercise data over the first few ms of the TMG curve
    from the post-exercise data.

    This is safe to do without appreciable affecting the later (i.e. > ~5 ms)
    portion of a TMG signal because differences in the first few ms are of the
    order 0.001 mm, while typical values in the TMG curve are of the order 5 mm.

    :param pre_data: 2D Numpy array containing raw pre-exericse data.
        Rows traverse time and columns traverse measurements
    :param post_data: 2D Numpy array containing raw post-exercise data.
    :return: adjusted pre/post-exercise data such that false SPM significance disappears
    """
    # the average of the average pre-exercise signal over the first few data points
    pre_mean = np.mean(np.mean(pre_data[0:START_ROWS_TO_AVERAGE, :], axis=1))
    post_mean = np.mean(np.mean(post_data[0:START_ROWS_TO_AVERAGE, :], axis=1))
    if post_mean > pre_mean:
        post_data -= np.mean(post_mean - pre_mean)

    # elif mode == BASE_ATRO:
    #     if pre_mean > post_mean:
    #         pre_data -= np.mean(pre_mean - post_mean)

    return pre_data, post_data


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
