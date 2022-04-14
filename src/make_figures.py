import os
import numpy as np
import matplotlib.pyplot as plt
import tmg_biomechanics.tmg_params_pypi as tmg_params_pypi
import plotting, constants, frontiers_utils, spm_analysis
"""
A set of functions used to create the Matplotlib figures that appear in the
journal article; in this sense, this script represents the final step in this
project's analysis pipeline.
"""

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
    params = tmg_params_pypi.get_params_of_tmg_signal(pre_tmg)
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
    show_plot=True

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
    t, ti = spm_analysis._get_spm_t_ti_paired_ttest(pre_data, post_data, alpha=0.05)
    # print(type(t))

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
        t, ti = spm_analysis._get_spm_t_ti_paired_ttest(pre_data, post_data)

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
    make_sample_tmg_plot()
    make_sample_spm_plot()
    make_setwise_spm_subplots()

