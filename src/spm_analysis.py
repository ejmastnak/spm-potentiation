""" 
This script performs SPM analysis of TMG data.
Input data: the per-subject TMG measurement files in `/data/csv-for-spm-normed/`

"""
import os
import numpy as np
import pandas as pd
import spm1d
import constants, frontiers_utils, plotting

# SPM paired t-test by subject
def perform_spm_tests_by_subjects():
    """
    For each subject:
    - Performs an SPM paired t-test comparing preprocessed pre-ISQ and post-ISQ
      TMG signals across all sets and saves the resulting SPM plots.
    - Queries from `spm1d` or directly computes discrete parameters 
      summarizing the above-described SPM paired t-test.

    Input data: the per-subject measurement files in `constants.SPM_DATA_DIR`
    Output data: 
        - Per-set CSV files in `/output/spm-params-by-set/`
          summarizing the results of the above-described statisical analysis.
        - Per-set JPG files storing a two-axis (one row, two column)
          graph the set's above-described SPM t-test and showing:
          - Axis 0: Mean normalized pre-ISQ and post-ISQ TMG signal across 
            all subjects, with standard deviation clouds, with respect to time.
          - Axis 1: SPM t-continuum with respect to time with threshold 
            and significance clusters emphasized.

    """ 
    pre_input_dir = constants.SPM_DATA_DIR + "pre-exercise/"
    post_input_dir = constants.SPM_DATA_DIR + "post-exercise/"
    pre_filenames = []
    post_filenames = []

    for filename in frontiers_utils.natural_sort(os.listdir(pre_input_dir)):
        pre_filenames.append(filename)
    for filename in frontiers_utils.natural_sort(os.listdir(post_input_dir)):
        post_filenames.append(filename)

    param_output_dir = constants.SPM_PARAMS_BY_SUBJECT_DIR
    plot_output_dir = constants.SPM_PLOTS_BY_SUBJECT_DIR
    fig_dpi = 300
    fig_format = "jpg"

    for i in range(len(pre_filenames)):
        param_output_file = param_output_dir + pre_filenames[i].replace("-pre.csv", "-spm-params.csv")
        plot_output_file = plot_output_dir + pre_filenames[i].replace("-pre.csv", "-spm-plot.jpg")

        pre_data = np.loadtxt(pre_input_dir + pre_filenames[i],
                delimiter=',', skiprows=1)  # skip header row
        post_data = np.loadtxt(post_input_dir + post_filenames[i],
                delimiter=',', skiprows=1)  # skip header row

        t, ti = _get_spm_ti(pre_data, post_data)
        
        # Compute SPM parameters and save as CSV
        param_df = _get_ti_parameters_as_df(ti,
                time_offset=constants.TMG_ROWS_TO_SKIP_FOR_SPM)
        param_df.to_csv(param_output_file)

        # Plot
        plotting.plot_spm_ttest(t, ti, pre_data, post_data,
                constants.TMG_ROWS_TO_SKIP_FOR_SPM,
                plot_output_file,
                fig_format=fig_format, fig_dpi=fig_dpi,
                tmg_y_axis_label="Displacement [mm]",
                show_plot=False, save_figures=True)

# SPM paired t-test by set
def perform_spm_tests_by_set():
    """
    For each measurement set:
    - Performs an SPM paired t-test comparing preprocessed pre-ISQ and post-ISQ
      TMG signals across all subjects and saves the resulting SPM plots.
    - Queries from `spm1d` or directly computes discrete parameters 
      summarizing the above-described SPM paired t-test.

    Input data: the normalized per-subject measurement files in `constants.NORMED_SPM_DATA_DIR`
    Output data: 
        - Per-set CSV files in `/output/spm-params-by-set/`
          summarizing the results of the above-described statisical analysis.
        - Per-set JPG files storing a two-axis (one row, two column)
          graph the set's above-described SPM t-test and showing:
          - Axis 0: Mean normalized pre-ISQ and post-ISQ TMG signal across 
            all subjects, with standard deviation clouds, with respect to time.
          - Axis 1: SPM t-continuum with respect to time with threshold 
            and significance clusters emphasized.

    """
    pre_input_dir = constants.NORMED_SPM_DATA_DIR + "pre-exercise/"
    post_input_dir = constants.NORMED_SPM_DATA_DIR + "post-exercise/"

    param_output_dir = constants.SPM_PARAMS_BY_SET_DIR
    plot_output_dir = constants.SPM_PLOTS_BY_SET_DIR
    fig_dpi = 300
    fig_format = "jpg"

    sets_per_measurement_file = 4
    rows_per_measurement_file = constants.TMG_ROWS_TO_USE_FOR_SPM - constants.TMG_ROWS_TO_SKIP_FOR_SPM
    subjects_in_database = 55

    # 3D Numpy tensor to hold all pre-exercise measurements in database
    pre_tensor = np.zeros([rows_per_measurement_file,
        sets_per_measurement_file,
        subjects_in_database])

    # 3D Numpy tensor to hold all post-exercise measurements in database
    post_tensor = np.zeros([rows_per_measurement_file,
        sets_per_measurement_file,
        subjects_in_database])

    # Load pre-exercise measurements into memory
    for i, filename in enumerate(frontiers_utils.natural_sort(os.listdir(pre_input_dir))):
        data = np.loadtxt(pre_input_dir + filename, delimiter=',', skiprows=1)
        pre_tensor[:, :, i] = data

    # Load post-exercise measurements into memory
    for i, filename in enumerate(frontiers_utils.natural_sort(os.listdir(post_input_dir))):
        data = np.loadtxt(post_input_dir + filename, delimiter=',', skiprows=1)
        post_tensor[:, :, i] = data

    # Perform SPM analysis for each set
    for s in range(sets_per_measurement_file):
        param_output_file = param_output_dir + "set-{}-params.csv".format(s + 1)
        plot_output_file = plot_output_dir + "set-{}-plot.jpg".format(s + 1)

        pre_data = pre_tensor[:, s, :]
        post_data = post_tensor[:, s, :]

        t, ti = _get_spm_ti(pre_data, post_data)
        
        # Compute SPM parameters and save as CSV
        param_df = _get_ti_parameters_as_df(ti,
                time_offset=constants.TMG_ROWS_TO_SKIP_FOR_SPM)
        param_df.to_csv(param_output_file)

        # Plot
        plotting.plot_spm_ttest(t, ti, pre_data, post_data,
                constants.TMG_ROWS_TO_SKIP_FOR_SPM,
                plot_output_file,
                fig_format=fig_format, fig_dpi=fig_dpi,
                tmg_y_axis_label="Normalized displacement",
                show_plot=False, save_figures=True)


# ---------------------------------------------------------------------- #
# Functions below this line are not meant to be called outside this script
# ---------------------------------------------------------------------- #
def _get_spm_ti(pre_data, post_data):
    """
    Returns the spm.t and spm.ti objects resulting from an SMP 
    two-sample t-test between the inputted pre- and post-exercise data.

    Parameters
    ----------
    pre_data : ndarray
        2D Numpy array containing pre-exercise TMG measurements.
        Rows should correspond to time and columns to measurements.
    post_data : ndarray
        2D Numpy array containing post-exercise TMG measurements
        Rows should correspond to time and columns to measurements.
    
    """
    try:
        t = spm1d.stats.ttest2(post_data.T, pre_data.T, equal_var=False)
        ti = t.inference(alpha=0.05, two_tailed=False, interp=True)
        return t, ti
    except Exception as e:
        print("Error performing SPM analysis: " + str(e))
        return None, None


def _get_ti_parameters_as_df(ti,
        time_offset=constants.TMG_ROWS_TO_SKIP_FOR_SPM):
    """
    Returns a TI object's parameters as a Pandas DataFrame, which is
    then used to easily save the parameters to a CSV file.

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

    # Creates an array of strings of the form ["Cluster 1", "Cluster 2", ...]
    header = []
    for c in range(len(clusters)):
        header.append("Cluster {}".format(c + 1)) 

    spm_param_names = constants.SPM_PARAM_NAMES
    num_clusters = len(clusters)
    spm_param_values = np.zeros([len(spm_param_names), num_clusters])

    # Loop through significance clusters
    for c, cluster in enumerate(clusters):  
        cluster_params = _get_params_of_spm_cluster(cluster, alpha, threshold,
                time_offset=time_offset)
        spm_param_values[:, c] = cluster_params

    # Convert Numpy array of SPM parameters to a Pandas dataframes,
    # which is in principle bloated but convenient later on
    # when including headers and row names when writing CSV files.
    return pd.DataFrame(spm_param_values, 
            index=spm_param_names, columns=header)


def _get_params_of_spm_cluster(cluster, alpha, threshold,
        time_offset=constants.TMG_ROWS_TO_SKIP_FOR_SPM):
    """
    A cluster represents a region of a 1D SPM t-statistic curve 
    above the SPM significance threshold region.

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
    tstart += time_offset
    tend += time_offset

    # 1D Numpy arrays holding the grid of times and corresponding
    # SPM t-statistic values for the current cluster.
    cluster_time = cluster._X
    cluster_time += time_offset
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
            cluster.centroid[0] + time_offset,
            cluster.centroid[1],
            spm_t_max,
            A_above_threshold,
            A_above_x]

if __name__ == "__main__":
    # perform_spm_tests_by_subjects()
    perform_spm_tests_by_set()
