import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import spm1d

import utilities
import spm_analysis
import preprocessing
import plotting
import constants

plt.style.use('frontiers.mplstyle')

"""
Collection of functions intended specifically for use in preparing
the potentiation paper for the Frontiers journal.
"""
def analysis_by_athlete(pre_data_dir, post_data_dir, 
        spm_param_output_dir, spm_plot_output_dir,
        points_per_msmnt=100, max_sets=4, skiprows=2):
    """
    Performs SPM analysis of each athlete using raw (un-normalized) data. 
    Computes the following files for each athlete:
    - SPM parameters associated with a two-sample SPM t-test comparing
      the athlete's pre-exercise and post-exercise measurements.
    - 2-axis SPM plot showing mean and standard deviation of the athlete's
      pre-exercise and post-exercise measurements on axes 0 and the
      SPM t-statistic associated with their comparison on axes 1.

    Parameters
    ----------
    pre_data_dir : str
        Path to a directory containing pre-exercise biomechanical
        time series CSV data files for each measured athlete.
        Columns correspond to measurements and rows to data points.
    post_data_dir : str
        Post-exercise analog of `pre_data_dir`.
    max_sets : int
        The number of measurement sets to analyze for each athlete
        Each data file should contain at least `2*max_sets` columns.
    skiprows : int
        The number of initial rows to skip in data files. Used in practice
        to avoid header and first row, which is zero in all measurements.
    
    """
    pre_tensor, post_tensor = get_pre_and_post_exercise_data_tensors(pre_data_dir,
            post_data_dir, spm_param_output_dir, spm_plot_output_dir,
            points_per_msmnt=100, max_sets=4, skiprows=2)
    num_athletes = np.shape(pre_tensor)[2]

    # Perform SPM analysis on each athlete
    for a in range(num_athletes):
        pre_data = pre_tensor[:, :, a]
        post_data = post_tensor[:, :, a]
        pre_data, post_data = preprocessing.fix_false_spm_significance(pre_data, post_data)

        t, ti = spm_analysis.get_spm_ti(pre_data, post_data)

        spm_param_output_file = spm_param_output_dir + "subject{}-spm-params.csv".format(a + 1)

        param_df = spm_analysis.get_ti_parameters_as_df(ti)
        param_df.to_csv(spm_param_output_file)

        # (zero-based) first row of TMG data that is read from CSV files
        # In practice only zero-th row of TMG data is skipped.
        tmg_data_start_row = constants.TMG_DATA_START_ROW_FOR_SPM
        fig_format = "png"
        fig_dpi = 300

        spm_plot_output_file = spm_plot_output_dir + "subject{}-plot.{}".format(a + 1, fig_format)
        plotting.plot_spm_ttest(t, ti, pre_data, post_data,
                tmg_data_start_row, spm_plot_output_file,
                fig_format=fig_format, fig_dpi=fig_dpi,
                show_plot=False, save_figures=True)


def normalized_analysis_by_set(pre_data_dir, post_data_dir, 
        spm_param_output_dir, spm_plot_output_dir,
        points_per_msmnt=100, max_sets=4, skiprows=2):
    """
    Performs SPM analysis of each set using normalized data. 
    Computes the following files for each set:
    - SPM parameters associated with a two-sample SPM t-test comparing the
      set's pre-exercise and post-exercise measurements across all athlete's.
    - 2-axis SPM plot showing mean and standard deviation of the set's
      pre-exercise and post-exercise measurements on axes 0 and the
      SPM t-statistic associated with their comparison on axes 1.

    Parameters
    ----------
    pre_data_dir : str
        Path to a directory containing pre-exercise biomechanical
        time series CSV data files for each measured athlete.
        Columns correspond to measurements and rows to data points.
    post_data_dir : str
        Post-exercise analog of `pre_data_dir`.
    max_sets : int
        The number of measurement sets to analyze for each athlete
        Each data file should contain at least `2*max_sets` columns.
    skiprows : int
        The number of initial rows to skip in data files. Used in practice
        to avoid header and first row, which is zero in all measurements.
    
    """
    pre_tensor, post_tensor = get_pre_and_post_exercise_data_tensors(pre_data_dir,
            post_data_dir, spm_param_output_dir, spm_plot_output_dir,
            points_per_msmnt=100, max_sets=4, skiprows=2)
    num_athletes = np.shape(pre_tensor)[2]

    # Normalize each athlete's TMG signal in each set by dividing both 
    # pre and post-exercise signals by the maximum value in the given set 
    # of that athlete's pre and post-exercise measurement.
    # Due to potentiation, the maximum will generally occur in the post-exercise
    # measurement, but no a priori assumption of where the max occurs is made.
    norm_factors = np.zeros([max_sets, num_athletes])
    for a in range(num_athletes):
        for s in range(max_sets):
            tmg_pre = pre_tensor[:, s, a]
            tmg_post = post_tensor[:, s, a]
            tmg_max = np.max(np.concatenate([tmg_pre, tmg_post]))
            norm_factors[s, a] = tmg_max

    # Create normalized analogs of `pre_tensor` and `post_tensor`.
    # Numpy broadcasting is used to produce element-wise division by each 
    # measurement maximum along the measurement axis for each athlete and set.
    pre_tensor_normed = pre_tensor/norm_factors
    post_tensor_normed = post_tensor/norm_factors

    # Perform SPM analysis on each set of normalized measurements
    for s in range(max_sets):
        pre_data = pre_tensor_normed[:, s, :]
        post_data = post_tensor_normed[:, s, :]

        np.savetxt("/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm_normed/pre-exercise/{}.csv".format(s+1), pre_data, delimiter=',')
        np.savetxt("/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm_normed/post-exercise/{}.csv".format(s+1), post_data, delimiter=',')

        pre_data, post_data = preprocessing.fix_false_spm_significance(pre_data, post_data)

        t, ti = spm_analysis.get_spm_ti(pre_data, post_data)

        spm_param_output_file = spm_param_output_dir + "set{}-params.csv".format(s + 1)

        param_df = spm_analysis.get_ti_parameters_as_df(ti)
        param_df.to_csv(spm_param_output_file)

        # plot_spm_ttest(t, ti, pre_data, post_data, figure_output_path, 
        # show_plot=True, save_figures=False):

        # (zero-based) first row of TMG data that is read from CSV files
        # In practice only zero-th row is skipped.
        tmg_data_start_row = constants.TMG_DATA_START_ROW_FOR_SPM
        fig_format = "png"
        fig_dpi = 300

        spm_plot_output_file = spm_plot_output_dir + "set{}-plot.{}".format(s + 1, fig_format)
        plotting.plot_spm_ttest(t, ti, pre_data, post_data,
                tmg_data_start_row, spm_plot_output_file,
                fig_format=fig_format, fig_dpi=fig_dpi,
                show_plot=False, save_figures=True)


def tmp_srdjan_set_analysis(pre_data_dir, post_data_dir, 
        spm_param_output_dir, spm_plot_output_dir,
        points_per_msmnt=100, max_sets=4, skiprows=1):
    """
    For temporary analysis of normalized CSV files sent by Srdjan 
    for which I am uncertain how the normalization was performed.
    Output analogous to `normalized_analysis_by_set`:

    """

    # Perform SPM analysis on each set of normalized measurements
    for s in range(max_sets):
        pre_data = np.loadtxt(pre_data_dir + "{}.csv".format(s + 1), delimiter=',',
                    skiprows=skiprows, max_rows=points_per_msmnt)
        post_data = np.loadtxt(post_data_dir + "{}.csv".format(s + 1), delimiter=',',
                    skiprows=skiprows, max_rows=points_per_msmnt)
        pre_data, post_data = preprocessing.fix_false_spm_significance(pre_data, post_data)

        t, ti = spm_analysis.get_spm_ti(pre_data, post_data)

        spm_param_output_file = spm_param_output_dir + "set{}-params.csv".format(s + 1)

        param_df = spm_analysis.get_ti_parameters_as_df(ti)
        param_df.to_csv(spm_param_output_file)

        # (zero-based) first row of TMG data that is read from CSV files
        # In practice only zero-th row is skipped.
        tmg_data_start_row = constants.TMG_DATA_START_ROW_FOR_SPM
        fig_format = "jpg"
        fig_dpi = 500

        spm_plot_output_file = spm_plot_output_dir + "spm-set{}.{}".format(s + 1, fig_format)
        plotting.plot_spm_ttest(t, ti, pre_data, post_data,
                tmg_data_start_row, spm_plot_output_file,
                fig_format=fig_format, fig_dpi=fig_dpi,
                show_plot=False, save_figures=True)


def tmp_make_spm_plot_for_article(pre_data_dir, post_data_dir, 
        points_per_msmnt=100, max_sets=4, skiprows=1,
        save_figure=True, show_plot=False):
    """
    Function used for the sole purpose of a generating a 4-axis plot showing
    SPM results for sets 1, 2, 3, and 4 for use in the Frontiers article.

    Currently uses normalized CSV files sent by Srdjan 
    for which I am uncertain how the normalization was performed.
    """
    fig, axes = plt.subplots(max_sets, 2, figsize=(6.8, 8))
    tmg_data_start_row = constants.TMG_DATA_START_ROW_FOR_SPM
    output_dir = "/home/ej/Documents/projects/tmg-bmc/frontiers-2022/article/figures/"
    output_file = output_dir + "spm-plot.jpg"

    subfib_labels = ["(1)", "(2)", "(3)", "(4)"]

    fig_dpi = 500

    pre_color = plotting.pre_color
    post_color = plotting.post_color
    post_color2 = plotting.post_color2
    pre_alpha = plotting.pre_alpha
    post_alpha = plotting.post_alpha

    tline_color = plotting.tline_color
    tfill_color = plotting.tfill_color
    tfill_color2 = plotting.tfill_color2

    linewidth = 1.5

    # Perform SPM analysis on each set of normalized measurements
    for s in range(max_sets):
        pre_data = np.loadtxt(pre_data_dir + "{}.csv".format(s + 1), delimiter=',',
                    skiprows=skiprows, max_rows=points_per_msmnt)
        post_data = np.loadtxt(post_data_dir + "{}.csv".format(s + 1), delimiter=',',
                    skiprows=skiprows, max_rows=points_per_msmnt)
        pre_data, post_data = preprocessing.fix_false_spm_significance(pre_data, post_data)
        t, ti = spm_analysis.get_spm_ti(pre_data, post_data)

        # BEGIN PLOTTING
        # --------------------------------------------- #
        N = np.shape(post_data)[0]       # number of rows in pre/post_data
        time = np.linspace(0, N - 1, N)  # [ms] assuming 1 kHz sampling

        post_mean = np.mean(post_data, axis=1)
        pre_mean = np.mean(pre_data, axis=1)
        post_sd = np.std(post_data, ddof=1, axis=1)
        pre_sd = np.std(pre_data, ddof=1, axis=1)

        # Plot TMG measurement
        # --------------------------------------------- #
        ax = axes[s, 0]
        plotting.remove_spines(ax)

        # Only put x label on bottom axis to save vertical space
        if s == max_sets - 1:  
            ax.set_xlabel("Time [ms]")
        ax.set_ylabel("Normalized displacement")

        # Mean value of time-series measurements
        ax.plot(time, pre_mean, color=pre_color, linewidth=linewidth, 
                label="Pre-ISQ mean", zorder=4)
        ax.plot(time, post_mean, color=post_color, linewidth=linewidth,
                label="Post-ISQ mean", zorder=3)

        # Standard deviation clouds
        ax.fill_between(time, post_mean - post_sd, post_mean + post_sd, 
                color=post_color, alpha=post_alpha, zorder=2)
        ax.fill_between(time, pre_mean - pre_sd, pre_mean + pre_sd,
                color=pre_color, alpha=pre_alpha, zorder=1)

        ax.text(-0.30, 0.5, subfib_labels[s], transform=ax.transAxes, fontsize=12)
        ax.legend(framealpha=1.0)
        # --------------------------------------------- #

        # Plot SPM results
        # --------------------------------------------- #
        ax = axes[s, 1]
        plotting.remove_spines(ax)

        # Only put x label on bottom axis to save vertical space
        if s == max_sets - 1:  
            ax.set_xlabel("Time [ms]")
        ax.set_ylabel("SPM $t$-statistic", labelpad=-0.1)

        ax.set_ylim(-7, 10)
        y_ticks = [-5, 0, 5, 10]
        y_tick_lables = ["-5", "0", "5", "10"]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_tick_lables)

        # Plot SPM t-statistic
        ax.plot(time, t.z, color=tline_color)  # plot t-curve

        # Plot dashed line at y = 0
        ax.axhline(y=0, color='black', linestyle=':')  

        # Plot dashed line at SPM significance threshold
        ax.axhline(y=ti.zstar, color='#000000', linestyle='--')

        # Text box showing alpha, threshold value, and p value
        ax.text(73, ti.zstar + 1.0, plotting.get_annotation_text(ti),
                va='bottom', ha='left', 
                bbox=dict(facecolor='#FFFFFF', edgecolor='#222222', boxstyle='round,pad=0.3'))

        # Shade between curve and threshold
        ax.fill_between(time, t.z, ti.zstar, where=t.z >= ti.zstar,
                interpolate=True, color=tfill_color)

    plt.tight_layout()

    if save_figure:
        plt.savefig(output_file, dpi=fig_dpi, bbox_inches='tight', pad_inches = 0)

    if show_plot:
        plt.show()


def get_pre_and_post_exercise_data_tensors(pre_data_dir, post_data_dir,
        spm_param_output_dir, spm_plot_output_dir,
        points_per_msmnt=100, max_sets=4, skiprows=2):
    """
    Used to pack pre and post-exercise measurement data into two 3D Numpy
    arrays in which:
    - Axis 0 corresponds to time series data points
    - Axis 1 corresponds to sets
    - Axis 2 corresponds to subjects

    Motivation for this function: avoid repeating the code used in both 
    the functions `normalized_analysis_by_set` and `analysis_by_athlete`.

    Parameters
    ----------
    All parameters play identical roles to their roles in the functions
    `normalized_analysis_by_set` and `analysis_by_athlete`.

    Returns
    -------
    pre_tensor : ndarray
        3D Numpy array holding pre-exercise data (see description above).
    post_tensor : ndarray
        3D Numpy array holding post-exercise data.
    
    """
    # Safety check that number of pre and post-exercise files match
    num_pre_files = 0
    num_post_files = 0
    for filename in utilities.natural_sort(os.listdir(pre_data_dir)):
        if os.path.isfile(pre_data_dir + filename) and filename.endswith("-pre.csv"):
            num_pre_files += 1
    for filename in utilities.natural_sort(os.listdir(post_data_dir)):
        if os.path.isfile(post_data_dir + filename) and filename.endswith("-post.csv"):
            num_post_files += 1

    if num_pre_files != num_post_files:
        print("Error: number of pre and post-exercise files do not match! Exiting.")
        return (None, None)
    else: 
        num_athletes = num_pre_files

    # 3D Numpy arrays for hold pre and post exercise measurement data
    pre_tensor = np.zeros([points_per_msmnt, max_sets, num_athletes])
    post_tensor = np.zeros([points_per_msmnt, max_sets, num_athletes])

    # Loop through pre-exercise data files and populate `pre_tensor`
    athlete_index = 0
    for filename in utilities.natural_sort(os.listdir(pre_data_dir)):
        if os.path.isfile(pre_data_dir + filename) and filename.endswith("-pre.csv"):
            athlete_data = np.loadtxt(pre_data_dir+filename, delimiter=',',
                    skiprows=skiprows, max_rows=points_per_msmnt)
            pre_tensor[:, :, athlete_index] = athlete_data
            athlete_index += 1

    # Loop through post-exercise data files and populate `post_tensor`
    athlete_index = 0
    for filename in utilities.natural_sort(os.listdir(post_data_dir)):
        if os.path.isfile(post_data_dir + filename) and filename.endswith("-post.csv"):
            athlete_data = np.loadtxt(post_data_dir+filename, delimiter=',',
                    skiprows=skiprows, max_rows=points_per_msmnt)
            post_tensor[:, :, athlete_index] = athlete_data
            athlete_index += 1

    return (pre_tensor, post_tensor)


def athlete_analysis_wrapper():
    """
    Wrapper function for performing SPM analysis
    of each athlete with `analysis_by_athlete`.
    """
    pre_data_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm/pre-exercise/"
    post_data_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm/post-exercise/"

    spm_param_output_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/output/spm-params-by-subject/"
    spm_plot_output_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/output/spm-plots-by-subject/"

    points_per_msmnt = 100
    max_sets = 4
    skiprows = 2

    analysis_by_athlete(pre_data_dir, post_data_dir,
            spm_param_output_dir, spm_plot_output_dir,
            points_per_msmnt=points_per_msmnt,
            max_sets=max_sets, skiprows=2)


def set_analysis_wrapper():
    """
    Wrapper function for performing SPM analysis
    of each athlete using `normalized_analysis_by_set`.
    """
    pre_data_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm/pre-exercise/"
    post_data_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm/post-exercise/"

    spm_param_output_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/output/spm-params-by-set/"
    spm_plot_output_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/output/spm-plots-by-set/"

    points_per_msmnt = 100
    max_sets = 4
    skiprows = 2

    normalized_analysis_by_set(pre_data_dir, post_data_dir, 
            spm_param_output_dir, spm_plot_output_dir,
            points_per_msmnt=points_per_msmnt,
            max_sets=max_sets, skiprows=2)


def tmp_srdjan_set_analysis_wrapper():
    """
    Wrapper function for performing SPM analysis
    of each data sent by Srdjan with `normalized_analysis_by_set`.
    """
    pre_data_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/sent/pre/"
    post_data_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/sent/post/"

    spm_param_output_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/output/tmp-srdjan-normalized/spm-params-by-set/"
    spm_plot_output_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/output/tmp-srdjan-normalized/spm-plots-by-set/"

    points_per_msmnt = 100
    max_sets = 4
    skiprows = 1

    
    # Generate SPM params and plots for each set
    # tmp_srdjan_set_analysis(pre_data_dir, post_data_dir, 
    #         spm_param_output_dir, spm_plot_output_dir,
    #         points_per_msmnt=points_per_msmnt,
    #         max_sets=max_sets, skiprows=2)

    # Generate one figure holding SPM plots for all sets
    tmp_make_spm_plot_for_article(pre_data_dir, post_data_dir, 
            points_per_msmnt=points_per_msmnt,
            max_sets=max_sets, skiprows=2, show_plot=True)


def practice():
    a = np.array([1,2,3])
    b = np.array([4,5,6])
    c = np.concatenate([a,b])
    print(a)
    print(b)
    print(c)

if __name__ == "__main__":
    # practice()
    # athlete_analysis_wrapper()
    # athlete_test()
    # set_analysis_wrapper()
    tmp_srdjan_set_analysis_wrapper()
