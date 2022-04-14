import os
import numpy as np
import matplotlib.pyplot as plt
import tmg_biomechanics.tmg_params_pypi as tmg_params_pypi
import plotting, constants, frontiers_utils, spm_analysis
"""
A set of functions used to create the LaTeX tables that appear in the journal
article; in this sense, this script represents the final step in this project's
analysis pipeline.
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
    data_dir = constants.TMG_PARAM_STATS_ACROSS_SUBJECTS_DIR
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
    data_dir = constants.SPM_PARAMS_BY_SET_ACROSS_SUBJ_DR
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


if __name__ == "__main__":
    make_spm_param_table()
    make_tmg_param_table()
    make_tmg_param_table(staggered=True)

