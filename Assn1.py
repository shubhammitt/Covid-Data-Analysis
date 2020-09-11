import pandas as pd
import numpy as np
import json
import re
import datetime
import sys

# API usage : https://api.covid19india.org/documentation/statedaily.html

def string_date_to_standard_date1(date):
    """ 
    Args:
        date : in string format, Ex - "2020-03-14"

    return date in datetime.date format so that relational operator works on it
    """
    year, mon, date = map(int, date.split('-'))
    return datetime.datetime(year, mon, date)


def string_date_to_standard_date2(date):
    """ 
    Args:
        date : in string format, Ex - "15-Mar-20"

    return date in datetime.date format so that relational operator works on it
    """
    date, mon, year = date.split('-')
    mon_name_to_num = {'Jan' : 1, 
                       'Feb' : 2, 
                       'Mar' : 3, 
                       'Apr' : 4, 
                       'May' : 5, 
                       'Jun' : 6, 
                       'Jul' : 7, 
                       'Aug' : 8, 
                       'Sep' : 9, 
                       'Oct' : 10, 
                       'Nov' : 11, 
                       'Dec' : 12 }
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


def count_from_start_to_end(data, start_date, end_date, states):
    """
    Args:
        data (TYPE): extracted from json file
        start_date (TYPE): Description
        end_date (TYPE): Description
        states : a list of states abbrevations whose count need to be taken in account

    return sum of confirmed_count, recovered_count, deceased_count in the list 'states'
    """
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
    confirmed_count, recovered_count, deceased_count = count_from_start_to_end(extract_json_file(json_file_path), start_date, end_date, ['tt'])
    print('confirmed_count: ',confirmed_count, 'recovered_count: ',recovered_count, 'deceased_count: ',deceased_count)
    return confirmed_count, recovered_count, deceased_count


def Q1_2(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_count, recovered_count, deceased_count = count_from_start_to_end(extract_json_file(json_file_path), start_date, end_date, ['dl'])
    print('confirmed_count: ',confirmed_count, 'recovered_count: ',recovered_count, 'deceased_count: ',deceased_count)
    return confirmed_count, recovered_count, deceased_count


def Q1_3(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    confirmed_count, recovered_count, deceased_count = count_from_start_to_end(extract_json_file(json_file_path), start_date, end_date, ['dl', 'mh'])
    print('confirmed_count: ',confirmed_count, 'recovered_count: ',recovered_count, 'deceased_count: ',deceased_count)
    return confirmed_count, recovered_count, deceased_count

def Q1_4(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    highest_confirmed_count = [0, '']
    highest_recovered_count = [0, '']
    highest_deceased_count  = [0, '']
    data = extract_json_file(json_file_path)

    for state in  data[0]:
        if len(state) == 2 and state != 'tt':
            confirmed_count, recovered_count, deceased_count = count_from_start_to_end(data, start_date, end_date, [state])
            if confirmed_count > highest_confirmed_count[0]:
                highest_confirmed_count[0] = confirmed_count
                highest_confirmed_count[1] = state

            if recovered_count > highest_recovered_count[0]:
                highest_recovered_count[0] = recovered_count
                highest_recovered_count[1] = state

            if deceased_count > highest_deceased_count[0]:
                highest_deceased_count[0] = deceased_count
                highest_deceased_count[1] = state

    print('Confirmed :- ')
    print('Highest affected State is: ', highest_confirmed_count[1])
    print('Highest affected State count is: ', highest_confirmed_count[0], '\n')
    print('Recovered :- ')
    print('Highest affected State is: ', highest_recovered_count[1])
    print('Highest affected State count is: ', highest_recovered_count[0], '\n')
    print('Deceased :- ')
    print('Highest affected State is: ', highest_deceased_count[1])
    print('Highest affected State count is: ', highest_deceased_count[0], '\n')


def Q1_5(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    lowest_confirmed_count = [sys.maxsize, '']
    lowest_recovered_count = [sys.maxsize, '']
    lowest_deceased_count  = [sys.maxsize, '']
    data = extract_json_file(json_file_path)

    for state in  data[0]:
        if len(state) == 2 and state != 'tt':
            confirmed_count, recovered_count, deceased_count = count_from_start_to_end(data, start_date, end_date, [state])
            if confirmed_count < lowest_confirmed_count[0]:
                lowest_confirmed_count[0] = confirmed_count
                lowest_confirmed_count[1] = state

            if recovered_count < lowest_recovered_count[0]:
                lowest_recovered_count[0] = recovered_count
                lowest_recovered_count[1] = state

            if deceased_count < lowest_deceased_count[0]:
                lowest_deceased_count[0] = deceased_count
                lowest_deceased_count[1] = state

    print('Confirmed :- ')
    print('Lowest affected State is: ', lowest_confirmed_count[1])
    print('Lowest affected State count is: ', lowest_confirmed_count[0], '\n')
    print('Recovered :- ')
    print('Lowest affected State is: ', lowest_recovered_count[1])
    print('Lowest affected State count is: ', lowest_recovered_count[0], '\n')
    print('Deceased :- ')
    print('Lowest affected State is: ', lowest_deceased_count[1])
    print('Lowest affected State count is: ', lowest_deceased_count[0], '\n')


def Q1_6(json_file_path, start_date, end_date):
    """Q1 function
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    data = extract_json_file(json_file_path)
    start_date, end_date = string_date_to_standard_date1(start_date), string_date_to_standard_date1(end_date)
    highest_confirmed_count = [0, '']
    highest_recovered_count = [0, '']
    highest_deceased_count  = [0, '']

    for day in data:
        today_date = string_date_to_standard_date2(day['date'])
        if start_date <= today_date and today_date <= end_date:
            count = int(day['dl'])
            if day['status'] == 'Confirmed' and count > highest_confirmed_count[0]:
                highest_confirmed_count[0] = count
                highest_confirmed_count[1] = day['date']

            if day['status'] == 'Recovered' and count > highest_recovered_count[0]:
                highest_recovered_count[0] = count
                highest_recovered_count[1] = day['date']

            if day['status'] == 'Deceased' and count > highest_deceased_count[0]:
                highest_deceased_count[0] = count
                highest_deceased_count[1] = day['date']

    print('Confirmed :- ')
    print('Day: ', highest_confirmed_count[1])
    print('Count: ',highest_confirmed_count[0],'\n')
    print('Recovered :- ')
    print('Day: ', highest_recovered_count[1])
    print('Count: ', highest_recovered_count[0], '\n')
    print('Deceased :- ')
    print('Day: ', highest_deceased_count[1])
    print('Count: ', highest_deceased_count[0], '\n')


def Q1_7(json_file_path, start_date, end_date):
    """Q1 function : You have to count all the active cases and print the live active cases as on date.
    
    Args:
        json_file_path (TYPE): Description
        start_date (TYPE): Description
        end_date (TYPE): Description
    """
    data = extract_json_file(json_file_path)
    print("State\t\tActive Cases")
    for state in  data[0]:
        if len(state) == 2 and state != 'tt':
            confirmed_count, recovered_count, deceased_count = count_from_start_to_end(data, start_date, end_date, [state])
            print(state,"\t\t",confirmed_count - recovered_count - deceased_count)
            
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
    Q1_4('states_daily.json', start_date, end_date)
    Q1_5('states_daily.json', start_date, end_date)
    Q1_6('states_daily.json', start_date, end_date)
    Q1_7('states_daily.json', start_date, end_date)
    # Q2_1('states_daily.json', start_date, end_date)
    # Q2_2('states_daily.json', start_date, end_date)
    # Q2_3('states_daily.json', start_date, end_date)
    # Q3('states_daily.json', start_date, end_date)