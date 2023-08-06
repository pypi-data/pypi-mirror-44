import pandas as pd
import datetime
import numpy as np
import tzlocal as tzl

local_timezone = tzl.get_localzone()

def decide(data_to_use, cutoff, category_field, category, default_assignment):
    """
    :param data_to_use: data upon which the decision shall take place
    :param cutoff: date to which the assignment needs to be calculated
    :param category_field: field in the dataframe data_to_use that shall be searched within
    :param category: variable, a value that shall be used for evaluation
    :param default_assignment: default assignment category
    :return: assignment
    """

    # initialize dataframe
    df = pd.DataFrame(data=data_to_use)

    # handle cutoff class > initialize cutoff_date as date, if it's a string
    # print('cutoff.__class__.__name__: ', cutoff.__class__.__name__)

    if cutoff.__class__.__name__ == 'str':
        cutoff_date = datetime.datetime.strptime(cutoff, '%Y-%m-%d')
    elif cutoff.__class__.__name__ == 'datetime':
        cutoff_date = cutoff
    elif cutoff.__class__.__name__ == 'Timestamp':
        cutoff_date = datetime.datetime.strptime(str(cutoff), '%Y-%m-%d %H:%M:%S')
    else:
        cutoff_date = datetime.datetime.fromtimestamp(cutoff).isoformat()

    # convert dates
    df['since'] = pd.to_datetime(df['since'])
    df['till'] = pd.to_datetime(df['till'])

    df.sort_values(by=['since', 'till'], inplace=True)

    search = df[
        (df[category_field] == category)
    ]

    # print('search[category_field].size', search[category_field].size)

    if search[category_field].size == 0:
        return default_assignment
    elif search[category_field].size == 1:
        return search.iloc[0].assignment
    else:
        for sa in search.iterrows():
            if sa[1].since is pd.NaT and sa[1].till is pd.NaT:
                # if both are empty, return assignment
                return sa[1].assignment
            elif sa[1].since is pd.NaT and sa[1].till is not pd.NaT:
                # if since is empty, test till and use value if check is ok
                if sa[1].till >= cutoff_date:
                    return sa[1].assignment
            elif sa[1].since is not pd.NaT and sa[1].till is pd.NaT:
                # if till is empty, check since and use that value
                if sa[1].since <= cutoff_date:
                    return sa[1].assignment
            else:
                if sa[1].since <= cutoff_date <= sa[1].till:
                    return sa[1].assignment

        return default_assignment


def calculate_assignment(
        target_df,
        assignment_df,
        target_column_name,
        assignment_lookup_field='oscis',
        lookup_field='person'
):
    """
    Procedure adds new column to dataframe with assignment to team.

    :param target_df: dataframe on which the assignment column shall be calculated
    :param assignment_df: dataframe with assignment to teams
    :param target_column_name: name of the column to be created
    :param assignment_lookup_field: name of the person field in the assignment enumerator
    :param lookup_field: name of the field to read the lookup value field in the enumerator, e.g. person (assignment) field or other
    :return:
    """
    for i in target_df.index:
        target_df.at[i, target_column_name] = decide(
            assignment_df,
            target_df.at[i, 'period'],
            assignment_lookup_field,
            target_df.at[i, lookup_field],
            ''
        )


def fix_assignment_using_bbs(
        bbs_enum_df,
        target_df,
        source_column_name,
        target_column_name,
        bbs_column_name,
        overwrite=False,
        fill_unused_with_source_column_value=False
):

    # create new data column, fill it with empties
    target_df[target_column_name] = ''

    for i in target_df.index:
        # fill only in case when source column value is empty
        source_column_value = target_df.at[i, source_column_name]

        # flag used for decision on proceeding
        proceed_with_write = True

        if overwrite is False and source_column_value is not np.NaN:
            proceed_with_write = False

        # does not overwrite actual value, must set a flag to do that
        if proceed_with_write:
            # find correct value in the enumerator
            new_value_search = bbs_enum_df[
               (bbs_enum_df.index == target_df.at[i, bbs_column_name])
            ]

            # shall not write anything if search returns nothing
            if new_value_search.size == 0:
                # print('nothing found, ask whether to use source column values')
                if fill_unused_with_source_column_value:
                    target_df.at[i, target_column_name] = source_column_value
            else:
                if new_value_search.values[0][0] != '':
                    target_df.at[i, target_column_name] = new_value_search.values[0][0]
                else:
                    pass  # target_df.at[i, target_column_name] = 'no value set in the enum'


def decide_multiple_assignments(target_df, columns_prioritized, new_column_name):
    # work with dataframe object
    target_df = pd.DataFrame(target_df)

    # create new column
    if new_column_name in target_df.columns:
        return
    else:
        target_df[new_column_name] = ''

    # check class, do not allow lists
    if columns_prioritized.__class__.__name__ != 'list':
        raise Exception('Columns passed in not a list.')

    for i in target_df.index:
        for single_column in columns_prioritized:
            if single_column in target_df.columns:
                if target_df.at[i, single_column] is not np.NaN and target_df.at[i, single_column] is not np.nan:

                    if target_df.at[i, single_column] == '':
                        pass  # print('empty value', 'single_column', single_column, 'row', i, 'switching to another column')
                    else:
                        pass  # print(single_column, i, 'value:', target_df.at[i, single_column])

                        target_df.at[i, new_column_name] = target_df.at[i, single_column]
                        break

def convert_epoch_to_datetime(epochTime):
    if np.isnan(epochTime):
        return epochTime
    else:
        return datetime.fromtimestamp(int(epochTime)/1000, local_timezone).strftime("%Y-%m-%d")