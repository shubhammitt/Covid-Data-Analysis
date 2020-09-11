import pandas as pd
import numpy as np
import json
import re
import datetime

# API usage : https://api.covid19india.org/documentation/statedaily.html

def string_date_to_standard_date1(date):
    """ 
    Args:
        date : in string format, Ex - "2020-03-14"

    return date in datetime.date format so that relational operator works on it
    """
    year, mon, date = map(int,date.split('-'))
    return datetime.datetime(year, mon, date)


def string_date_to_standard_date2(date):
    """ 
    Args:
        date : in string format, Ex - "15-Mar-20"

    return date in datetime.date format so that relational operator works on it
    """
    date, mon, year = date.split('-')
    mon_name_to_num = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6, 'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12}
    mon = mon_name_to_num[mon]
    return datetime.datetime(2000 + int(year), mon, int(date))


def extract_json_file(json_file_path):
    """ 
    Args:
        json_file_path : json file's name

    returns a list of dictionaries and each dictionary contains the required stats
    """
    with open(json_file_path) as json_file:
        return json.load(json_file)['states_daily']


def count_from_start_to_end(json_file_path, start_date, end_date, states):
    """
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
        states : a list of states abbrevations whose count need to be taken in account

    return sum of confirmed_count, recovered_count, deceased_count in the list states
    """
    
    data = extract_json_file(json_file_path)
    start_date, end_date = string_date_to_standard_date1(start_date), string_date_to_standard_date1(end_date)
    confirmed_count = recovered_count = deceased_count = 0

    for day in data:
        today_date = string_date_to_standard_date2(day['date'])
        if start_date <= today_date and today_date <= end_date:
            count = 0
            for state in states:
                count += int(day[state])

            if day['status'] == 'Confirmed':
                confirmed_count += count
            elif day['status'] == 'Recovered':
                recovered_count += count
            else:
                deceased_count += count

    return confirmed_count, recovered_count, deceased_count


def Q1_1(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_count, recovered_count, deceased_count = count_from_start_to_end(json_file_path, start_date, end_date, ['tt'])
    print('confirmed_count: ',confirmed_count, 'recovered_count: ',recovered_count, 'deceased_count: ',deceased_count)
    return confirmed_count, recovered_count, deceased_count


def Q1_2(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_count, recovered_count, deceased_count = count_from_start_to_end(json_file_path, start_date, end_date, ['dl'])
    print('confirmed_count: ',confirmed_count, 'recovered_count: ',recovered_count, 'deceased_count: ',deceased_count)
    return confirmed_count, recovered_count, deceased_count


def Q1_3(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_count, recovered_count, deceased_count = count_from_start_to_end(json_file_path, start_date, end_date, ['dl', 'mh'])
    print('confirmed_count: ',confirmed_count, 'recovered_count: ',recovered_count, 'deceased_count: ',deceased_count)
    return confirmed_count, recovered_count, deceased_count


def Q1_4(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    
    print('Confirmed \n')
    print('Highest affected State is: ')
    print('Highest affected State count is: ')
    print('Recovered \n')
    print('Highest affected State is: ')
    print('Highest affected State count is: ')
    print('Deceased \n')
    print('Highest affected State is: ')
    print('Highest affected State count is: ')


def Q1_5(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    print('Confirmed \n')
    print('Lowest affected State is: ')
    print('Lowest affected State count is: ')
    print('Recovered \n')
    print('Lowest affected State is: ')
    print('Lowest affected State count is: ')
    print('Deceased \n')
    print('Lowest affected State is: ')
    print('Lowest affected State count is: ')


def Q1_6(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    print('Confirmed \n')
    print('Day: ',Highest_spike_day)
    print('Count: ',Highest_spike_count)
    print('Recovered \n')
    print('Day: ',Highest_spike_day)
    print('Count: ',Highest_spike_count)
    print('Deceased \n')
    print('Day: ',Highest_spike_day)
    print('Count: ',Highest_spike_count)


def Q1_7(json_file_path, start_date, end_date):
    """Q1 function : You have to count all the active cases and print the live active cases as on date.
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    print() # print any way you want


def Q2_1(json_file_path, start_date, end_date):
    """Q2 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    #plt.show()
    #plt.save()

def Q2_2(json_file_path, start_date, end_date):
    """Q2 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    #plt.show()
    #plt.save()


def Q2_3(json_file_path, start_date, end_date):
    """Q2 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    #plt.show()
    #plt.save()

def Q3(json_file_path, start_date, end_date):
    """Q3 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    return confirmed_intercept, confirmed_slope, recovered_intercept, recovered_slope, deceased_intercept, deceased_slope


if __name__ == "__main__":
    # execute only if run as a script
    print('2018101 and 2018261') # Please put this first

    start_date = "2020-03-14"
    end_date = "2020-09-05"
    
    Q1_1('states_daily.json', start_date, end_date)
    Q1_2('states_daily.json', start_date, end_date)
    Q1_3('states_daily.json', start_date, end_date)
    # Q1_4('states_daily.json', start_date, end_date)
    # Q1_5('states_daily.json', start_date, end_date)
    # Q1_6('states_daily.json', start_date, end_date)
    # Q1_4('states_daily.json', start_date, end_date)
    # Q2_1('states_daily.json', start_date, end_date)
    # Q2_2('states_daily.json', start_date, end_date)
    # Q2_3('states_daily.json', start_date, end_date)
    # Q3('states_daily.json', start_date, end_date)