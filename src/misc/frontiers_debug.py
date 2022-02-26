import numpy as np
import matplotlib.pyplot as plt
import spm1d

import utilities
import spm_analysis
import preprocessing
import plotting
import constants

"""
Collection of functions used for debugging in the context of the analysis
for the potentiation paper for the Frontiers journal.
"""
# subject, sets, max_rows
def plot_subject(subject_id, skiprows=2, max_rows=100, sets=None, normed=False, 
        plot_pre=True):
    """
    Parameters
    ----------
    subject_id : int
        1-based index used to identify subject 
        (instead of passing in the subject's entire string name).
        1 corresponds to "1-BR20200910125909", for example.
    max_rows : int
        Passed to Numpy's `loadtxt` function as the `max_rows` parameter
        to select which rows to read from the subject's measurement file.
    sets : tuple
        A tuple containing any or all of (1, 2, 3, 4).
        Passed to Numpy's `loadtxt` function as the `usecols` parameter
        to select which sets to read from the subject's measurement file.
    normed : bool
        Whether to use raw or normalized data.
    plot_pre : bool
        Set to True to plot pre-exercise data.
        Set to False to post pre-exercise data.
    
    """
    if normed:
        data_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm_normed/"
    else:
        data_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm/"

    subject_name = get_subject_name_from_id(subject_id)

    if plot_pre:
        filename = data_dir + "pre-exercise/{}-pre.csv".format(subject_name)
    else:
        filename = data_dir + "post-exercise/{}-post.csv".format(subject_name)

    data = np.loadtxt(filename, delimiter=',', skiprows=skiprows,
            max_rows=max_rows, usecols=sets)
    
    if len(sets) == 1:
        plt.plot(data)
    else:
        for s in sets:
            tmg = data[:, s]
            plt.plot(tmg)


def athlete_test():
    subject = "43-VT20210317105103"
    pre_file = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm/pre-exercise/{}-pre.csv".format(subject)
    post_file = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm/post-exercise/{}-post.csv".format(subject)
    skiprows = 2
    max_sets = 4
    max_rows = 100
    pre_data = np.loadtxt(pre_file, delimiter=',',
            skiprows=skiprows, max_rows=max_rows)
    post_data = np.loadtxt(post_file, delimiter=',',
            skiprows=skiprows, max_rows=max_rows)
    pre_data, post_data = preprocessing.fix_false_spm_significance(pre_data, post_data)
    t, ti = spm_analysis.get_spm_ti(pre_data, post_data)

    # ti.plot()

    # spm_param_output_file = spm_param_output_dir + "subject{}-spm-params.csv".format(a + 1)

    # param_df = spm_analysis.get_ti_parameters_as_df(ti)
    # param_df.to_csv(spm_param_output_file)

    # # (zero-based) first row of TMG data that is read from CSV files
    # # In practice only zero-th row of TMG data is skipped.
    tmg_data_start_row = constants.TMG_DATA_START_ROW_FOR_SPM
    plotting.plot_spm_ttest(t, ti, pre_data, post_data,
            tmg_data_start_row, "",
            show_plot=True, save_figures=False)

    # from matplotlib import pyplot

    # pre_data = pre_data.T
    # post_data = post_data.T
    # t  = spm1d.stats.ttest2(pre_data, post_data, equal_var=False)
    # ti = t.inference(alpha=0.05, two_tailed=False, interp=True)

    # pyplot.close('all')
    # ### plot mean and SD:
    # pyplot.figure( figsize=(8, 3.5) )
    # ax     = pyplot.axes( (0.1, 0.15, 0.35, 0.8) )
    # spm1d.plot.plot_mean_sd(pre_data)
    # spm1d.plot.plot_mean_sd(post_data, linecolor='r', facecolor='r')
    # ax.axhline(y=0, color='k', linestyle=':')
    # ax.set_xlabel('Time (%)')
    # ax.set_ylabel('Plantar arch angle  (deg)')
    # ### plot SPM results:
    # ax     = pyplot.axes((0.55,0.15,0.35,0.8))
    # ti.plot()
    # ti.plot_threshold_label(fontsize=8)
    # ti.plot_p_values(size=10, offsets=[(0,0.3)])
    # ax.set_xlabel('Time (%)')
    # pyplot.show()
    # plt.show()



def get_subject_name_from_id(subject_id):
    """
    Input a 1-based integer index.
    Return a string holding the subject's name as used in the project.
    1 corresponds to "1-BR20200910125909", for example.

    """
    names = ["1-BR20200910125909", 
            "2-SZ20200901134322", 
            "3-EM20200901124828", 
            "4-SD20200901145937", 
            "5-SK20200901142319", 
            "6-SD20200929090956", 
            "7-SK20200929095140", 
            "8-NF20200929102126", 
            "9-MM20200929105429", 
            "10-MK20200929112805",
            "11-JJ20200929120454",
            "12-JZ20200924121704",
            "13-ZI20200924091029",
            "14-VT20200924094806",
            "15-MK20200924102106",
            "16-LR20200924113647",
            "18-JL20200910100638",
            "19-MC20200910105450",
            "20-MS20200910112714",
            "21-SR20200910121233",
            "23-AL20201014125345",
            "24-ME20201104141336",
            "26-FD20201105113904",
            "30-BB20210312101025",
            "31-EM20210312111435",
            "32-JZ20210312131656",
            "33-SD20210312121833",
            "34-SK20210312114610",
            "35-SR20210312124932",
            "36-SZ20210312103958",
            "37-AL20210317133110",
            "38-IF20210317130746",
            "39-JL20210317121435",
            "40-MM20210317111914",
            "41-NF20210317114800",
            "42-NU20210317124142",
            "43-VT20210317105103",
            "44-ZI20210317135522",
            "45-KB20210621084346",
            "46-AM20210621092253",
            "47-JD20210621100050",
            "48-IP20210621104314",
            "49-NB20210621112423",
            "50-AK20210621120651",
            "51-OB20210621124708",
            "52-AL20211112131130",
            "53-MM20211112111608",
            "54-ZI20211112121510",
            "55-SD20211214101158",
            "56-JL20211210115356",
            "57-NF20211210105845",
            "58-NU20211210123108",
            "59-FD20211220140045",
            "60-GG20211223134841",
            "61-AG20211210130200"]
    if subject_id < len(names):
        return names[subject_id - 1]
    else:
        print("Error: subject does not exist.")
        return None
    

def subject_test():
    subject_id = 1
    # sets = [ 0, 1, 2, 3 ]
    sets = [ 0 ]
    skiprows = 2
    max_rows = 100
    normed = True
    plot_pre = True

    plot_subject(subject_id, max_rows=max_rows, sets=sets, 
            normed=normed, plot_pre=True)
    plot_subject(subject_id, max_rows=max_rows, sets=sets, 
            normed=normed, plot_pre=False)
    plt.show()

if __name__ == "__main__":
    subject_test()
