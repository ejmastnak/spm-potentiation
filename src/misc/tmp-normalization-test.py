import numpy as np
from matplotlib import pyplot as plt

subject_num = 8

# Srdjan version
# --------------------------------------------- #
normed_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/sent/"
normed_pre_file = normed_dir + "pre/1.csv"
normed_post_file = normed_dir + "post/1.csv"

normed_data_pre = np.loadtxt(normed_pre_file, delimiter=',')
normed_data_post = np.loadtxt(normed_post_file, delimiter=',')

x_pre = normed_data_pre[:, subject_num]
x_post = normed_data_post[:, subject_num]

plt.plot(x_pre)
plt.plot(x_post)
# --------------------------------------------- #
normed_dir = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv_for_spm_normed/"
normed_pre_file = normed_dir + "pre/1.csv"
normed_post_file = normed_dir + "post/1.csv"

normed_data_pre = np.loadtxt(normed_pre_file, delimiter=',')
normed_data_post = np.loadtxt(normed_post_file, delimiter=',')

x_pre = normed_data_pre[:, subject_num]
x_post = normed_data_post[:, subject_num]

plt.plot(x_pre, linestyle='--')
plt.plot(x_post, linestyle='--')

plt.show()
