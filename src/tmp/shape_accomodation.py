import numpy as np

# --------------------------------------------- #
# A collection of functions used to ensure pre and post-exercise data files
# intended for use with SPM have the same number of rows and columns.
# --------------------------------------------- #

def match_rows(pre_data, post_data, pre_rows, post_rows):
    """
    If there are more post-exercise rows than pre-exercise rows,
    trims number of rows in post-exercise array to match 
    the number of rows in pre-exercise array.
    And vice versa for opposite case.

    :param pre_data: 2D Numpy array containing pre-exercise measurement data
    :param post_data: 2D Numpy array containing post-exercise measurement data
    """
    if pre_rows < post_rows:  # more post-exercise rows; trim post-exercise to match pre
        post_data = post_data[0:pre_rows, :]

    elif pre_rows > post_rows:  # more post-exercise rows; trim pre-exercise to match post
        pre_data = pre_data[0:post_rows, :]

    return pre_data, post_data


def match_cols(pre_data, post_data, pre_rows, pre_cols, post_rows, post_cols):
    """
    If there are more post-exercise columns than pre-exercise columns, 
    adds more columns to pre-exercise array until the number of columns
    in pre-exercise and post-exercise match.
    And vice versa for opposite case.

    Extra columns are found by taking the average of the existing columns, 
    and then adding noise to each datapoint; the noise size is in the 
    interval of +/- 10 percent of each data point's absolute value.

    :param pre_data: 2D Numpy array containing pre-exercise measurement data
    :param post_data: 2D Numpy array containing post-exercise measurement data
    """
    if pre_cols < post_cols:  # more post-exercise columns; add more noisy averaged pre-exercise columns
        temp_pre_data = np.zeros(
            shape=(post_rows, post_cols))  # declare empty array with proper dimensions (more columns)
        col_avg = pre_data.mean(axis=1)  # get column average

        for i, col in enumerate(pre_data.T):  # fill expanded array's first columns with existing pre-exercise data
            temp_pre_data[:, i] = col
        for j in range(pre_cols, post_cols):
            temp_pre_data[:, j] = col_avg + 0.1 * np.random.uniform(-np.abs(col_avg), abs(
                col_avg))  # add a noisy average of original columns. adds in range of \pm 10 percent of each data point
        pre_data = temp_pre_data  # overwrite old data with correctly sized array

    elif pre_cols > post_cols:  # more pre-exercise columns; add more noisy averaged post-exercise columns

        temp_post_data = np.zeros(
            shape=(pre_rows, pre_cols))  # declare empty array with proper dimensions (more columns)
        col_avg = post_data.mean(axis=1)  # get column average

        for i, col in enumerate(post_data.T):  # fill expanded array's first columns with existing post-exercise data
            temp_post_data[:, i] = col
        for j in range(post_cols, pre_cols):
            temp_post_data[:, j] = col_avg + 0.1 * np.random.uniform(-np.abs(col_avg), abs(
                col_avg))  # add a noisy average of original columns. adds in range of \pm 10 percent of each data point

        post_data = temp_post_data  # overwrite old data with correctly sized array

    return pre_data, post_data


def increase_cols(pre_data, post_data, pre_rows, pre_cols, post_rows, post_cols):
    """
    Extra columns are found by taking the average of the existing columns, 
    and then adding noise to each datapoint; the noise size is in 
    the interval of +/- 10 percent of each data point's absolute value.

    """
    tmp_pre_data = np.zeros(shape=(post_rows, 5))  # declare empty array with 5 columns
    col_avg = pre_data.mean(axis=1)  # get column average
    for i, col in enumerate(pre_data.T):  # fill expanded array's first columns with existing pre-exercise data
        tmp_pre_data[:, i] = col
    for j in range(pre_cols, post_cols):
        tmp_pre_data[:, j] = col_avg + 0.1 * np.random.uniform(-np.abs(col_avg), abs(
            col_avg))  # add a noisy average of original columns. adds in range of \pm 10 percent of each data point
    pre_data = tmp_pre_data # overwrite old data with correctly sized array

    tmp_post_data = np.zeros(shape=(pre_rows, 5))  # declare empty array with 5 columns
    col_avg = post_data.mean(axis=1)  # get column average
    for i, col in enumerate(post_data.T):  # fill expanded array's first columns with existing post-exercise data
        tmp_post_data[:, i] = col
    for j in range(post_cols, pre_cols):
        tmp_post_data[:, j] = col_avg + 0.1 * np.random.uniform(-np.abs(col_avg), abs(
            col_avg))  # add a noisy average of original columns. adds in range of \pm 10 percent of each data point
    post_data = tmp_post_data  # overwrite old data with correctly sized array

    return pre_data, post_data
