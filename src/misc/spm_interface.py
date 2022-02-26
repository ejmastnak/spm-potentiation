from pathlib import Path
import os
import traceback
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np

import analysis
import shape_accomodation
import data_processing
import plotting

"""
This script revolves around comparing pre-exercise and post-exercise data.
The following naming convention appears throughout:
    - Variables and functions applying to pre-exercise data are prefixed with "pre_"
    - Variables and functions applying to post-exercise data are prefixed with "post_"
"""

class SPMInterface:

    def __init__(self, pre_filename=None, post_filename=None):
        """
        For now includes filename parameters as a hacky way to load data automatically on startup for testing
        """
        self.pre_filename = ""  # name of file holding pre-exercise data
        self.post_filename = ""  # name of file holding post-exercise data
        self.pre_data = np.zeros(shape=(0, 0))  # e.g. 1000 x 10
        self.post_data = np.zeros(shape=(0, 0))  # e.g. 1000 x 10
        self.new_data = True

        # START TKINTER WIDGETS
        self.root_window = tk.Tk()
        self.root_window.title("SPM 1D Analysis Interface")

        # create frames here
        self.rootframe = ttk.Frame(self.root_window, padding=(3, 12, 3, 12))
        self.textarea_frame = ttk.Frame(self.rootframe)  # panel to hold text areas
        self.controlframe = ttk.Frame(self.rootframe)  # panel to hold controls

        # Pre-exercise data window
        self.pre_label = ttk.Label(self.textarea_frame, text="Pre-exercise data")
        self.pre_scroll = ttk.Scrollbar(self.textarea_frame)
        self.pre_text_area = tk.Text(self.textarea_frame, height=5, width=52)
        self.pre_scroll.config(command=self.pre_text_area.yview)
        self.pre_text_area.config(yscrollcommand=self.pre_scroll.set)
        self.pre_text_area.insert(tk.END, "No data imported")
        self.pre_text_area.configure(state='disabled')

        # Post-exercise data window
        self.post_label = ttk.Label(self.textarea_frame, text="Post-exercise data")
        self.post_scroll = ttk.Scrollbar(self.textarea_frame)
        self.post_text_area = tk.Text(self.textarea_frame, height=5, width=52)
        self.post_scroll.config(command=self.post_text_area.yview)
        self.post_text_area.config(yscrollcommand=self.post_scroll.set)
        self.post_text_area.insert(tk.END, "No data imported")
        self.post_text_area.configure(state='disabled')

        # SPM analysis results window
        self.spm_label = ttk.Label(self.textarea_frame, text="SPM analysis results")
        self.spm_scroll = ttk.Scrollbar(self.textarea_frame)
        self.spm_text_area = tk.Text(self.textarea_frame, height=7, width=52)
        self.spm_scroll.config(command=self.spm_text_area.yview)
        self.spm_text_area.config(yscrollcommand=self.spm_scroll.set)
        self.spm_text_area.insert(tk.END, "No analysis results")
        self.spm_text_area.configure(state='disabled')

        # create control widgets
        self.import_post_button = ttk.Button(self.controlframe, text="Import post-exercise data", command=self.import_post_data)
        self.import_pre_button = ttk.Button(self.controlframe, text="Import pre-exercise data", command=self.import_pre_data)
        self.compare_button = ttk.Button(self.controlframe, text="Compare", command=self.compare)
        self.export_curve_button = ttk.Button(self.controlframe, text="Export t Curve", command=self.export_tcurve)
        self.export_params_button = ttk.Button(self.controlframe, text="Export t Parameters", command=self.export_tparams)
        self.close_button = ttk.Button(self.controlframe, text="Exit", command=self.close)

        # gridding subframes
        self.rootframe.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))  # place the root frame

        self.textarea_frame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))  # place textarea frame
        self.controlframe.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))  # place control frame

        # gridding text area frame
        self.pre_label.grid(column=0, row=1)
        self.pre_scroll.grid(column=1, row=2, sticky=tk.W)
        self.pre_text_area.grid(column=0, row=2, sticky=tk.W)

        self.post_label.grid(column=0, row=3)
        self.post_scroll.grid(column=1, row=4, sticky=tk.W)
        self.post_text_area.grid(column=0, row=4, sticky=tk.W)

        self.spm_label.grid(column=0, row=5)
        self.spm_scroll.grid(column=1, row=6, sticky=tk.W)
        self.spm_text_area.grid(column=0, row=6, sticky=tk.W)

        # gridding control frame
        self.import_pre_button.grid(column=0, row=0, sticky=tk.W)
        self.import_post_button.grid(column=0, row=1, sticky=tk.W)
        self.compare_button.grid(column=0, row=2, sticky=tk.W)
        self.export_curve_button.grid(column=0, row=3, sticky=tk.W)
        self.export_params_button.grid(column=0, row=4, sticky=tk.W)
        self.close_button.grid(column=0, row=5, sticky=tk.W)

        # configure weights
        self.root_window.columnconfigure(0, weight=1)
        self.root_window.rowconfigure(0, weight=1)

        self.rootframe.columnconfigure(0, weight=1)  # control frame
        self.rootframe.rowconfigure(0, weight=1)

        # for loading data programtically (and not via gui) when testing
        if pre_filename is not None and post_filename is not None:
            self.set_pre_data(pre_filename)
            self.set_post_data(post_filename)

        self.root_window.mainloop()
        # END TKINTER WIDGETS

    @ staticmethod
    def get_data_description(filename, data):
        """
        Used to get a string description of imported pre/post exercise data
        to display in the GUI, to give the user a description of the file they've imported

        :param filename: full path to a file containing measurement data
        :param data: 2D numpy array holding the data measurement data; rows are data samples and columns are measurement sets
        """

        file_string = "Filename: " + Path(filename).name
        dim_string_1 = "Dimensions: {} rows by {} columns".format(data.shape[0], data.shape[1])
        dim_string_2 = "({} measurements of {} points per measurement)".format(data.shape[1], data.shape[0])
        path_string = "Location: " + os.path.dirname(filename)
        return file_string + "\n" + dim_string_1 + "\n" + dim_string_2 + "\n" + path_string

    @ staticmethod
    def set_imported_data_description(text_widget, text_content):
        """
        Wrapper method for protocol of setting data text widget info content
        Used with to give the user a description of the data they've imported
        And to give an overview of SPM analysis results
        """
        text_widget.configure(state='normal')
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, text_content)
        text_widget.configure(state='disabled')

    # START GUI WIDGET ACTION FUNCTIONS
    # --------------------------------------------- #
    def import_pre_data(self):
        """
        Implements the protocol for importing pre-exercise measurement data.
        This method is set as the action for the import_pre_button widget.
        """
        # Get csv files with file chooser dialog
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        # Catch null filename on cancelled dialog
        if filename:  
            try:
                self.pre_data = np.loadtxt(filename, delimiter=",", 
                        skiprows=constants.start_row, max_rows=constants.max_rows)
                data_processing.process_pre_data()
                self.set_imported_data_description(self.pre_text_area,
                        self.get_data_description(filename, self.pre_data))
                self.pre_filename = filename

    # TODO: fix false significance
    # if self.post_data is not None:  # if active data has been set
    #     # fix potential false SPM significance region problems
    #     pre_data, self.post_data = shape_accomodation.fix_false_spm_significance(pre_data, self.post_data)

            except Exception as e:
                print("Error importing pre-exercise data: " + str(e))
                traceback.print_tb(e.__traceback__)
                return

    def import_post_data(self):
        """
        Analogous to import_pre_data above.
        """
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                self.post_data = np.loadtxt(filename, delimiter=",", 
                        skiprows=constants.start_row, max_rows=constants.max_rows)
                data_processing.process_post_data()
                self.set_imported_data_description(self.post_text_area,
                        self.get_data_description(filename, self.post_data))
                self.post_filename = filename

            except Exception as e:
                print("Error importing post-exercise data: " + str(e))
                return

    def compare(self):
        """
        Action for the "Compare" button, which runs an SPM analysis comparing
        the imported pre and post-exercise data.
        """
        if self.is_import_data_null():  # null data check
            return
        self.reshape_data()  # reshape input data as necessary
        self.plot_test_results()

    def plot_test_results(self):
        """
        Plots the pre/post exercise data's mean and standard deviation clouds on axis 0.
        Plots the SPM t-test between the pre and post-exercise data on axis 1.
        """
        try:
            t, ti = analysis.get_spm_ti(self.pre_data, self.post_data)  # try getting t an ti objects
        except Exception as e:
            print("Error performing SPM analysis: " + str(e))
            return

        self.set_imported_data_description(self.spm_text_area,
                analysis.get_spm_ti_string_description(ti, time_offset=self.get_time_offset()))
        plotting.plot_spm_ttest(t, ti, self.pre_data, self.post_data,
                time_offset=self.get_time_offset(),
                figure_output_path=Path(self.post_filename).name.replace(".csv", ".png"))

    def export_tcurve(self, *args):  # used to write an output file
        """
        Action for the export t-curve button widget.
        Export the t-statistic as a 2D array to a local CSV file.
        First column is time, second is t-statistic
        """
        if self.is_import_data_null():  # null data check
            return

        try:
            t = analysis.get_spm_t(self.pre_data, self.post_data)  # try getting t object
        except Exception as e:
            print("Error performing SPM analysis: " + str(e))
            return

        analysis.export_t_curve(t, time_offset=self.get_time_offset())

    def export_tparams(self, *args):  # used to write an output file
        """
        Action for the export parameters button widget.
        Exports various ti object parameters to a local csv file in tabular format
        """
        if self.is_import_data_null():  # null data check
            return

        try:
            _, ti = analysis.get_spm_ti(self.pre_data, self.post_data)  # try getting t an ti objects
        except Exception as e:
            print("Error performing SPM analysis: " + str(e))
            return

        analysis.export_ti_parameters(ti, time_offset=self.get_time_offset(),
                                      baseline_filename=self.pre_filename,
                                      active_filename=self.post_filename)

    def close(self):
        """
        Action for the close button widget.
        Closes the current SPM window and exits the program
        """
        self.root_window.destroy()
        tk.sys.exit()
    # --------------------------------------------- #
    # END GUI WIDGET ACTION FUNCTIONS

    def set_pre_data(self, pre_filename):
        """
        Action to programatically set pre-exercise data.
        Implements the protocol for importing pre-exercise data.
        """
        # Only continue if a file is chosen; avoids null filename on cancel click.
        if pre_filename:  
            try:
                self.pre_data = np.loadtxt(pre_filename, delimiter=",", 
                        skiprows=constants.start_row, max_rows=constants.max_rows)
                data_processing.process_pre_data()  # process imported data
                self.set_imported_data_description(self.pre_text_area,
                        self.get_data_description(pre_filename, self.pre_data))
                # If import is successful, set filename
                self.pre_filename = pre_filename

            except Exception as e:
                print("Error importing pre-exercise data: " + str(e))
                traceback.print_tb(e.__traceback__)
                return

    def set_post_data(self, post_filename):
        """
        Action to programatically set active data.
        Implements the protocol for importing post-exercise data.
        """
        if post_filename:
            try:
                self.post_data = np.loadtxt(post_filename, delimiter=",", 
                        skiprows=constants.start_row, max_rows=constants.max_rows)
                data_processing.process_post_data(self.pre_data)
                self.set_imported_data_description(self.post_text_area, 
                        self.get_data_description(post_filename, self.post_data))
                self.post_filename = post_filename

            except Exception as e:
                print("Error importing post-exercse data: " + str(e))
                traceback.print_tb(e.__traceback__)
                return

    def is_import_data_null(self):
        """
        Used as a null check for imported data.
        Returns true (data is null) if there are either no rows or
         no columns in either of pre-exercise and active data arrays.

        e.g. pre_data.shape = (0, 100) and post_data.shape = (10, 100) returns true (data is null)
        """
        pre_shape = self.pre_data.shape
        post_shape = self.post_data.shape

        pre_rows = pre_shape[0]
        pre_cols = pre_shape[1]
        post_rows = post_shape[0]
        post_cols = post_shape[1]

        # Quick way to check if any of the values are zero
        if pre_rows*pre_cols*post_rows*post_cols == 0:
            return True
        else:
            return False

    def reshape_data(self):
        """ Reshapes imported measurement data, if necessary, into a format compatible with spm1d """

        pre_shape = self.pre_data.shape
        post_shape = self.post_data.shape

        pre_rows = pre_shape[0]
        pre_cols = pre_shape[1]
        post_rows = post_shape[0]
        post_cols = post_shape[1]

        # Same number columns, different number of rows
        if pre_rows != post_rows and pre_cols == post_cols:  
            self.pre_data, self.post_data = shape_accomodation.match_rows(self.pre_data, self.post_data, pre_rows, post_rows)

        # Same number rows, different number columns
        elif pre_rows == post_rows and pre_cols != post_cols:  
            self.pre_data, self.post_data = shape_accomodation.match_cols(self.pre_data, self.post_data, pre_rows, pre_cols, post_rows, post_cols)

        # Different number of rows AND different number of columns
        elif pre_shape != post_shape:  
            self.pre_data, self.post_data = shape_accomodation.match_rows(self.pre_data,
                    self.post_data, pre_rows, post_rows)
            self.pre_data, self.post_data = shape_accomodation.match_cols(self.pre_data,
                    self.post_data, pre_rows, pre_cols, post_rows, post_cols)

        if pre_cols == 1 and post_cols == 1:
            self.pre_data, self.post_data = shape_accomodation.increase_cols(self.pre_data, self.post_data, pre_rows, pre_cols, post_rows, post_cols)

def get_spm_ti_string_description(ti, time_offset=0):
    """
    Returns a string description of an SPM TI inference object's important parameters, e.g. start time, centroid, etc...
    Used to provide a string description of SMP inference results in the GUI
    :param ti: An SPM TI inference object
    :param time_offset: integer [milliseconds] to correct for potentially changing SPM start time
    """

    # Start header
    # Potentiated file,"filename"
    # Potentiated file,"filename"
    # Alpha,
    # T-star,
    # # End header
    # Parameter,Cluster,Cluster

    analysis_string = "Alpha: {:.2f}".format(ti.alpha)  # alpha value
    analysis_string += "\nThreshold: {:.2f}".format(ti.zstar)  # threshold t-statistic value
    clusters = ti.clusters  # portions of curve above threshold value
    threshold = ti.zstar
    if clusters is not None:
        for i, cluster in enumerate(clusters):
            tstart, tend = cluster.endpoints  # start and end time of each cluster
            tstart += time_offset  # add potential time offset
            tend += time_offset
            x, z = cluster._X, cluster._Z  # x and z (time and t-statistic) coordinates of the cluster
            z_max = np.max(z)  # max value of t-statistic in this cluster
            N = len(x)  # number of points in this cluster
            A = 0.0  # area under curve
            for k in range(1, N, 1):  # i = 1, 2, ..., N
                A += np.abs(0.5*(z[k] + z[k-1]))*(x[k] - x[k-1])  # midpoint formula
            A_threshold = A - (threshold * (x[-1] - x[0]))  # subtract area below threshold (threshold * interval length)

            cluster_string = "\n" + 50*"-"  # draws a bunch of dashes i.e. ----------
            cluster_string += "\nSignificance Region {}".format(i+1)  # include a newline character
            cluster_string += "\nProbability: {:.2e}".format(cluster.P)
            cluster_string += "\nProbability (decimal): {:.4f}".format(cluster.P)
            cluster_string += "\nStart: {:.2f}\t End: {:.2f}".format(tstart, tend)
            cluster_string += "\nCentroid: ({:.2f}, {:.2f})".format(cluster.centroid[0] + time_offset, cluster.centroid[1])
            cluster_string += "\nMaximum: {:.2f}".format(z_max)
            cluster_string += "\nArea Above Threshold: {:.2f}".format(A_threshold)
            cluster_string += "\nArea Above x Axis: {:.2f}".format(A)
            analysis_string += cluster_string
    return analysis_string


# Begin functions used to write data to CSV files
# --------------------------------------------- #
def export_t_curve(t, time_offset=0):
    """
    Exports the SPM t statistic as a function of time to a local csv file chosen by the user
    Assumes 1 kHz sampling of data! (as is standard for TMG measurements)
    :param t: 1D numpy array containing an SPM t statistic
    :param time_offset: integer [milliseconds] to correct for potentially changing SPM start time
    """
    try:
        filename = filedialog.asksaveasfilename(filetypes=[("CSV files", "*.csv")])
        if filename is None or filename == "":  # in case export was cancelled
            return
        if not filename.endswith(".csv"):  # append .csv extension, unless user has done so manually
            filename += ".csv"
        time = np.arange(0, len(t.z), 1)  # assumes 1 kHz sampling, i.e. 1ms per sample. Time reads 0, 1, 2, ...
        time += time_offset  # add potential time offset
        header = "Time [ms], SPM t-statistic"
        np.savetxt(filename, np.column_stack([time, t.z]), delimiter=',', header=header)

    except Exception as e:
        print("Error performing exporting SPM data: " + str(e))
        return


def export_ti_parameters(ti, time_offset=0, pre_filename="", post_filename="", output_file_path=None):
    """
    Exports various ti object parameters to a local csv file in tabular format
    :param ti: An SPM TI inference object
    :param time_offset: integer [milliseconds] to correct for potentially changing SPM start time
    :param pre_filename: name of pre-exercise data file, just for reference in the exported information
    :param pos_filename: name of post-exercise data file, just for reference in the exported information
    :param output_file_path: full path for output file. If None, a GUI file chooser is used instead.
    """
    try:
        if output_file_path is None:  # use GUI file chooser to determine output file path if no path specified
            output_file_path = filedialog.asksaveasfilename(filetypes=[("Text files", "*.csv")])
            if output_file_path is None or output_file_path == "":  # in case export was cancelled
                return
            if not output_file_path.endswith(".csv"):  # append .csv extension, unless user has done so manually
                output_file_path += ".csv"

        # Print file header
        metadata = "# START HEADER\n"
        metadata += "# Pre-exercise file,{}\n".format(Path(pre_filename).name)
        metadata += "# Post-exercise file,{}\n".format(Path(post_filename).name)
        metadata += "# Alpha,{:.2f}\n".format(ti.alpha)  # alpha value
        metadata += "# Threshold,{:.2f}\n".format(ti.zstar)  # threshold t-statistic value
        metadata += "# END HEADER\n"

        with open(output_file_path, 'w') as output:  # open file for writing
            output.write(metadata)  # write metadata

            clusters = ti.clusters  # portions of curve above threshold value
            threshold = ti.zstar

            if clusters is None:  # catch possibility that threshold is not exceeded
                output.write("Significance threshold not exceeded.")
            else:

                # Create header string of the form "# Parameter,Cluster 1,Cluster 2, ..."
                header = "# Parameter"
                for i in range(len(clusters)):
                    header += ",Cluster {}".format(i + 1)
                header += "\n"  # add new line
                output.write(header)  # write header

                # Assign each outputted parameter a row; pack into an array for easier printing to file
                param_strs = ["Probability",  # probability for threshold in exponent (scientific) notation
                              "Probability (decimal)",  # probability as a float
                              "Start Time [ms]",
                              "End Time [ms]",
                              "Centroid Time [ms]",
                              "Centroid t-value",
                              "Maximum",
                              "Area Above Threshold",
                              "Area Above x Axis"]

                for i, cluster in enumerate(clusters):  # loop through significance clusters
                    tstart, tend = cluster.endpoints  # start and end time of each cluster
                    tstart += time_offset  # add potential time offset
                    tend += time_offset

                    x, z = cluster._X, cluster._Z  # x and z (time and t-statistic) coordinates of the cluster
                    z_max = np.max(z)  # max value of t-statistic in this cluster
                    N = len(x)  # number of points in this cluster
                    A = 0.0  # area under curve
                    for k in range(1, N, 1):  # i = 1, 2, ..., N
                        A += np.abs(0.5*(z[k] + z[k-1]))*(x[k] - x[k-1])  # midpoint formula
                    # subtract area below threshold (threshold * interval length)
                    A_threshold = A - (threshold * (x[-1] - x[0]))

                    param_strs[0] += ",{:.2e}".format(cluster.P)
                    param_strs[1] += ",{:.4f}".format(cluster.P)
                    param_strs[2] += ",{:.2f}".format(tstart)
                    param_strs[3] += ",{:.2f}".format(tend)
                    param_strs[4] += ",{:.2f}".format(cluster.centroid[0] + time_offset)
                    param_strs[5] += ",{:.2f}".format(cluster.centroid[1])
                    param_strs[6] += ",{:.2f}".format(z_max)
                    param_strs[7] += ",{:.2f}".format(A_threshold)
                    param_strs[8] += ",{:.2f}".format(A)

                # print parameter strings---this is where it's useful the strings are in an array
                for i, param_str in enumerate(param_strs):
                    output.write(param_str)  # write header
                    if i < len(param_strs):  # don't print new line for last string at end of file
                        output.write("\n")

    except Exception as e:
        print("Error exporting SPM parameters: " + str(e))
        traceback.print_exception(type(e), e, e.__traceback__)
        return
# --------------------------------------------- #
# End functions used to write data to CSV files


def gui_launch():
    interface = SPMInterface()


def development_launch():
    # load data programatically for development use
    data_dir = "/home/ej/Media/tmg-bmc-media/measurements/spm-measurements/spm-measurements/spm_1_9_2020/sd/"
    base_filename = data_dir + "sd_base.csv"
    pot_filename = data_dir + "sd_pot.csv"
    interface = SPMInterface(pre_filename=base_filename, post_filename=pot_filename)


if __name__ == "__main__":
    # gui_launch()
    development_launch()
    # practice()
