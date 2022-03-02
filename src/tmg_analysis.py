import pandas as pd

def get_params_of_tmg_file(input_dir, xlsx_filename, output_dir,
        column_mode, base_msmts=1, pot_msmts=1, max_set=8):
    """
    Computes the TMG and RDD parameters of for the raw TMG measurements
    stored in a standard TMG Excel measurement file.
    See documentation of conversion constants in `constants.py`.

    Parameters
    ----------
    input_dir : str
        Parent directory holding the TMG Excel file
    xlsx_filename : str
        File name of the Excel file, excluding full path but including extension
    output_dir : str
        Output directory in which to write parameter files CSV files
    column_mode : int
        One of the conversion mode constants documented in `constants.py`
    base_msmts : int
        The number of baseline measurements per set in the Excel file
    pot_msmts : int
        The number of potentiated measurements per set in the Excel file
    max_set : int
        Ignore sets in Excel file above this set number.

    """
    xlsx_file = input_dir + xlsx_filename
    subject_id = io_utils.get_subject_ID_from_filename(xlsx_filename)

    # Read measurements from Excel file into a pandas dataframe
    df = io_utils.xlsx_to_pandas_df(xlsx_file)

    n_cols = df.shape[1]
    msmts_per_set = base_msmts + pot_msmts
    sets = n_cols/msmts_per_set

    if not sets.is_integer():
        print("Error: Non-integer number of measurements per sets.")
        print("Aborting")
        return
    else:
        sets = int(sets)

    col_names = []
    row_names = constants.TMG_PARAM_NAMES

    # First add parameters to a list, then create a DataFrame from the list
    param_list = []

    if column_mode == constants.VERBATIM:
        # Loop through each measurement number and TMG signal in Excel file
        for (m, tmg) in df.iteritems():

            # Determine if measurement is baseline or potentiated
            if 1 <= m % (msmts_per_set) <= base_msmts:  # baseline
                base_pot = "B"
            else:  # potentiated
                base_pot = "P"

            # Set and measurement number of each measurement
            col_names.append("ID{}-S{}-M{}-{}".format(subject_id, 
                int((m - 1)/msmts_per_set) + 1, m, base_pot))

            params = get_params_of_tmg_signal(tmg.to_numpy())
            param_list.append(params)

        param_df = pd.DataFrame(param_list).transpose()
        param_df.columns=col_names
        param_df.index=row_names
        param_df.to_csv(output_dir + xlsx_filename.replace(".xlsx", "-rdd-params.csv"))

    elif column_mode == constants.PRE_POST_BY_SET_FIRST_REP:
        for set in range(1, sets + 1):
            if set > max_set:
                break

            base_col = df.iloc[:, (set - 1) * msmts_per_set]
            col_names.append("ID{}-S{}-M{}-B".format(subject_id, set, base_col.name))
            params = get_params_of_tmg_signal(base_col.to_numpy())
            param_list.append(params)

            pot_col = df.iloc[:, (set - 1) * msmts_per_set + base_msmts]
            col_names.append("ID{}-S{}-M{}-P".format(subject_id, set, pot_col.name))
            params = get_params_of_tmg_signal(pot_col.to_numpy())
            param_list.append(params)

        param_df = pd.DataFrame(param_list).transpose()
        param_df.columns=col_names
        param_df.index=row_names
        param_df.to_csv(output_dir + xlsx_filename.replace(".xlsx", "-rdd-params.csv"))
