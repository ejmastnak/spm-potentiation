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
    subject_number = 1
    if subject_number < 10:  # accomodate leading zero for numbers 1-9
        input_filename = "subject-0{}/set-1-tmg-stats.csv".format(subject_number)
    else:
        input_filename = "subject-{}/set-1-tmg-stats.csv".format(subject_number)
    table_title = "Subject {}, Set 1".format(subject_number)
    output_file = constants.MANUSCRIPT_TABLE_DIR + "tmg_stats_by_subj_by_set.tex"

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
    subject_number = 1
    if subject_number < 10:  # accomodate leading zero for numbers 1-9
        input_filename = "subject-0{}-tmg-stats.csv".format(subject_number)
    else:
        input_filename = "subject-{}-tmg-stats.csv".format(subject_number)
    output_file = constants.MANUSCRIPT_TABLE_DIR + "tmg_stats_by_subj_across_sets.tex"
    table_title = "Subject {}, Sets 1-8".format(subject_number)

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
        output_file = constants.MANUSCRIPT_TABLE_DIR + "tmg_stats_across_subj_by_set_{}.tex".format(s)
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
            [".2f", ".2f", "+.0f", ".2f", ".2f", ".1f", ".0e"],  # Dm
            [".1f", ".1f", "+.0f", ".1f", ".1f", ".1f", ".0e"],  # Td
            [".1f", ".1f", "+.0f", ".1f", ".1f", ".1f", ".0e"],  # Tc
            [".2f", ".2f", "+.0f", ".2f", ".2f", ".1f", ".0e"],  # RDDMax
            [".1f", ".1f", "+.0f", ".1f", ".1f", ".1f", ".0e"],  # RDDMaxTime
            ]

    with open(output_file, 'w') as writer:

        # Used to record which file the table was generated as a comment in the
        # table's LaTeX source code.
        if comment is not None:  
            writer.write('% {}\n'.format(comment))

        writer.write('\\begin{tabular}{|l|c|c|c|c|c|c|c|}')
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.2ex}} \\hspace{-7pt}')
        writer.write('\n    ')

        # Used to add a brief title indicating the subject and set(s) from
        # which the table was generated that is visible in the compiled tabled.
        if table_title is not None:  
            writer.write('\\textbf{{{}}}'.format(table_title))

        writer.write(' & $ \\mu_{\\text{pre}} $ & $ \\mu_{\\text{post}} $ & change & $ \\sigma_{\\text{pre}} $ & $ \\sigma_{\\text{post}} $ & $ \\lvert t \\rvert $ & $ p $ \\\\[0.3ex]')
        writer.write('\n    ')
        writer.write('\\hline {\\rule{0pt}{2.5ex}} \\hspace{-7pt}')
        writer.write('\n    ')

        for i, p in enumerate(param_indices):  # loop through all TMG parameters
            writer.write(printable_param_names[i])
            for j, stat in enumerate(tmg_stats[p, :]):  # loop through all parameter stats
                if j == 2:  # add percent sign to percent difference
                    writer.write(" & $ {0:{1}} \% $ ".format(stat, formats[i][j]))
                elif j == 5:  # take absolute value of t-statistic
                    writer.write(" & $ {0:{1}} $ ".format(np.abs(stat), formats[i][j]))
                elif j == 6:  # write p value in scientific notation
                    writer.write(" & $ \SI{{{0:{1}}}}{{}} $ ".format(stat, formats[i][j]))
                else:
                    writer.write(" & $ {0:{1}} $ ".format(stat, formats[i][j]))

            writer.write('\\\\\n    ')

        writer.write('\\hline')
        writer.write('\n')
        writer.write('\\end{tabular}')


if __name__ == "__main__":
    make_tmg_param_table_by_subj_by_set()
    make_tmg_param_table_by_subj_across_sets()
    make_tmg_param_table_by_set_across_subj()
