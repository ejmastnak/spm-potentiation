import os
import numpy as np
import constants, frontiers_utils

"""
A set of functions used to create the LaTeX tables that appear in the journal
article; in this sense, this script represents the final step in this project's
analysis pipeline.
"""

def make_tmg_param_table_by_subj_by_set():
    """
    Creates a single LaTeX `tabular` environment to demonstrate a comparison of
    pre-ISQ and post-ISQ TMG parameters in a given set for a given subject.

    Input data: A sample TMG stat output file in
    `TMG_STATS_BY_SUBJ_BY_SET_8MPS_DIR`.

    """
    input_dir = constants.TMG_STATS_BY_SUBJ_BY_SET_8MPS_DIR
    input_filename = "54-ZI20211112121510/set-1-tmg-stats.csv"
    output_file = constants.ARTICLE_TABLE_DIR + "tmg_stats_by_subj_by_set.tex"
    table_title = "Subject 1, Set 1"

    _make_tmg_param_table(input_dir + input_filename, output_file,
            comment="Generated from {}".format(input_filename),
            table_title=table_title)


def make_tmg_param_table_by_subj_across_sets():
    """
    Creates a single LaTeX `tabular` environment to demonstrate a comparison of
    pre-ISQ and post-ISQ TMG parameters for a given subject across all sets.

    Input data: A sample TMG stat output file in
    `TMG_STATS_BY_SUBJ_ACROSS_SETS_1MPS_DIR`.

    """
    input_dir = constants.TMG_STATS_BY_SUBJ_ACROSS_SETS_1MPS_DIR
    input_filename = "54-ZI20211112121510-tmg-stats.csv"
    output_file = constants.ARTICLE_TABLE_DIR + "tmg_stats_by_subj_across_sets.tex"
    table_title = "Subject 1, Sets 1-8"

    _make_tmg_param_table(input_dir + input_filename, output_file,
            comment="Generated from {}".format(input_filename),
            table_title=table_title)


def make_tmg_param_table_by_set_across_subj():
    """
    Creates a single LaTeX table to demonstrate a comparison of pre-ISQ and
    post-ISQ TMG parameters for a given subject across all sets

    Input data: The TMG stat output file in `TMG_STATS_BY_SET_ACROSS_SUBJ_DIR`.

    """
    input_dir = constants.TMG_STATS_BY_SET_ACROSS_SUBJ_DIR
    sets_to_use = [1, 2, 3, 4]

    for s in sets_to_use:
        input_filename = "set-{}-tmg-stats.csv".format(s)
        output_file = constants.ARTICLE_TABLE_DIR + "tmg_stats_across_subj_by_set_{}.tex".format(s)
        table_title = "Subjects 1-54, Set {}".format(s)

        _make_tmg_param_table(input_dir + input_filename, output_file,
                comment="Generated from {}".format(input_filename),
                table_title=table_title)


def _make_tmg_param_table(input_file, output_file, comment=None, table_title=None):
    """
    Creates LaTeX tabular environment summarizing the contents of a CSV file summarizing
    a pre-ISQ/post-ISQ comparison of TMG parameters.

    Columns: Stat values in `constants.TMG_STAT_NAMES`
    Rows: The following TMG param values:
          - Dm [mm]
          - Td [ms]
          - Tc [ms]
          - RDDMax [mm/ms]
          - RDDMaxTime [ms]

    Input data: A CSV file whose columns correspond to the statistics in
        `constants.TMG_STAT_NAMES` and whose rows follow the same order as in
        `constants.TMG_PARAM_NAMES`, which is the same order used by the
        function `tmg_analysis.analyze_tmg_params_by_set` which generates the
        CSV files in `constants.TMG_PARAMS_BY_SET_DIR`.

    """
    param_names = constants.TMG_PARAM_NAMES
    stat_names = constants.TMG_STAT_NAMES
    num_stats = len(stat_names)
    skiprows = 1     # skips stat name heading on first row
    usecols = tuple(range(1, num_stats + 1))  # skip param names in first column

    tmg_stats = np.loadtxt(input_file,
            delimiter=",",
            usecols=usecols,
            skiprows=skiprows)

    # Row indices of Dm, Td, Tc, RDDMax, and RDDMaxTime within `tmg_stats`
    param_indices = [0, 1, 2, 8, 11]

    printable_param_names = ["\\Dm [\\si{\\milli \\meter}]", "\\Td [\\si{\\milli \\second}]", "\\Tc [\\si{\\milli \\second}]", "\\RDDMax [\\si{\\milli \\meter \\per \\milli \\second}]", "\\RDDMaxTime [\\si{\\milli \\second}]"]
    formats = [
            [".2f", ".2f", ".2f", ".2f", ".1f", ".0e"],  # Dm
            [".1f", ".1f", ".1f", ".1f", ".1f", ".0e"],  # Td
            [".1f", ".1f", ".1f", ".1f", ".1f", ".0e"],  # Tc
            [".2f", ".2f", ".2f", ".2f", ".1f", ".0e"],  # RDDMax
            [".1f", ".1f", ".1f", ".1f", ".1f", ".0e"],  # RDDMaxTime
            ]

    with open(output_file, 'w') as writer:

        # Used to record which file the table was generated as a comment in the
        # table's LaTeX source code.
        if comment is not None:  
            writer.write('% {}\n'.format(comment))

        writer.write('\\begin{tabular}{|l|c|c|c|c|c|c|}')
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.0ex}} \\hspace{-7pt}')
        writer.write('\n    ')

        # Used to add a brief title indicating the subject and set(s) from
        # which the table was generated that is visible in the compiled tabled.
        if table_title is not None:  
            writer.write('\\textbf{{{}}}'.format(table_title))

        writer.write(' & $ \\mu_{\\text{pre}} $ & $ \\mu_{\\text{post}} $ & $ \\sigma_{\\text{pre}} $ & $ \\sigma_{\\text{post}} $ & $ \\lvert t \\rvert $ & $ p $ \\\\[0.3ex]')
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.0ex}} \\hspace{-7pt}')
        writer.write('\n    ')

        for i, p in enumerate(param_indices):  # loop through all TMG parameters
            writer.write(printable_param_names[i])
            for j, stat in enumerate(tmg_stats[p, :]):  # loop through all parameter stats
                if j == 4:  # take absolute value of t-statistic
                    writer.write(" & $ {0:{1}} $ ".format(np.abs(stat), formats[i][j]))
                elif j == 5:  # write p value in scientific notation
                    writer.write(" & $ \SI{{{0:{1}}}}{{}} $ ".format(stat, formats[i][j]))
                else:
                    writer.write(" & $ {0:{1}} $ ".format(stat, formats[i][j]))

            writer.write('\\\\\n    ')

        writer.write('\\hline')
        writer.write('\n')
        writer.write('\\end{tabular}')


def make_tmg_param_table_by_set_across_subj_old(use_set1_as_baseline=False):
    """
    Creates a single LaTeX table that, for each measurement set, compares pre-
    and post-exercise values of each TMG parameter averaged across all subjects.

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
    if not use_set1_as_baseline:
        output_file = constants.ARTICLE_TABLE_DIR + "tmg_tabular.tex"
    elif use_set1_as_baseline:
        output_file = constants.ARTICLE_TABLE_DIR + "tmg_tabular_relto_baseline.tex"
    input_dir = constants.TMG_STATS_BY_SET_ACROSS_SUBJ_DIR
    param_names = constants.TMG_PARAM_NAMES
    skiprows = 1     # skips Parameter name heading on first row
    pre_cols = (1)   # pre-exercise mean
    post_cols = (2)  # post-exercise mean
    max_set = 4

    pre_params = np.zeros([len(param_names), max_set])
    post_params = np.zeros([len(param_names), max_set])
    for s in range(1, max_set + 1):  # 1-based numbering
        if not use_set1_as_baseline:
            one_set_pre_params = np.loadtxt(input_dir + "set{}-tmg-stats.csv".format(s),
                    delimiter=",",
                    usecols=pre_cols,
                    skiprows=skiprows)
        if use_set1_as_baseline:
            # Use set 1 for all pre-exercise params
            one_set_pre_params = np.loadtxt(input_dir + "set{}-tmg-stats.csv".format(1),
                    delimiter=",",
                    usecols=pre_cols,
                    skiprows=skiprows)
        pre_params[:,s-1] = one_set_pre_params

        one_set_post_params = np.loadtxt(input_dir + "set{}-tmg-stats.csv".format(s),
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
    for s in range(0, max_set):
        if not use_set1_as_baseline:
            dm_pre_str += " & ${:.2f}$".format(dm_pre[s])
        if use_set1_as_baseline:
            dm_pre_str += " & ${:.2f}$".format(dm_pre[s]) if s == 0 else " & -"
        dm_post_str += " & ${:.2f}$".format(dm_post[s])
        dm_diff = 100 * (dm_post[s] - dm_pre[s]) / dm_pre[s]
        dm_diff_str += " & ${:+.1f}$\\%".format(dm_diff)

    # Td
    td_pre_str = ""
    td_post_str = ""
    td_diff_str = ""
    for s in range(0, max_set):
        if not use_set1_as_baseline:
            td_pre_str += " & ${:.2f}$".format(td_pre[s])
        if use_set1_as_baseline:
            td_pre_str += " & ${:.2f}$".format(td_pre[s]) if s == 0 else " & -"
        td_post_str += " & ${:.2f}$".format(td_post[s])
        td_diff = 100 * (td_post[s] - td_pre[s]) / td_pre[s]
        td_diff_str += " & ${:+.1f}$\\%".format(td_diff)

    # Tc
    tc_pre_str = ""
    tc_post_str = ""
    tc_diff_str = ""
    for s in range(0, max_set):
        if not use_set1_as_baseline:
            tc_pre_str += " & ${:.2f}$".format(tc_pre[s])
        if use_set1_as_baseline:
            tc_pre_str += " & ${:.2f}$".format(tc_pre[s]) if s == 0 else " & -"
        tc_post_str += " & ${:.2f}$".format(tc_post[s])
        tc_diff = 100 * (tc_post[s] - tc_pre[s]) / tc_pre[s]
        tc_diff_str += " & ${:+.1f}$\\%".format(tc_diff)

    # RDD max
    rddmax_pre_str = ""
    rddmax_post_str = ""
    rddmax_diff_str = ""
    for s in range(0, max_set):
        if not use_set1_as_baseline:
            rddmax_pre_str += " & ${:.2f}$".format(rddmax_pre[s])
        if use_set1_as_baseline:
            rddmax_pre_str += " & ${:.2f}$".format(rddmax_pre[s]) if s == 0 else " & -"
        rddmax_post_str += " & ${:.2f}$".format(rddmax_post[s])
        rddmax_diff = 100 * (rddmax_post[s] - rddmax_pre[s]) / rddmax_pre[s]
        rddmax_diff_str += " & ${:+.1f}$\\%".format(rddmax_diff)

    # RDD max
    rddmax_time_pre_str = ""
    rddmax_time_post_str = ""
    rddmax_time_diff_str = ""
    for s in range(0, max_set):
        if not use_set1_as_baseline:
            rddmax_time_pre_str += " & ${:.2f}$".format(rddmax_time_pre[s])
        if use_set1_as_baseline:
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


def make_spm_param_table_by_set_across_subj():
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
    make_tmg_param_table_by_subj_by_set()
    make_tmg_param_table_by_subj_across_sets()
    make_tmg_param_table_by_set_across_subj()
    # make_spm_param_table_by_set_across_subj()
    # make_tmg_param_table_by_set_across_subj()
    # make_tmg_param_table_by_set_across_subj(use_set1_as_baseline=True)
