import pandas as pd
import numpy as np
import spm1d
from pathlib import Path
import os
import traceback

import plotting
import shape_accomodation
import utilities
import constants

"""
A collection of functions for performing SPM analysis of pre-exercise
and post-exercise 1D biomechanical time series data.
"""

def get_spm_t(pre_data, post_data):
    """
    Returns the spm.t object resulting from an SMP t test between the inputted pre and post-exercise data
    :param pre_data: 2D Numpy array containing pre_exercise data
    :param post_data: 2D Numpy array containing post_exercise data
    """
    try:
        t = spm1d.stats.ttest2(post_data.T, pre_data.T, equal_var=False)
        return t
    except Exception as e:
        print("Error performing SPM analysis: " + str(e))
        return None


def get_spm_ti(pre_data, post_data):
    """
    Returns the spm.t and spm.ti objects resulting from an SMP t test between the inputted pre and post-exercise data
    :param pre_data: 2D Numpy array containing pre_exercise data
    :param post_data: 2D Numpy array containing post_exercise data
    """
    try:
        t = spm1d.stats.ttest2(post_data.T, pre_data.T, equal_var=False)
        ti = t.inference(alpha=0.05, two_tailed=False, interp=True)
        return t, ti
    except Exception as e:
        print("Error performing SPM analysis: " + str(e))
        return None

def get_TI_df_header(clusters):
    """
    Creates an array of strings of the form 
    ["Cluster 1", "Cluster 2", ...]
    to be used as the header for a Pandas dataframe associated with the 
    characteristic parameters describing an SPM TI inference object.

    Parameters
    ----------
    clusters : ?
        A (list?) of SPM-related objects representing regions in which
        an SPM t-statistic exceeds the SPM threshold value (zstar).
    
    """
    header = []
    for c in range(len(clusters)):
        header.append("Cluster {}".format(c + 1)) 
    return header

def get_spm_cluster_params(cluster, alpha, threshold):
    """
    A cluster represents a region of a 1D SPM t-statistic curve above
    the SPM significance threshold region.

    Returns, in the following order, a 1D list of the following
    parameters associated with the inputted SPM cluster object.
    ["alpha",
     "threshold",
     "p value",
     "Significance start time [ms]",
     "Significance end time [ms]",
     "Centroid time [ms]",
     "Centroid t-value",
     "Maximum",
     "Area above threshold",
     "Area above x axis"]

    """
    # Start and end time of each cluster
    tstart, tend = cluster.endpoints  

    # 1D Numpy arrays holding the times and SPM t statistic values
    # for the current cluster.
    cluster_time = cluster._X
    cluster_spm_t = cluster._Z

    # Max value of t-statistic in the current cluster
    spm_t_max = np.max(cluster_spm_t)  

    # Number of SPM t-statisic points in the current cluster
    N = len(cluster_time)  

    # Compute area between SPM curve and the x axis
    # using the trapezoidal rule formula.
    A_above_x = 0.0
    for n in range(1, N, 1):
        A_above_x += np.abs(0.5*(cluster_spm_t[n] + cluster_spm_t[n-1]))*(cluster_time[n] - cluster_time[n-1])

    # Compute area between SPM curve and SPM threshold by subtracting
    # off the area between SPM threshold and the x axis
    A_above_threshold = A_above_x - (threshold * (cluster_time[-1] - cluster_time[0]))

    return [alpha,
            threshold,
            cluster.P,
            tstart,
            tend,
            cluster.centroid[0],
            cluster.centroid[1],
            spm_t_max,
            A_above_threshold,
            A_above_x]

def get_ti_parameters_as_df(ti):
    """
    Returns a TI object's parameters as a Pandas dataframe

    Parameters
    ----------
    ti : SPM TI inference object
        An SPM TI inference object generated from a comparison
        of pre-exercise and post-exercise data.

    """
    # Clusters are portions of SPM t curve above threshold value
    clusters = ti.clusters  

    if clusters is None:
        print("Significance threshold not exceeded. Returning None.")
        return None

    alpha = ti.alpha
    threshold = ti.zstar

    headers = get_TI_df_header(clusters)
    spm_param_names = constants.SPM_PARAM_NAMES
    num_clusters = len(clusters)
    spm_param_values = np.zeros([len(spm_param_names), num_clusters])

    # Loop through significance clusters
    for c, cluster in enumerate(clusters):  
        cluster_params = get_spm_cluster_params(cluster, alpha, threshold)
        spm_param_values[:, c] = cluster_params

    # Convert Numpy array of SPM parameters to a Pandas dataframes,
    # which is in principle bloated but convenient later on
    # when including headers and row names when writing CSV files.
    return pd.DataFrame(spm_param_values, 
            index=spm_param_names, columns=headers)

def multi_set_spm_analysis(parent_dir, file_basename, sets_to_convert):
    """
    Import full path to a directory containing pre and post-exercise 
    CSV files for each set of a TMG measurement for a SINGLE athlete
    The files should be named in the form
        EM1234-pre-1.csv   # pre-exericse, set 1
        EM1234-pre-2.csv   # pre-exericse, set 2
        EM1234-pre-3.csv   # pre-exericse, set 3
        EM1234-post-1.csv  # post-exercise, set 1
        EM1234-post-2.csv  # post-exercise, set 2
        EM1234-post-3.csv  # post-exercise, set 3

    Exports csv file of spm parameters (e.g. threshold, centroid time, etc...)
    for each set's pre/post-exercise file pair.
    Exports a png graph of original measurement and spm t-statistic plot for each set's pre/post-exercise file pair

    :param parent_dir: full path to a directory containing data files
    :param file_basename: data file basename e.g. "EM1234" for above example
    :param sets_to_convert: list of the set numbers of convert e.g. [1, 2, 3]
    """
    start_row = 1  # csv data file row at which to begin reading data (0-indexed)
    max_rows = 100  # number of rows to read after start_row is reached

    for set_num in sets_to_convert:
        pre_filename = parent_dir + file_basename + "-pre-{}.csv".format(set_num)
        post_filename = parent_dir + file_basename + "-post-{}.csv".format(set_num)

        params_output_path = parent_dir + file_basename + "-set{}-params.csv".format(set_num)
        figure_output_path = parent_dir + file_basename + "-set{}.png".format(set_num)
        pre_data = np.loadtxt(pre_filename, delimiter=",", skiprows=start_row, max_rows=max_rows)  # load data
        post_data = np.loadtxt(post_filename, delimiter=",", skiprows=start_row, max_rows=max_rows)  # load data
        pre_data, post_data = shape_accomodation.fix_false_spm_significance(pre_data, post_data)

        t, ti = get_spm_ti(pre_data, post_data)
        export_ti_parameters(ti, time_offset=start_row,
                pre_filename=pre_filename,
                post_filename=post_filename,
                output_file=params_output_path)
        plotting.plot_spm_ttest(t, ti, pre_data, post_data,
                figure_output_path, time_offset=start_row, show_plot=False)


def all_set_spm_analysis(data_dir, base_filenames):
    """
    Input full path to a directory containing pre and post-exercise
    CSV files for TMG measurements of MULTIPLE athletes.
    The files should be named in the form
        EM1234-pre.csv   # pre-exercise, first athlete
        EM1234-post.csv  # post-exercise, first athlete
        SD1234-pre.csv   # pre-exercise, second athlete
        SD1234-post.csv  # post-exercise, second athlete
        JZ1234-pre.csv   # pre-exercise, third athlete
        JZ1234-post.csv  # post-exercise, third athlete
        etc...

    Input a list of "base" filenames for each athlete of the form e.g. ["EM1234", "SD1234", "JZ1234"]

    Exports csv file of spm parameters (e.g. threshold, centroid time, etc...)
    for each athlete's pre/post-exercise file pair.
    Exports a png graph of original measurement and spm t-statistic plot 
    for each athlete's pre/post-exercise file pair.

    :param data_dir: full path to a directory containing data files
    :param base_filenames: list of the set numbers of convert e.g. [1, 2, 3]
    """
    start_row = 1  # csv data file row at which to begin reading data (0-indexed)
    # TODO: move to a constants file
    max_rows = 100  # number of rows to read after start_row is reached

    param_output_dir = utilities.make_output_dir(data_dir + "params-spm-csv")
    fig_output_dir = utilities.make_output_dir(data_dir + "spm-figures")

    for file_basename in base_filenames:
        print(file_basename)
        pre_filename = data_dir + file_basename + "-pre.csv"
        post_filename = data_dir + file_basename + "-post.csv"

        params_output_path = param_output_dir + file_basename + "-spm-params.csv"
        figure_output_path = fig_output_dir + file_basename + "-spm-figure.png"
        pre_data = np.loadtxt(pre_filename, delimiter=",", skiprows=start_row, max_rows=max_rows)  # load data
        post_data = np.loadtxt(post_filename, delimiter=",", skiprows=start_row, max_rows=max_rows)  # load data
        pre_data, post_data = shape_accomodation.fix_false_spm_significance(pre_data, post_data)

        t, ti = get_spm_ti(pre_data, post_data)
        export_ti_parameters(ti, time_offset=start_row,
                pre_filename=pre_filename,
                post_filename=post_filename,
                output_file=params_output_path)
        plotting.plot_spm_ttest(t, ti, pre_data, post_data,
                figure_output_path, time_offset=start_row,
                show_plot=False, save_figures=True)


def multi_set_spm_analysis_wrapper():
    """
    Wrapper method for performing SPM analysis on the following file structure:

    Input path to parent directory, containing subdirectories
    for a SINGLE athelte named in the standard TMG-form e.g. "EM1234".
    Each sub-directory should contain pre and post-exercise CSV files
    for each set of a TMG measurement for this SINGLE athlete.
    The files should be named in the form
        EM1234-pre-1.csv   # pre-exercise, set 1
        EM1234-pre-2.csv   # pre-exercise, set 2
        EM1234-pre-3.csv
        EM1234-post-1.csv    # post-exercise, set 1
        EM1234-post-2.csv    # post-exercise, set 2
        EM1234-post-3.csv

    Input list of sets to convert for each individual athlete.
    Calls multi_set_spm_analysis(...) for each individual athlete,
    which exports csv file of SPM params and a png file of SPM graphs.

    """
    parent_dir = "/Users/ejmastnak/Documents/Media/tmg-bmc-media/measurements/analysis-spm-potenciacija-19-03-2021/"
    sub_dirs = ["MM20210319105636_1/", "EP20210319102018/", "MM20210319115856/", "NF20210319122049/", "NF20210319113716/", "ZI20210319123747/"]
    sets_to_convert = [list(range(2, 8)), list(range(1, 9)), list(range(1, 5)), list(range(1, 5)), list(range(1, 6)), list(range(1, 6))]

    for i, dir in enumerate(sub_dirs):
        print(dir)
        file_basename = dir[0:-1]  # drop backslash
        multi_set_spm_analysis(parent_dir + dir, file_basename, sets_to_convert[i])
        print()


def all_set_spm_analysis_wrapper():
    """
    Wrapper method for performing SPM analysis on the following file structure:

    Input full path to a directory containing pre and post-exercise
    CSV files for TMG measurements of MULTIPLE athletes.
    The files should be named in the form
        EM1234-pre.csv   # pre-exercise, first athlete
        EM1234-post.csv  # post-exercise, first athlete
        SD1234-pre.csv   # pre-exercise, second athlete
        SD1234-post.csv  # post-exercise, second athlete
        JZ1234-pre.csv   # pre-exercise, third athlete
        JZ1234-post.csv  # post-exercise, third athlete
        etc...

    Input a list of "base" filenames for each athlete of the form e.g. ["EM1234", "SD1234", "JZ1234"]

    Calls all_set_spm_analysis(...) which exports CSV file of SPM params 
    and a png file of SPM graphs---see function documentation
    """
    base_filenames = ['1-BR20200910125909', '2-SZ20200901134322', '3-EM20200901124828', '4-SD20200901145937',
                      '5-SK20200901142319', '6-SD20200929090956', '7-SK20200929095140', '8-NF20200929102126',
                      '9-MM20200929105429', '10-MK20200929112805', '11-JJ20200929120454', '12-JZ20200924121704',
                      '13-ZI20200924091029', '14-VT20200924094806', '15-MK20200924102106', '16-LR20200924113647',
                      '17-LH20200924105451', '18-JL20200910100638', '19-MC20200910105450', '20-MS20200910112714',
                      '21-SR20200910121233', '22-VD20201009103409', '23-AL20201014125345', '24-ME20201104141336',
                      '25-IL20201104132459', '26-FD20201105113904', '27-MM20201021123025', '30-BB20210312101025',
                      '31-EM20210312111435', '32-JZ20210312131656', '33-SD20210312121833', '34-SK20210312114610',
                      '35-SR20210312124932', '36-SZ20210312103958', '37-AL20210317133110', '38-IF20210317130746',
                      '39-JL20210317121435', '40-MM20210317111914', '41-NF20210317114800', '42-NU20210317124142',
                      '43-VT20210317105103', '44-ZI20210317135522']

    data_dir = "/Users/ejmastnak/Documents/Media/tmg-bmc-media/project-potentiation-spm-rdd-2021/data-csv-BP-100ms-raw/"
    all_set_spm_analysis(data_dir, base_filenames)


if __name__ == "__main__":
    # set_file_analysis_wrapper()
    # per_set_analysis_wrapper()
    all_set_spm_analysis_wrapper()
