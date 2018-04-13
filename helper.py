'''
helper functions
'''
import os
import tempfile
import requests
import pandas as pd

DEBUG = 0

def populate_data_frame(url=None, file_name=None):
    '''
    create and populate a pandas data frame, sourced wither
    from a url / filename or just local file
    '''
    tmp_dir = tempfile.gettempdir()
    if url != None:
        # todo: add error checking / exception handling
        response = requests.get(url+file_name)
        data_file_name = os.path.join(tmp_dir, file_name)
        if DEBUG:
            print("dataFileName response from {}{} to {}".format(url, file_name, data_file_name))
        with open(data_file_name, "wb") as data_file:
            data_file.write(response.content)
    else:
        # we are reading from file param, not url
        data_file_name = file_name

    if DEBUG:
        print("populating dataframe from  {}".format(data_file_name))

    data_frame = pd.read_csv(data_file_name, sep=",")
    return data_frame

def write_data_frame(data_frame=None, file_name=None, output_dir=tempfile.gettempdir()):
    '''
    write data frame to csv file, if no output_dir specified
    the defined temp dir is used
    '''
    output_file = os.path.join(output_dir, file_name)
    data_frame.to_csv(output_file)

def add_z_score(data_frame=None, column=None):
    '''
    implement simple z-score type outlier detection.
    Take the value, subtract average and divide by stddev to get zscore
    (which is basically number of stddevs from mean)
    '''
    # no error checking here, assumption is that column exists
    avg = data_frame[column].mean()
    stddev = data_frame[column].std()
    # add zscore column for later reference
    data_frame[column+'_zscore'] = abs(data_frame[column]-avg)/stddev
    return data_frame

def find_most_correlated_industries(data_frame=None, column=None):
    '''
    find highesst correlated industries by column
    '''
    correlation = data_frame.corr()

def find_highest_lowest_period(data_frame=None, column=None, group_by=None):
    '''
    find period containing highest / lowest values of given column, grouped

    there is probably a better way to do this, but time is running out :)
    '''
    # get left hand side frame, industry / date of lowest column value
    min_side = data_frame.loc[data_frame.groupby(group_by)[column].idxmin()][[group_by, 'Period', column]]
    min_side.rename(columns={'Period': 'Date of Lowest', column: 'Lowest'}, inplace=True)
    # get right hand side frame, industry / date of highest column value
    max_side = data_frame.loc[data_frame.groupby(group_by)[column].idxmax()][[group_by, 'Period', column]]
    max_side.rename(columns={'Period': 'Date of Highest', column: 'Highest'}, inplace=True)
    # now join on group by column
    data = pd.merge(left=min_side, right=max_side,
                    left_on=group_by, right_on=group_by)
    print("\n\nPeriod of highest / lowest {}, by {}".format(column, group_by))
    print(data)
    print("\n\n")
