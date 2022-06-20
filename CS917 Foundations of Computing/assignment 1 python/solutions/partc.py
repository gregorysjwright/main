import csv
import time
import calendar
from collections import OrderedDict
"""
    Part C
    Please provide definitions for the following functions
"""

#######
# Helper functions
#######
def get_stamp(date): # input date ("dd/mm/yy"), returns timestamp
    return int(calendar.timegm(time.strptime(date, "%d/%m/%Y")))

def get_date(stamp): # input timestamp, returns date("dd/mm/yy")
        return time.strftime("%d/%m/%Y", time.gmtime(int(stamp)))

def in_range(stamp, start_date, end_date): # returns bool if timestamp within date range
    if int(stamp) >= get_stamp(start_date) and int(stamp) <= get_stamp(end_date):
        return True
    else:
        return False

def avg_price(a): # returns average price i.e ratio shown
    return float(a['volumeto'])/float(a['volumefrom'])
    
#######
#######

    
def  moving_avg_short(data, start_date, end_date):

    short_dictionary = dict()

    for j in range(0, len(data)):
        if in_range(data[j]['time'], start_date, end_date):
            rows = []
            if j > 2: # creates list of rows to find moving average over (3 days)
                rows = data[j-2:j+1]
            else: # if at beginning of data, start index from beginning instead
                rows = data[0:j+1]
            ratios = list(map(avg_price, rows))
            short_dictionary[get_date(data[j]['time'])] = sum(ratios)/len(ratios)
            
    return short_dictionary


def  moving_avg_long(data, start_date, end_date):
	 
    long_dictionary = dict()

    for j in range(0, len(data)):
        if in_range(data[j]['time'], start_date, end_date):
            
            if j > 8: # creates list of rows to find moving average over (10 days)
                rows = data[j-9:j+1]
            else:
                rows = data[0:j+1]
            ratios = list(map(avg_price, rows))
            long_dictionary[get_date(data[j]['time'])] = sum(ratios)/len(ratios)
    
    return long_dictionary


def  find_buy_list(short_avg_dict, long_avg_dict):
    buy_dictionary = dict()
    short = sorted(short_avg_dict.items(), key=lambda t: get_stamp(t[0])) # sorted list of items by date from dictionaries
    long = sorted(long_avg_dict.items(), key=lambda t: get_stamp(t[0]))
      
    for i in range(1, len(short)):
        if (short[i-1] <= long[i-1]) and (short[i] > long[i]):
            buy_dictionary[short[i][0]] = 1
        else:
            buy_dictionary[short[i][0]] = 0
            
    return buy_dictionary


def  find_sell_list(short_avg_dict, long_avg_dict):
    sell_dictionary = dict()
    short = sorted(short_avg_dict.items(), key=lambda t: get_stamp(t[0])) # sorted list of items by date from dictionaries
    long = sorted(long_avg_dict.items(), key=lambda t: get_stamp(t[0]))
                       
    for i in range(1, len(short)):
        if (short[i-1] >= long[i-1]) and (short[i] < long[i]):
            sell_dictionary[short[i][0]] = 1
        else:
            sell_dictionary[short[i][0]] = 0

    return sell_dictionary


def  crossover_method(data, start_date, end_date):
    long = moving_avg_long(data, start_date, end_date)
    short = moving_avg_short(data, start_date, end_date)
    buy = find_buy_list(short,long)
    sell = find_sell_list(short,long)
    buy_list = list(map(lambda b:b[0], list(filter(lambda b:b[1], buy.items()))))
    sell_list = list(map(lambda s:s[0], list(filter(lambda s:s[1], sell.items()))))
    return [buy_list, sell_list]


# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program

    # Example variable initialization
    # data is always the cryptocompare_btc.csv read in using a DictReader
    
    data = []
    with open("cryptocompare_btc.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]
        #print(get_date(1430179200))
        #print(get_stamp("01/06/2017"))
        #print(crossover_method(data, "28/04/2015", "12/05/2015"))
        #print(crossover_method(data, "05/09/2018", "27/09/2018"))
        #print(crossover_method(data, "03/11/2019", "14/11/2019"))
    pass

