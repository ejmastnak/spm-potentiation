from pathlib import Path
from decimal import Decimal
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import spm1d
import spm_analysis, constants

def plot_spm_ttest(t, ti, pre_data, post_data, time_offset,
        figure_output_path, fig_format="png", fig_dpi=300,
        tmg_y_axis_label="Displacement", x_axis_label="Time [ms]",
        title=None, ti_params_df=None,
        show_plot=True, save_figures=False):
    """
    Plots the pre and post-exercise data's mean and standard deviation clouds on axis 0.
    Plots the SPM t-test between the pre and post-exericse data on axis 1.

    Parameters
    ----------
    t : spm1d.stats._spm.SPM_T
        An SPM T object associated with a comparision of pre_data and post_data
    ti : spm1d.stats._spm.SPMi_T
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
    tmg_y_axis_label : str
        Label, passed to Matplotlib's `ax.set_ylabel`, for the y axis
        of the plot showing TMG signals.
    x_axis_label : str
        Label, passed to Matplotlib's `ax.set_xlabel`, for the x axis
        of both the plot showing TMG signals and the SPM t-statistic plot.
    title : str
        Optional title
    ti_params_df : DataFrame
        An optional Pandas DataFrame frame computed in `spm_analysis.py`
        holding parameters describing the ti object.
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

    width_inches = 7
    fig, axes = plt.subplots(1, 2, figsize=(width_inches, 0.5*width_inches))

    # Plot time-series measurements (generally TMG data)
    # --------------------------------------------- #
    ax = axes[0]
    remove_spines(ax)
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(tmg_y_axis_label)

    # Mean value of time-series measurements
    ax.plot(time, pre_mean, color=constants.PRE_COLOR, linewidth=2.5, 
            label="Pre-ISQ", zorder=4)
    ax.plot(time, post_mean, color=constants.POST_COLOR, linewidth=2.5,
            label="Post-ISQ", zorder=3)

    # Standard deviation clouds
    ax.fill_between(time, post_mean - post_sd, post_mean + post_sd, 
            color=constants.POST_COLOR, alpha=constants.POST_ALPHA, zorder=2)
    ax.fill_between(time, pre_mean - pre_sd, pre_mean + pre_sd,
            color=constants.PRE_COLOR, alpha=constants.PRE_ALPHA, zorder=1)

    ax.axhline(y=0, color='black', linestyle=':')  # dashed line at y = 0
    ax.legend(framealpha=1.0, loc="lower right")
    # --------------------------------------------- #

    # Plot SPM results
    # --------------------------------------------- #
    ax = axes[1]
    remove_spines(ax)
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel("SPM $t$-continuum", labelpad=-0.1)

    # Plot SPM t-statistic
    ax.plot(time, t.z, color=constants.SPM_T_LINE_COLOR)  # plot t-curve

    # Plot dashed line at y = 0
    ax.axhline(y=0, color='black', linestyle=':')  

    # Plot dashed line at SPM significance threshold
    ax.axhline(y=ti.zstar, color='#000000', linestyle='--')

    # Text box showing alpha, threshold value, and p value
    ax.text(0.70, 0.97, 
            get_annotation_text(ti, ti_params_df=ti_params_df),
            va='top', ha='left',
            transform=ax.transAxes,
            bbox=dict(facecolor='#FFFFFF', edgecolor='#222222', boxstyle='round,pad=0.3'))

    # Shade between curve and threshold
    ax.fill_between(time, t.z, ti.zstar, where=t.z >= ti.zstar,
            interpolate=True, color=constants.SPM_FILL_COLOR)

    if title is not None:
        plt.suptitle(title, y=0.93, fontsize=16)

    plt.tight_layout()

    if save_figures:
        plt.savefig(figure_output_path, format=fig_format, dpi=fig_dpi, 
                bbox_inches='tight', pad_inches = 0)

    if show_plot:  # either show plot...
        plt.show()
    else:  # ...or clear plot during automated batch tasks to clear memory
        plt.close(fig)


def get_annotation_text(ti, ti_params_df=None):
    """
    Used to create a nice-looking annotation of the alpha, p, and t-threshold
    values for the plot of an SPM t-test.
    Accounting for formatting/new line characters, output looks something like...
    t^* = 4.42
    alpha = 0.05
    p < 0.0001

    Keep in mind that alpha and tstar are assigned globally for the entire SPM
    ti object, while p-values are assigned on a per-cluster basis. 
    For ti objects with multiple supra-threshold significance clusters,
    descriptive parameters are printed only the cluster with the smallest
    p-value. This is not perfectly general, but works well for TMG signals.

    Parameters
    ----------
    ti : spm1d.stats._spm.SPMi_T
        An SPM TI inference object
    ti_params_df : DataFrame
        An optional Pandas DataFrame frame computed in `spm_analysis.py`
        holding parameters describing the ti object.
    """
    # If no parameter DataFrame was passed or if no supra-threshold clusters
    # occurred, write only t-star and alpha.
    if ti_params_df is None or ti.clusters is None or len(ti.clusters) == 0:
        return "$\\alpha = {:.2f}$\n$t^* = {:.2f}$".format(ti.zstar, ti.alpha)

    # If at least one supra-threshold cluster occured
    ti_params = ti_params_df.to_numpy()

    # Declare indices of various parameters in `constants.SPM_PARAM_NAMES`
    p_index = 2
    start_time_index = 3
    end_time_index = 4
    t_max_index = 7
    area_index = 8

    # Find index of cluster with smallest p-value
    c_min = np.argmin(ti_params[p_index, :])

    # Parameters for cluster with smallest p-value
    p          = ti_params[p_index, c_min]
    start_time = ti_params[start_time_index, c_min]
    end_time   = ti_params[end_time_index, c_min]
    t_max      = ti_params[t_max_index, c_min]
    area       = ti_params[area_index, c_min]

    # This if/else block ensures p-value is written in nicely-readable
    # scientific notation.
    # See https://stackoverflow.com/a/45359185
    if p == 0.0:
        p_string =  "$p = 2 \\cdot 10^{{-16}}$\n"

        return str.format((
              "$\\alpha = {alpha:.2f}$\n"
            + "$p = 2 \\cdot 10^{{-16}}$\n"
            + "$T_1 = {t_start:.1f} \, \\mathrm{{ms}}$\n"
            + "$T_2 = {t_end:.1f} \, \\mathrm{{ms}}$\n"
            + "$t^* = {threshold:.2f}$\n"
            + "$t$-$\\mathrm{{max}} = {maximum:.1f}$\n"
            + "$\\mathrm{{Area}} = {area:.0f}$"
            ),
            alpha=ti.alpha, threshold=ti.zstar,
            t_start = start_time, t_end = end_time,
            maximum = t_max, area = area)

    else: # extract exponent and mantissa for scientific notation
        (sign, digits, exponent) = Decimal(p).as_tuple()
        exp = len(digits) + exponent - 1
        man = Decimal(p).scaleb(-exp).normalize()

        return str.format((
              "$\\alpha = {alpha:.2f}$\n"
            + "$p = {man:.0f} \\cdot 10^{{{exp:.0f}}}$\n"
            + "$T_1 = {t_start:.1f} \, \\mathrm{{ms}}$\n"
            + "$T_2 = {t_end:.1f} \, \\mathrm{{ms}}$\n"
            + "$t^* = {threshold:.2f}$\n"
            + "$t$-$\\mathrm{{max}} = {maximum:.1f}$\n"
            + "$\\mathrm{{Area}} = {area:.0f}$"
            ),
            alpha=ti.alpha, threshold=ti.zstar,
            man=man, exp=exp,
            t_start = start_time, t_end = end_time,
            maximum = t_max, area = area)
        

def remove_spines(ax):
    """ Simple auxiliary function to remove upper and right spines from the passed axis"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
