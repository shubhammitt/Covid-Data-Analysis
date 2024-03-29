import json
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# API usage : https://api.covid19india.org/documentation/statedaily.html

states = ['ap', 'ar', 'as', 'br', 'ct', 'ga', 'gj', 'hp',
          'hr', 'jh', 'ka', 'kl', 'mh', 'ml', 'mn', 'mp',
          'mz', 'nl', 'or', 'pb', 'rj', 'sk', 'tg', 'tn',
          'tr', 'up', 'ut', 'wb']
uts = ['an', 'ch', 'dd', 'dl', 'dn', 'jk', 'la', 'ld', 'py']


def string_date_to_standard_date1(date):
    '''
    Args:
        date : in string format, Ex - "2020-03-14"
    return date in datetime.date format so that relational operator works on it
    '''
    try:
        year, mon, date = map(int, date.split('-'))
        return datetime.datetime(year, mon, date)
    except:
        print("Please enter dates in YYYY-MM-DD format!")
        exit(1)


def string_date_to_standard_date2(date):
    '''
    Args:
        date : in string format, Ex - "15-Mar-20"
    return date in datetime.date format so that relational operator works on it
    '''
    try:
        date, mon, year = date.split('-')
        mon_name_to_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
                           'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
                           'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        mon = mon_name_to_num[mon]
        return datetime.datetime(2000 + int(year), mon, int(date))
    except:
        return None


def json_to_df(json_file_path):
    '''
    Args:
        Takes file path of json file
    returns pandas dataframe
    '''
    try:
        with open(json_file_path) as json_file:
            dataset = json.load(json_file)['states_daily']
    except:
        print("File not found!!")
        exit(1)

    # Remove those states from global list which are not in data
    df = pd.DataFrame(dataset)
    for state in states:
        if state not in df.columns:
            states.remove(state)

    # Remove those UT's from global list which are not in data
    for ut in uts:
        if ut not in df.columns:
            uts.remove(ut)

    return df


def remove_useless_cols(df, cols):
    '''
    Args:
        cols - columns which we dont want to drop
    Function:
        remove useless columns from dataframe
    '''
    cols = [col_name for col_name in df.columns if col_name not in cols]
    df.drop(cols, axis=1, inplace=True)


def tranform_df_dates(df, date):
    '''
    Function:
        convert string date to datetime.date in 'date' column
        and if there is some issue while converting than remove that row
    '''
    df[date] = df[date].apply(string_date_to_standard_date2)
    df.dropna(subset=[date], inplace=True)


def remove_useless_rows(df, start_date, end_date):
    '''
    Function:
        removes those rows from dataframe whose dates are not between start_date and end_date
    '''
    df.drop(df[(start_date > df['date']) | (
        df['date'] > end_date)].index, axis=0, inplace=True)


def change_col_pos(df, cols):
    '''
        just to make df consistent in look by bringing ['date', 'status', 'tt'] in front,
        followed by UT's anf then all states
    '''
    for idx, col_name in enumerate(cols):
        col = df.pop(col_name)
        df.insert(idx, col_name, col)


def str_to_int(x):
    '''
        convert string to integer and if there is any error then return 0
    '''
    try:
        x = int(x)
        return x
    except:
        return 0


def string_to_int_cols(df, cols):
    '''
        change all values from str to int and if there is some error then place 0 value there
    '''
    rows = df.shape[0]
    for col_name in cols:
        df[col_name] = df[col_name].apply(str_to_int)


def pre_process_data(json_file_path, start_date, end_date):
    '''
    '''
    cols = ['date', 'status'] + states + uts
    df = json_to_df(json_file_path)
    start_date = string_date_to_standard_date1(start_date)
    end_date = string_date_to_standard_date1(end_date)

    if start_date > end_date:
        print("Enter start_date less than end_date!!")
        exit(1)

    remove_useless_cols(df, cols)
    tranform_df_dates(df, 'date')
    remove_useless_rows(df, start_date, end_date)
    change_col_pos(df, ['date', 'status'] + uts)
    string_to_int_cols(df, states + uts)
    df.sort_values(by=['date'])

    confirmed_df = df.loc[df['status'] == 'Confirmed'].copy()
    recovered_df = df.loc[df['status'] == 'Recovered'].copy()
    deceased_df = df.loc[df['status'] == 'Deceased'].copy()

    cols.remove('status')
    remove_useless_cols(confirmed_df, cols)
    remove_useless_cols(recovered_df, cols)
    remove_useless_cols(deceased_df, cols)

    return confirmed_df, recovered_df, deceased_df


def Q1_1(json_file_path, start_date, end_date):
    """Q1 function
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)
    confirmed_count = confirmed_df[states + uts].sum().sum()
    recovered_count = recovered_df[states + uts].sum().sum()
    deceased_count = deceased_df[states + uts].sum().sum()
    print("\nQ1_1 :-\n ")
    print('confirmed_count: ', confirmed_count, 'recovered_count: ',
          recovered_count, 'deceased_count: ', deceased_count)
    return confirmed_count, recovered_count, deceased_count


def Q1_2(json_file_path, start_date, end_date):
    """Q1 function
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)
    state = 'dl'
    confirmed_count = confirmed_df[state].sum()
    recovered_count = recovered_df[state].sum()
    deceased_count = deceased_df[state].sum()

    print("\nQ1_2 :-\n ")
    print('confirmed_count: ', confirmed_count, 'recovered_count: ',
          recovered_count, 'deceased_count: ', deceased_count)
    return confirmed_count, recovered_count, deceased_count


def Q1_3(json_file_path, start_date, end_date):
    """Q1 function
        Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    states = ['dl', 'mh']
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)
    confirmed_count = confirmed_df[states].sum().sum()
    recovered_count = recovered_df[states].sum().sum()
    deceased_count = deceased_df[states].sum().sum()

    print("\nQ1_3 :-\n ")
    print('confirmed_count: ', confirmed_count, 'recovered_count: ',
          recovered_count, 'deceased_count: ', deceased_count)
    return confirmed_count, recovered_count, deceased_count


def Q1_4(json_file_path, start_date, end_date):
    """Q1 function
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)
    confirmed_cumulative_sum = confirmed_df[states].cumsum().iloc[-1, :]
    highest_confirmed_value = confirmed_cumulative_sum.max()

    recovered_cumulative_sum = recovered_df[states].cumsum().iloc[-1, :]
    highest_recovered_value = recovered_cumulative_sum.max()

    deceased_cumulative_sum = deceased_df[states].cumsum().iloc[-1, :]
    highest_deceased_value = deceased_cumulative_sum.max()

    print("\nQ1_4 :-\n ")
    print('Confirmed :- ')
    print('Highest affected State is: ', list(
        confirmed_cumulative_sum[confirmed_cumulative_sum.values == highest_confirmed_value].index))
    print('Highest affected State count is: ', highest_confirmed_value, '\n')
    print('Recovered :- ')
    print('Highest affected State is: ', list(
        recovered_cumulative_sum[recovered_cumulative_sum.values == highest_recovered_value].index))
    print('Highest affected State count is: ', highest_recovered_value, '\n')
    print('Deceased :- ')
    print('Highest affected State is: ', list(
        deceased_cumulative_sum[deceased_cumulative_sum.values == highest_deceased_value].index))
    print('Highest affected State count is: ', highest_deceased_value, '\n')


def Q1_5(json_file_path, start_date, end_date):
    """Q1 function
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)
    confirmed_cumulative_sum = confirmed_df[states].cumsum().iloc[-1, :]
    lowest_confirmed_value = confirmed_cumulative_sum.min()

    recovered_cumulative_sum = recovered_df[states].cumsum().iloc[-1, :]
    lowest_recovered_value = recovered_cumulative_sum.min()

    deceased_cumulative_sum = deceased_df[states].cumsum().iloc[-1, :]
    lowest_deceased_value = deceased_cumulative_sum.min()

    print("\nQ1_5 :-\n ")
    print('Confirmed :- ')
    print('Lowest affected State is: ', list(
        confirmed_cumulative_sum[confirmed_cumulative_sum.values == lowest_confirmed_value].index))
    print('Lowest affected State count is: ', lowest_confirmed_value, '\n')
    print('Recovered :- ')
    print('Lowest affected State is: ', list(
        recovered_cumulative_sum[recovered_cumulative_sum.values == lowest_recovered_value].index))
    print('Lowest affected State count is: ', lowest_recovered_value, '\n')
    print('Deceased :- ')
    print('Lowest affected State is: ', list(
        deceased_cumulative_sum[deceased_cumulative_sum.values == lowest_deceased_value].index))
    print('Lowest affected State count is: ', lowest_deceased_value, '\n')


def Q1_6(json_file_path, start_date, end_date):
    """Q1 function
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)
    state = 'dl'
    highest_confirmed_count = confirmed_df[state].max()
    highest_recovered_count = recovered_df[state].max()
    highest_deceased_count = deceased_df[state].max()

    print("\nQ1_6 :-\n ")
    print('Confirmed :- ')
    print('Day: ', confirmed_df[confirmed_df[state] ==
                                highest_confirmed_count]['date'].to_string(index=False))
    print('Count: ', highest_confirmed_count, '\n')
    print('Recovered :- ')
    print('Day: ', recovered_df[recovered_df[state] ==
                                highest_recovered_count]['date'].to_string(index=False))
    print('Count: ', highest_recovered_count, '\n')
    print('Deceased :- ')
    print('Day: ', deceased_df[deceased_df[state] ==
                               highest_deceased_count]['date'].to_string(index=False))
    print('Count: ', highest_deceased_count, '\n')


def Q1_7(json_file_path, start_date, end_date):
    """Q1 function : You have to count all the active cases and print the live active cases as on date.
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)
    confirmed_cumulative_sum = confirmed_df[states].cumsum().iloc[-1, :]
    recovered_cumulative_sum = recovered_df[states].cumsum().iloc[-1, :]
    deceased_cumulative_sum = deceased_df[states].cumsum().iloc[-1, :]

    print("\nQ1_7 :-\n ")
    print("State \t\t\tActive_Cases")
    for state in states:
        print(
            state +
            "\t\t\t",
            confirmed_cumulative_sum[state] -
            recovered_cumulative_sum[state] -
            deceased_cumulative_sum[state])
    print()


def getXY(df, start_date, states):
    X = (df['date'] - start_date).to_list()
    X = [i.days for i in X]
    Y = df[states].sum(axis=1).cumsum().tolist()
    return X, Y


def Q2_1(json_file_path, start_date, end_date):
    """Q2 function
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)

    start_date = string_date_to_standard_date1(start_date)
    end_date = string_date_to_standard_date1(end_date)

    confirmed_X, confirmed_Y = getXY(confirmed_df, start_date, states + uts)
    recovered_X, recovered_Y = getXY(recovered_df, start_date, states + uts)
    deceased_X, deceased_Y = getXY(deceased_df, start_date, states + uts)

    name = "Q2_1"
    plt.title(name)
    plt.xlabel("Number of days from - " + str(start_date))
    plt.ylabel("Number of cases")
    plt.fill_between(
        confirmed_X,
        0,
        confirmed_Y,
        alpha=0.5,
        color='red',
        label="Confirmed")
    plt.fill_between(
        recovered_X,
        0,
        recovered_Y,
        alpha=0.5,
        color='blue',
        label="Recovered")
    plt.fill_between(
        deceased_X,
        0,
        deceased_Y,
        alpha=0.8,
        color='green',
        label="Deceased")

    plt.legend(loc=2)
    plt.savefig(name)
    plt.show()
    plt.close(plt.figure())
    plt.clf()


def Q2_2(json_file_path, start_date, end_date):
    """Q2 function
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)
    start_date = string_date_to_standard_date1(start_date)
    end_date = string_date_to_standard_date1(end_date)

    confirmed_X, confirmed_Y = getXY(confirmed_df, start_date, ['dl'])
    recovered_X, recovered_Y = getXY(recovered_df, start_date, ['dl'])
    deceased_X, deceased_Y = getXY(deceased_df, start_date, ['dl'])

    name = "Q2_2"
    plt.title(name)
    plt.xlabel("Number of days from - " + str(start_date))
    plt.ylabel("Number of cases")
    plt.fill_between(
        confirmed_X,
        0,
        confirmed_Y,
        color='red',
        label="Confirmed",
        alpha=0.5)
    plt.fill_between(
        recovered_X,
        0,
        recovered_Y,
        color='blue',
        label="Recovered",
        alpha=0.5)
    plt.fill_between(
        deceased_X,
        0,
        deceased_Y,
        color='green',
        label="Deceased",
        alpha=0.8)

    plt.legend(loc=2)
    plt.savefig(name)
    plt.show()
    plt.close(plt.figure())
    plt.clf()


def Q2_3(json_file_path, start_date, end_date):
    """Q2 function
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)
    start_date = string_date_to_standard_date1(start_date)
    end_date = string_date_to_standard_date1(end_date)

    confirmed_X, confirmed_Y = getXY(confirmed_df, start_date, states + uts)
    recovered_X, recovered_Y = getXY(recovered_df, start_date, states + uts)
    deceased_X, deceased_Y = getXY(deceased_df, start_date, states + uts)
    active_X, active_Y = confirmed_X, []

    for i in range(len(active_X)):
        active_Y.append(confirmed_Y[i] - recovered_Y[i] - deceased_Y[i])

    name = "Q2_3"
    plt.title(name)
    plt.xlabel("Number of days from - " + str(start_date))
    plt.ylabel("Number of cases")
    plt.fill_between(
        active_X,
        0,
        active_Y,
        color='red',
        label="Active",
        alpha=0.5)
    plt.legend(loc=2)
    plt.savefig(name)
    plt.show()
    plt.close(plt.figure())
    plt.clf()


def Q3(json_file_path, start_date, end_date):
    """Q3 function
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    state = 'dl'
    confirmed_df, recovered_df, deceased_df = pre_process_data(
        json_file_path, start_date, end_date)
    start_date = string_date_to_standard_date1(start_date)
    end_date = string_date_to_standard_date1(end_date)

    def getXY(df):
        X = (df['date'] - start_date).to_list()
        X = [i.days for i in X]
        Y = df[state].tolist()
        return X, Y

    confirmed_X, confirmed_Y = getXY(confirmed_df)
    recovered_X, recovered_Y = getXY(recovered_df)
    deceased_X, deceased_Y = getXY(deceased_df)

    def find_intercept_slope(X, Y):
        n = len(X)
        sum_X = sum(X)
        sum_Y = sum(Y)
        sum_sq_X = sum([x * x for x in X])
        sum_sq_Y = sum([y * y for y in Y])
        sum_XY = sum([x * y for x, y in zip(X, Y)])
        intercept = (sum_Y * sum_sq_X - sum_X * sum_XY) / \
            (n * sum_sq_X - sum_X**2)
        slope = (n * sum_XY - sum_X * sum_Y) / (n * sum_sq_X - sum_X**2)
        return intercept, slope

    confirmed_intercept, confirmed_slope = find_intercept_slope(
        confirmed_X, confirmed_Y)
    recovered_intercept, recovered_slope = find_intercept_slope(
        recovered_X, recovered_Y)
    deceased_intercept, deceased_slope = find_intercept_slope(
        deceased_X, deceased_Y)

    def plot(X, Y, slope, intercept, name):
        plt.scatter(X, Y, s=10)
        plt.title(name)
        plt.xlabel("Number of days from start_date")
        plt.ylabel("Number of cases")
        axes = plt.gca()
        x_vals = np.array(axes.get_xlim())
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, color='red')
        plt.savefig(name)
        plt.show()
        plt.close(plt.figure())
        plt.clf()

    plot(confirmed_X, confirmed_Y, confirmed_slope, confirmed_intercept, "confirmed_Q3")
    plot(recovered_X, recovered_Y, recovered_slope, recovered_intercept, "recovered_Q3")
    plot(deceased_X, deceased_Y, deceased_slope, deceased_intercept, "deceased_Q3")

    print('\nQ3 :-\n')
    print(
        confirmed_intercept,
        confirmed_slope,
        recovered_intercept,
        recovered_slope,
        deceased_intercept,
        deceased_slope)
    return confirmed_intercept, confirmed_slope, recovered_intercept, recovered_slope, deceased_intercept, deceased_slope


if __name__ == "__main__":
    # execute only if run as a script
    print('2018101 and 2018261')  # Please put this first

    start_date = "2020-03-14"
    end_date = "2020-09-05"

    Q1_1('states_daily.json', start_date, end_date)
    Q1_2('states_daily.json', start_date, end_date)
    Q1_3('states_daily.json', start_date, end_date)
    Q1_4('states_daily.json', start_date, end_date)
    Q1_5('states_daily.json', start_date, end_date)
    Q1_6('states_daily.json', start_date, end_date)
    Q1_7('states_daily.json', start_date, end_date)
    Q2_1('states_daily.json', start_date, end_date)
    Q2_2('states_daily.json', start_date, end_date)
    Q2_3('states_daily.json', start_date, end_date)
    Q3('states_daily.json', start_date, end_date)
