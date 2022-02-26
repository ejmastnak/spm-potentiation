from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import spm1d
import spm_analysis

# START COLORS
pre_color = "#000000"  # black
post_color = "#dd502d"  # orange
post_color2 = "#3997bf"  # blue
pre_alpha = 0.20
post_alpha = 0.75

tline_color = "#000000"  # black
tfill_color = "#7e3728"  # light orange
tfill_color2 = "#244d90"  # light blue
# END COLORS

def plot_spm_ttest(t, ti, pre_data, post_data, time_offset,
        figure_output_path, fig_format="png", fig_dpi=300,
        show_plot=True, save_figures=False):
    """
    Plots the pre and post-exercise data's mean and standard deviation clouds on axis 0.
    Plots the SPM t-test between the pre and post-exericse data on axis 1.

    Parameters
    ----------
    t : TODO
        An SPM T object associated with a comparision of pre_data and post_data
    ti : TODO
        The SPM TI inference object associated with `t`.
    pre_data : ndarray
        2D numpy array containing pre-exercise measurement data.
    post_data : ndarray
        2D numpy array containing post-exercise measurement data.
        Should have the same number of rows as `pre_data`.
    time_offset : double
        Time TODO units (an integer number of milliseconds for TMG data)
        to append to `time` array to account for the fact that the first
        row of TMG data (which is always zero) is usually skipped in SPM
        analysis to avoid zero-variance problems.
    figure_output_path : str
        Path at which to save plot as a figure.
    fig_format : str
        Format passed to Matplotlib's `savefig` function.
        The user is reponsible for file extension of `figure_output_path`
        matching `fig_format` in a sensible way.
    fig_dpi : int
        Passed to `dpi` parameter Matplotlib's `savefig` function.
        Controls DPI at which to save figures.
    show_plot : bool
        Whether or not to show matplotlib plot.
        Generally set to False for automated processes.
    save_figures : bool
        Whether or not to automatically save figure before plotting.

    """
    N = np.shape(post_data)[0]  # number of rows in pre/post_data
    time = np.linspace(0, N - 1, N) + time_offset  # [ms] assuming 1 kHz sampling

    post_mean = np.mean(post_data, axis=1)
    pre_mean = np.mean(pre_data, axis=1)
    post_sd = np.std(post_data, ddof=1, axis=1)
    pre_sd = np.std(pre_data, ddof=1, axis=1)

    fig, axes = plt.subplots(1, 2, figsize=(8, 4))

    # Plot time-series measurements (generally TMG data)
    # --------------------------------------------- #
    ax = axes[0]
    remove_spines(ax)
    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("Displacement [mm]")

    # Mean value of time-series measurements
    ax.plot(time, pre_mean, color=pre_color, linewidth=2.5, 
            label="Pre-exercise mean", zorder=4)
    ax.plot(time, post_mean, color=post_color, linewidth=2.5,
            label="Post-exercise mean", zorder=3)

    # Standard deviation clouds
    ax.fill_between(time, post_mean - post_sd, post_mean + post_sd, 
            color=post_color, alpha=post_alpha, zorder=2)
    ax.fill_between(time, pre_mean - pre_sd, pre_mean + pre_sd,
            color=pre_color, alpha=pre_alpha, zorder=1)

    ax.axhline(y=0, color='black', linestyle=':')  # dashed line at y = 0
    ax.legend(framealpha=1.0)
    # --------------------------------------------- #

    # Plot SPM results
    # --------------------------------------------- #
    ax = axes[1]
    remove_spines(ax)
    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("SPM $t$ statistic", labelpad=-0.1)

    # Plot SPM t-statistic
    ax.plot(time, t.z, color=tline_color)  # plot t-curve

    # Plot dashed line at y = 0
    ax.axhline(y=0, color='black', linestyle=':')  

    # Plot dashed line at SPM significance threshold
    ax.axhline(y=ti.zstar, color='#000000', linestyle='--')

    # Text box showing alpha, threshold value, and p value
    ax.text(73, ti.zstar + 0.4, get_annotation_text(ti),
            va='bottom', ha='left', 
            bbox=dict(facecolor='#FFFFFF', edgecolor='#222222', boxstyle='round,pad=0.3'))

    # Shade between curve and threshold
    ax.fill_between(time, t.z, ti.zstar, where=t.z >= ti.zstar,
            interpolate=True, color=tfill_color)

    if save_figures:
        plt.savefig(figure_output_path, format=fig_format, dpi=fig_dpi)

    if show_plot:  # either show plot...
        plt.show()
    else:  # ...or clear plot during automated batch tasks to clear memory
        plt.close(fig)

def get_annotation_text(ti):
    """
    Used to create a nice-looking annotation of the alpha, p, and t-threshold
    values for the plot of an SPM t-test.
    Accounting for formatting/new line characters, output looks something like...
    t^* = 4.42
    alpha = 0.05
    p < 0.0001  # Assuming a single significance cluster

    Keep in mind that alpha and tstar are assigned globally 
    for the entire SPM ttest, while p-values are assigned on 
    a per-cluster basis. Thus p-value is included only for a
    ttest producing one significance cluster.

    """
    if len(ti.clusters) == 1:
        p = ti.clusters[0].P
        if p < 0.0001:
            return "$t^* = {:.2f}$\n$\\alpha = {:.2f}$\n$p < 0.0001$".format(ti.zstar, ti.alpha)
        else:
            return "$t^* = {:.2f}$\n$\\alpha = {:.2f}$\n$p = {:.4f}$".format(ti.zstar, ti.alpha, p)
    else:
        return "$t^* = {:.2f}$\n$\\alpha = {:.2f}$".format(ti.zstar, ti.alpha)

def remove_spines(ax):
    """ Simple auxiliary function to remove upper and right spines from the passed axis"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
