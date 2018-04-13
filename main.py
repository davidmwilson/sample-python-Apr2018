'''
Author:         David Wilson
Date:           Apr 13th 2018
Description:    example python program showing data reading / cleaning / manipulation
'''
import pandas as pd
import helper

#pylint: disable=pointless-string-statement
def main():
    '''
    main
    '''
    source_url = "https://storage.googleapis.com/coderpad/"
    # for debugging purposes
    use_local_file = 0
    if use_local_file:
        # replace with your local directory as approprioate
        insight_data = helper.populate_data_frame(
            file_name='c:/users/david/appdata/local/temp/data.csv')
        mapping_data = helper.populate_data_frame(
            file_name='c:/users/david/appdata/local/temp/maping.csv')
    else:
        insight_data = helper.populate_data_frame(
            url=source_url, file_name='data.csv')
        mapping_data = helper.populate_data_frame(
            url=source_url, file_name='maping.csv')

    print("{} rows in insight_data".format(len(insight_data)))
    print("{} rows in mapping_data".format(len(mapping_data)))

    '''
    enrich insight data with product names from mapping
    '''
    merged_data = pd.merge(left=insight_data,
                           right=mapping_data, left_on='Product_Code', right_on='ProductCode')
    # now drop the ProductCode column from Mapping data, which we no longer need
    merged_data.drop('ProductCode', axis=1, inplace=True)
    '''
    do some cleaning based on Insight_Score
    While I don't have full clarity on what this value represents
    it seems the vast majority are between -100 and +100
    so, for purposes of illustration I'm going to a very simple filter based on that for now
    '''
    merged_data = merged_data[(merged_data['Insight_Score'] <= 100)
                              & (merged_data['Insight_Score'] >= -100)]
    print("after filtering, {} rows in merged_data".format(len(merged_data)))
    '''
    add zScore to data frame, again I'm looking at Insight_Score
    I then want to identify values with zScore<=3
    '''
    std_devs = 3
    z_score_column = 'Insight_Score'
    merged_data = helper.add_z_score(data_frame=merged_data, column=z_score_column)
    '''
    add outlier boolean based on zscore in excess of given number of std deviations
    '''
    merged_data['outlier'] = merged_data[z_score_column+'_zscore'] > std_devs
    '''
    how many are thus flagged?
    '''
    num_outliers = len(merged_data[merged_data['outlier']])
    print("{} rows in merged_data, {} with zScore > {}".format(
        len(merged_data), num_outliers, std_devs))

    '''
    now calculate max/min insight score by industry
    '''
    helper.find_highest_lowest_period(data_frame=merged_data,
                                      column='Insight_Score', group_by='Industry')

    '''
    show date of lowest insight_score per industry
    '''

    '''
    I wasn't 100% sure data was to be exported, so I'm just doing the merged data set
    that's the insight / mapping data joined by product code to get product name etc
    '''
    helper.write_data_frame(data_frame=merged_data, file_name='datanew.csv')

# when this is called on own, invoke main
if __name__ == "__main__":
    main()
