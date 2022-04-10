import os
import numpy as np
import matplotlib.pyplot as plt
import tmg_biomechanics.tmg_params as tmg_params
import plotting, constants, frontiers_utils, spm_analysis
"""
A set of functions used to create the LaTeX tables and figures that appear 
in the journal article; in this sense, this script represents the final 
step in this project's analysis pipeline.
"""

def make_tmg_param_table(staggered=False):
    """
    Creates a single LaTeX table that, for each measurement set,
    compares pre- and post-exercise values of each TMG parameter.

    Columns: Set number (1, 2, 3, and 4)
    Rows: The following TMG param values:
          - Dm [mm]
          - Td [ms]
          - Tc [ms]
          - RDDMax [mm/ms]
          - RDDMaxTime [ms]

    Input data: The `setX-tmg-stats.csv` values stored in
                `constants.TMG_PARAMS_BY_SET_DIR`
                Assumes TMG params in CSV file appear in the same order
                as in `constants.TMG_PARAM_NAMES`, which is the same order
                used by the function `tmg_analysis.analyze_tmg_params_by_set`
                which generates the CSV files in `constants.TMG_PARAMS_BY_SET_DIR`.

    """
    if not staggered:
        output_file = constants.ARTICLE_TABLE_DIR + "tmg_tabular.tex"
    elif staggered:
        output_file = constants.ARTICLE_TABLE_DIR + "tmg_tabular_staggered.tex"
    data_dir = constants.TMG_PARAM_STATS_BY_SET_DIR
    param_names = constants.TMG_PARAM_NAMES
    skiprows = 1     # skips Parameter name heading on first row
    pre_cols = (1)   # pre-exercise mean
    post_cols = (2)  # post-exercise mean
    num_sets = 4

    pre_params = np.zeros([len(param_names), num_sets])
    post_params = np.zeros([len(param_names), num_sets])
    for s in range(1, num_sets + 1):  # 1-based numbering
        if not staggered:
            one_set_pre_params = np.loadtxt(data_dir + "set{}-tmg-stats.csv".format(s),
                    delimiter=",",
                    usecols=pre_cols,
                    skiprows=skiprows)
        if staggered:
            # Use set 1 for all pre-exercise params
            one_set_pre_params = np.loadtxt(data_dir + "set{}-tmg-stats.csv".format(1),
                    delimiter=",",
                    usecols=pre_cols,
                    skiprows=skiprows)
        pre_params[:,s-1] = one_set_pre_params

        one_set_post_params = np.loadtxt(data_dir + "set{}-tmg-stats.csv".format(s),
                delimiter=",",
                usecols=post_cols,
                skiprows=skiprows)
        post_params[:,s-1] = one_set_post_params

    # 1D arrays holding each TMG parameter for all sets.
    # Index number assumes the order in constants.SPM_PARAM_NAMES.
    dm_pre           = pre_params[0, :]
    td_pre           = pre_params[1, :]
    tc_pre           = pre_params[2, :]
    rddmax_pre       = pre_params[8, :]
    rddmax_time_pre  = pre_params[11, :]
    dm_post          = post_params[0, :]
    td_post          = post_params[1, :]
    tc_post          = post_params[2, :]
    rddmax_post      = post_params[8, :]
    rddmax_time_post = post_params[11, :]

    # Dm
    dm_pre_str = ""
    dm_post_str = ""
    dm_diff_str = ""
    for s in range(0, num_sets):
        if not staggered:
            dm_pre_str += " & ${:.2f}$".format(dm_pre[s])
        if staggered:
            dm_pre_str += " & ${:.2f}$".format(dm_pre[s]) if s == 0 else " & -"
        dm_post_str += " & ${:.2f}$".format(dm_post[s])
        dm_diff = 100 * (dm_post[s] - dm_pre[s]) / dm_pre[s]
        dm_diff_str += " & ${:+.1f}$\\%".format(dm_diff)

    # Td
    td_pre_str = ""
    td_post_str = ""
    td_diff_str = ""
    for s in range(0, num_sets):
        if not staggered:
            td_pre_str += " & ${:.2f}$".format(td_pre[s])
        if staggered:
            td_pre_str += " & ${:.2f}$".format(td_pre[s]) if s == 0 else " & -"
        td_post_str += " & ${:.2f}$".format(td_post[s])
        td_diff = 100 * (td_post[s] - td_pre[s]) / td_pre[s]
        td_diff_str += " & ${:+.1f}$\\%".format(td_diff)

    # Tc
    tc_pre_str = ""
    tc_post_str = ""
    tc_diff_str = ""
    for s in range(0, num_sets):
        if not staggered:
            tc_pre_str += " & ${:.2f}$".format(tc_pre[s])
        if staggered:
            tc_pre_str += " & ${:.2f}$".format(tc_pre[s]) if s == 0 else " & -"
        tc_post_str += " & ${:.2f}$".format(tc_post[s])
        tc_diff = 100 * (tc_post[s] - tc_pre[s]) / tc_pre[s]
        tc_diff_str += " & ${:+.1f}$\\%".format(tc_diff)

    # RDD max
    rddmax_pre_str = ""
    rddmax_post_str = ""
    rddmax_diff_str = ""
    for s in range(0, num_sets):
        if not staggered:
            rddmax_pre_str += " & ${:.2f}$".format(rddmax_pre[s])
        if staggered:
            rddmax_pre_str += " & ${:.2f}$".format(rddmax_pre[s]) if s == 0 else " & -"
        rddmax_post_str += " & ${:.2f}$".format(rddmax_post[s])
        rddmax_diff = 100 * (rddmax_post[s] - rddmax_pre[s]) / rddmax_pre[s]
        rddmax_diff_str += " & ${:+.1f}$\\%".format(rddmax_diff)

    # RDD max
    rddmax_time_pre_str = ""
    rddmax_time_post_str = ""
    rddmax_time_diff_str = ""
    for s in range(0, num_sets):
        if not staggered:
            rddmax_time_pre_str += " & ${:.2f}$".format(rddmax_time_pre[s])
        if staggered:
            rddmax_time_pre_str += " & ${:.2f}$".format(rddmax_time_pre[s]) if s == 0 else " & -"
        rddmax_time_post_str += " & ${:.2f}$".format(rddmax_time_post[s])
        rddmax_time_diff = 100 * (rddmax_time_post[s] - rddmax_time_pre[s]) / rddmax_time_pre[s]
        rddmax_time_diff_str += " & ${:+.1f}$\\%".format(rddmax_time_diff)

    with open(output_file, 'w') as writer:
        writer.write('\\begin{tabular}{|c|l|c|c|c|c|}')
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.0ex}} \\hspace{-7pt}')
        writer.write('\n    ')
        writer.write('Parameter & & Set 1 & Set 2 & Set 3 & Set 4\\\\')
        writer.write('\n    ')
        writer.write('\\hline')
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.0ex}} \\hspace{-7pt}')
        writer.write('\n    ')
        writer.write('\n    ')

        # Dm
        writer.write('% Dm\n    ')
        writer.write('\\multirow{3}{*}{\\parbox{2cm}{\\centering \\textbf{\\Dm}\\\\ {\\footnotesize Max.\\\\[-0.8ex] displacement}}} & Pre-ISQ Mean $ [\\si{\\milli \\meter}] $')
        writer.write(dm_pre_str + "\\\\")
        writer.write('\n    ')
        writer.write(' & Post-ISQ Mean $ [\\si{\\milli \\meter}] $')
        writer.write(dm_post_str + "\\\\")
        writer.write('\n    ')
        writer.write(' & Percent change')
        writer.write(dm_diff_str + "\\\\")
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.0ex}} \\hspace{-7pt}')
        writer.write('\n    ')
        writer.write('\n    ')

        # Td
        writer.write('% Td\n    ')
        writer.write('\\multirow{3}{*}{\\parbox{2cm}{\\centering \\textbf{\\Td}\\\\ {\\footnotesize Delay time}}} & Pre-ISQ Mean $ [\\si{\\milli \\second}] $')
        writer.write(td_pre_str + "\\\\")
        writer.write('\n    ')
        writer.write(' & Post-ISQ Mean $ [\\si{\\milli \\second}] $')
        writer.write(td_post_str + "\\\\")
        writer.write('\n    ')
        writer.write(' & Percent change')
        writer.write(td_diff_str + "\\\\")
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.0ex}} \\hspace{-7pt}')
        writer.write('\n    ')
        writer.write('\n    ')

        # Tc
        writer.write('% Tc\n    ')
        writer.write('\\multirow{3}{*}{\\parbox{2cm}{\\centering \\textbf{\\Td}\\\\ {\\footnotesize Contraction time}}} & Pre-ISQ Mean $ [\\si{\\milli \\second}] $')
        writer.write(tc_pre_str + "\\\\")
        writer.write('\n    ')
        writer.write(' & Post-ISQ Mean $ [\\si{\\milli \\second}] $')
        writer.write(tc_post_str + "\\\\")
        writer.write('\n    ')
        writer.write(' & Percent change')
        writer.write(tc_diff_str + "\\\\")
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.0ex}} \\hspace{-7pt}')
        writer.write('\n    ')
        writer.write('\n    ')

        # RDD max
        writer.write('% RDD max\n    ')
        writer.write('\\multirow{3}{*}{\\parbox{2cm}{\\centering \\textbf{\\RDDMax}\\\\ {\\footnotesize Max. derivative}}} & Pre-ISQ Mean $ [\\si{\\milli \\meter \\per \\milli \\second}] $')
        writer.write(rddmax_pre_str + "\\\\")
        writer.write('\n    ')
        writer.write(' & Post-ISQ Mean $ [\\si{\\milli \\meter \\per \\milli \\second}] $')
        writer.write(rddmax_post_str + "\\\\")
        writer.write('\n    ')
        writer.write(' & Percent change')
        writer.write(rddmax_diff_str + "\\\\")
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.0ex}} \\hspace{-7pt}')
        writer.write('\n    ')
        writer.write('\n    ')

        # RDD max time
        writer.write('% RDD max time\n    ')
        writer.write('\\multirow{3}{*}{\\parbox{2cm}{\\centering \\textbf{\\RDDMaxTime}\\\\ {\\footnotesize Time of max.\\\\[-0.8ex] derivative}}} & Pre-ISQ Mean $ [\\si{\\milli \\second}] $')
        writer.write(rddmax_time_pre_str + "\\\\")
        writer.write('\n    ')
        writer.write(' & Post-ISQ Mean $ [\\si{\\milli \\second}] $')
        writer.write(rddmax_time_post_str + "\\\\")
        writer.write('\n    ')
        writer.write(' & Percent change')
        writer.write(rddmax_time_diff_str + "\\\\")
        writer.write('\n    ')

        writer.write('\\hline')
        writer.write('\n')
        writer.write('\\end{tabular}')


def make_spm_param_table():
    """
    Creates a single LaTeX table that, for each measurement set,
    compares pre- and post-exercise values of each SPM parameter.

    Columns: Set number (1, 2, 3, and 4)
    Rows: The following SPM param values:
          - Threshold
          - Significance start time [ms]
          - Significance end time [ms]
          - Centroid time [ms]
          - Centroid t-value
          - Maximum
          - Area above threshold

    Input data: The `setX-params.csv` files stored in 
                `constants.SPM_PARAMS_BY_SET_DIR`.
                Assumes SPM params in CSV file appear in the same order 
                as in `constants.SPM_PARAM_NAMES`, which is the same order 
                used by the function `spm_analysis.perform_spm_tests_by_set()`,
                which generates the CSV files in `constants.SPM_PARAMS_BY_SET_DIR`.

    """
    data_dir = constants.SPM_PARAMS_BY_SET_DIR
    output_file = constants.ARTICLE_TABLE_DIR + "spm_tabular.tex"
    param_names = constants.SPM_PARAM_NAMES
    skiprows = 1   # skips "Cluster Number" heading on first row
    usecols = (1)  # use column 2 (param values); ignore column 1 (param names)
    num_sets = 4

    spm_params = np.zeros([len(param_names), num_sets])
    for s in range(1, num_sets + 1):  # 1-based numbering
        # Load individual set's params into 1D array
        one_set_params = np.loadtxt(data_dir + "set{}-params.csv".format(s),
                delimiter=",",
                usecols=usecols,
                skiprows=skiprows)
        # Place the set's params into 2D array for all sets
        spm_params[:,s-1] = one_set_params

    # 1D arrays holding each SPM parameter for all sets.
    # Index number assumes the order in constants.SPM_PARAM_NAMES.
    thresholds     = spm_params[1, :]
    start_times    = spm_params[3, :]
    end_times      = spm_params[4, :]
    centroid_times = spm_params[5, :]
    centroid_ts    = spm_params[6, :]
    spm_maxima     = spm_params[7, :]
    cluster_areas  = spm_params[8, :]
    
    # Threshold
    threshold_str = ""
    for s in range(0, num_sets):
        threshold_str += " & {:.2f}".format(thresholds[s])

    # Start time
    start_time_str = ""
    for s in range(0, num_sets):
        start_time_str += " & {:.2f}".format(start_times[s])

    # End time
    end_time_str = ""
    for s in range(0, num_sets):
        end_time_str += " & {:.2f}".format(end_times[s])

    # Centroid time
    centroid_time_str = ""
    for s in range(0, num_sets):
        centroid_time_str += " & {:.2f}".format(centroid_times[s])

    # Centroid SPMt value
    centroid_t_str = ""
    for s in range(0, num_sets):
        centroid_t_str += " & {:.2f}".format(centroid_ts[s])

    # Max SPMt value
    spm_max_str = ""
    for s in range(0, num_sets):
        spm_max_str += " & {:.2f}".format(spm_maxima[s])

    # Area above threshold
    cluster_area_str = ""
    for s in range(0, num_sets):
        cluster_area_str += " & {:.1f}".format(cluster_areas[s])

    with open(output_file, 'w') as writer:
        writer.write('\\begin{tabular}{|l|c|c|c|c|}')
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.0ex}} \\hspace{-7pt}')
        writer.write('\n    ')

        writer.write('SPM Parameters & Set 1 & Set 2 & Set 3 & Set 4\\\\')
        writer.write('\n    ')
        writer.write('\\hline')
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.0ex}} \\hspace{-7pt}')
        writer.write('\n    ')

        writer.write('SPM threshold $ t^{*} $')
        writer.write(threshold_str + '\\\\')
        writer.write('\n    ')

        writer.write('Start time $ [\\si{\\milli \\second}] $')
        writer.write(start_time_str + '\\\\')
        writer.write('\n    ')

        writer.write('End time $ [\\si{\\milli \\second}] $')
        writer.write(end_time_str + '\\\\')
        writer.write('\n    ')

        writer.write('Centroid time $ [\\si{\\milli \\second}] $')
        writer.write(centroid_time_str + '\\\\')
        writer.write('\n    ')

        writer.write('Centroid $ t $-value')
        writer.write(centroid_t_str + '\\\\')
        writer.write('\n    ')

        writer.write('SPM maximum')
        writer.write(spm_max_str + '\\\\')
        writer.write('\n    ')

        writer.write('Area above threshold')
        writer.write(cluster_area_str + '\\\\')
        writer.write('\n    ')
        writer.write('\\hline')
        writer.write('\n')
        writer.write('\\end{tabular}')


def make_sample_tmg_plot():
    """
    Generates a 2-axis Maplotlib plot showing a TMG signal (axis 0)
    and its time deriviatve (axis 1), with the following parameters defined:
    - Dm, Td, Tc (TMG)
    - RDDMax, RDDMaxTime (TMG derivative)

    Input data: the per-subject measurement files in `constants.INITIAL_DATA_DIR`

    """
    save_figure=True
    show_plot=True

    file_basename = "54-ZI20211112121510"
    pre_file = constants.INITIAL_DATA_DIR + "pre-exercise/" + file_basename + "-pre.csv"
    post_file = constants.INITIAL_DATA_DIR + "post-exercise/" + file_basename + "-post.csv"
    output_file = constants.ARTICLE_FIGURE_DIR + "tmg-example.jpg"

    pre_data = np.loadtxt(pre_file, delimiter=',', skiprows=1)
    post_data = np.loadtxt(post_file, delimiter=',', skiprows=1)
    set_num = 2  # set from which to extract TMG signal
    numpoints = 400

    pre_tmg = pre_data[:numpoints, set_num]
    post_tmg = post_data[:numpoints, set_num]
    pre_rdd = np.gradient(pre_tmg, constants.TMG_DT)
    post_rdd = np.gradient(post_tmg, constants.TMG_DT)

    N = np.shape(pre_tmg)[0]         # number of rows in pre/post_data
    time = np.linspace(0, N - 1, N)  # [ms] assuming 1 kHz sampling

    # Only show TMG parameters for pre-exercise signal to avoid clutter
    params = tmg_params.get_params_of_tmg_signal(pre_tmg)
    dm = params[0]
    td = params[1]
    tc = params[2]
    rdd_max = params[8]
    rdd_max_time = params[11]
    dm_index = np.argmax(pre_tmg)

    # --------------------------------------------- #
    # BEGIN PLOTTING
    # --------------------------------------------- #
    fig_width_inches = 7
    fig, axes = plt.subplots(2, 1, figsize=(fig_width_inches, 0.8*fig_width_inches))
    tmg_data_start_row = constants.TMG_ROWS_TO_SKIP_FOR_SPM
    fig_dpi = 400
    fig_format = "jpg"
    
    # For labels showing "Dm", "Tc", etc...
    param_font_size = 11

    # For arrows indicating TMG/RDD parameters
    arrow_linewidth=1.0

    # For boxes surrounding parameter names
    param_bbox = dict(facecolor='#ffffff',
            boxstyle="round, rounding_size=0.1, pad=0.2")

    # Plot TMG measurement
    # --------------------------------------------- #
    ax = axes[0]
    plotting.remove_spines(ax)

    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("Displacement [mm]")

    ax.plot(time, pre_tmg)

    # Move y axis to t = 0
    ax.set_xlim(xmin=0)

    # Horizontal dashed line noting y = 0
    ax.axhline(y=0, color='black', linestyle=':')  

    # Vertical dashed line noting 0.1*Dm
    ax.vlines(td, 0.1*dm, 0.96*dm, color='black', linestyle=':')  

    # Arrow and text for Dm
    ax.text(dm_index, 0.5*dm, "Dm",
            ha="center", va="center",
            fontsize=param_font_size,
            zorder=10,
            bbox=param_bbox)
    ax.annotate("", xy=(dm_index, dm), xytext=(dm_index, 0),
            arrowprops=dict(lw=arrow_linewidth, arrowstyle="<->, head_length=0.8, head_width=0.4"))

    # Arrow and text for Td
    ax.text(0.5*td, 0.20*dm, "Td",
            ha="center", va="center",
            fontsize=param_font_size,
            bbox=param_bbox)
    ax.annotate("", xy=(0, 0.1*dm), xytext=(td, 0.1*dm),
            arrowprops=dict(lw=arrow_linewidth, arrowstyle="<->, head_length=0.3, head_width=0.5"))

    # Arrow and text for Tc
    ax.text(td + 0.5*tc, 0.99*dm, "Tc",
            ha="center", va="center",
            fontsize=param_font_size,
            bbox=param_bbox)
    ax.annotate("", xy=(td, 0.9*dm), xytext=(td + tc, 0.9*dm),
            arrowprops=dict(lw=arrow_linewidth, arrowstyle="<->, head_length=0.3, head_width=0.5"))

    # --------------------------------------------- #

    # Plot TMG derivative
    # --------------------------------------------- #
    ax = axes[1]
    plotting.remove_spines(ax)

    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("Disp. per time [mm/ms]")

    ax.plot(time, pre_rdd)

    # Move y axis to t = 0
    ax.set_xlim(xmin=0)

    # Horizontal dashed line noting y = 0
    ax.axhline(y=0, color='black', linestyle=':')  

    # Vertical dashed line noting RDDMaxTime
    ax.vlines(rdd_max_time, -0.15*rdd_max, 0, color='black', linestyle=':')  

    # Arrow and text for RDDMax
    ax.text(rdd_max_time, 0.5*rdd_max, "RDDMax",
            ha="center", va="center",
            fontsize=param_font_size,
            zorder=10,
            bbox=param_bbox)
    ax.annotate("", xy=(rdd_max_time, rdd_max), xytext=(rdd_max_time, 0),
            arrowprops=dict(lw=arrow_linewidth, arrowstyle="<->, head_length=0.8, head_width=0.4"))

    # Arrow and text for RDDMaxTime
    ax.text(0.5*rdd_max_time, -0.30*rdd_max, "RDDMax\nTime",
            ha="center", va="center",
            fontsize=param_font_size,
            bbox=param_bbox)
    ax.annotate("", xy=(0, -0.09*rdd_max), xytext=(rdd_max_time, -0.09*rdd_max),
            arrowprops=dict(lw=arrow_linewidth, arrowstyle="<->, head_length=0.4, head_width=0.5"))

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.12)

    if save_figure:
        plt.savefig(output_file, dpi=fig_dpi, bbox_inches='tight', pad_inches = 0)

    if show_plot:
        plt.show()


def make_sample_spm_plot():
    """
    Generates a 2-axis Maplotlib plot showing the results of a
    representative SPM paired t-test using unnormalized TMG data from a
    single subject.

    Input data: the per-subject measurement files in `constants.SPM_DATA_DIR`

    """
    save_figure=True
    show_plot=False

    file_basename = "54-ZI20211112121510"
    pre_file = constants.SPM_DATA_DIR + "pre-exercise/" + file_basename + "-pre.csv"
    post_file = constants.SPM_DATA_DIR + "post-exercise/" + file_basename + "-post.csv"
    output_file = constants.ARTICLE_FIGURE_DIR + "spm-example.jpg"

    pre_data = np.loadtxt(pre_file, delimiter=',', skiprows=1)
    post_data = np.loadtxt(post_file, delimiter=',', skiprows=1)

    # --------------------------------------------- #
    # BEGIN PLOTTING
    # --------------------------------------------- #
    width_inches = 7
    fig, axes = plt.subplots(1, 2, figsize=(width_inches, 0.5*width_inches))
    tmg_data_start_row = constants.TMG_ROWS_TO_SKIP_FOR_SPM

    fig_dpi = 350
    fig_format = "jpg"

    pre_color    = constants.PRE_COLOR
    post_color   = constants.POST_COLOR
    pre_alpha    = constants.PRE_ALPHA
    post_alpha   = constants.POST_ALPHA
    tline_color  = constants.T_LINE_COLOR
    tfill_color  = constants.T_FILL_COLOR
    tfill_color2 = constants.T_FILL_COLOR2
    linewidth = 1.5

    # Loop through each set of normalized measurements
    t, ti = spm_analysis._get_spm_ti(pre_data, post_data)

    # Begin plotting
    # --------------------------------------------- #
    N = np.shape(post_data)[0]       # number of rows in pre/post_data
    time = np.linspace(0, N - 1, N)  # [ms] assuming 1 kHz sampling

    post_mean = np.mean(post_data, axis=1)
    pre_mean = np.mean(pre_data, axis=1)
    post_sd = np.std(post_data, ddof=1, axis=1)
    pre_sd = np.std(pre_data, ddof=1, axis=1)

    # Plot TMG measurement
    # --------------------------------------------- #
    ax = axes[0]
    plotting.remove_spines(ax)

    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("Displacement [mm]")

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

    ax.legend(framealpha=1.0, loc="lower right")
    # --------------------------------------------- #

    # Plot SPM results
    # --------------------------------------------- #
    ax = axes[1]
    plotting.remove_spines(ax)

    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("SPM $t$-continuum", labelpad=-0.1)

    ax.set_ylim(-7, 12)
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


def make_setwise_spm_subplots():
    """
    Generates a 4-axis Maplotlib plot showing SPM results for
    sets 1, 2, 3, and 4 for use in the Frontiers journal article.

    Essentially the same figures as produced by 
    `spm_analysis.perform_spm_tests_by_set`, just placed in a single figure
    to meet the Frontiers requirement that subfigures be in a single figure.

    Input data: the normalized per-subject measurement files in `constants.NORMED_SPM_DATA_DIR`

    """
    save_figure=True, 
    show_plot=False

    pre_input_dir = constants.NORMED_SPM_DATA_DIR + "pre-exercise/"
    post_input_dir = constants.NORMED_SPM_DATA_DIR + "post-exercise/"
    output_file = constants.ARTICLE_FIGURE_DIR + "spm-subplot.jpg"

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
    
    # --------------------------------------------- #
    # BEGIN PLOTTING
    # --------------------------------------------- #
    fig, axes = plt.subplots(sets_per_measurement_file, 2, figsize=(6.8, 8))
    tmg_data_start_row = constants.TMG_ROWS_TO_SKIP_FOR_SPM

    subfib_labels = ["(1)", "(2)", "(3)", "(4)"]

    fig_dpi = 500
    fig_format = "jpg"

    pre_color    = constants.PRE_COLOR
    post_color   = constants.POST_COLOR
    pre_alpha    = constants.PRE_ALPHA
    post_alpha   = constants.POST_ALPHA
    tline_color  = constants.T_LINE_COLOR
    tfill_color  = constants.T_FILL_COLOR
    tfill_color2 = constants.T_FILL_COLOR2

    linewidth = 1.5

    # Loop through each set of normalized measurements
    for s in range(sets_per_measurement_file):
        pre_data = pre_tensor[:, s, :]
        post_data = post_tensor[:, s, :]
        t, ti = spm_analysis._get_spm_ti(pre_data, post_data)

        # Begin plotting
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
        if s == sets_per_measurement_file - 1:  
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
        if s == sets_per_measurement_file - 1:  
            ax.set_xlabel("Time [ms]")
        ax.set_ylabel("SPM $t$-continuum", labelpad=-0.1)

        ax.set_ylim(-7, 12)
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


if __name__ == "__main__":
    # make_spm_param_table()
    # make_tmg_param_table()
    # make_tmg_param_table(staggered=True)
    make_sample_tmg_plot()
    # make_sample_spm_plot()
    # make_setwise_spm_subplots()

