import csv
# additional modules
import time
import calendar
from functools import reduce

"""
    Part A
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


def  highest_price(data, start_date, end_date):
    ranged_data = filter(lambda x: in_range(x['time'],start_date, end_date), data)  # finds data within date range
    r = reduce(lambda a,b:a if float(a['high']) > float(b['high']) else b, ranged_data) # finds data with largest 'high' value 
    return float(r['high'])


def  lowest_price(data, start_date, end_date):
    ranged_data = filter(lambda x: in_range(x['time'],start_date, end_date), data)
    r = reduce(lambda a,b:b if float(a['low']) > float(b['low']) else a, ranged_data) # finds data with lowest 'low' value in date range
    return float(r['low'])


def  max_volume(data, start_date, end_date):
    ranged_data = filter(lambda x: in_range(x['time'],start_date, end_date), data)
    r = reduce(lambda a,b:a if float(a['volumefrom']) > float(b['volumefrom']) else b, ranged_data) # finds data with highest 'volumefrom' value in date range    
    return float(r['volumefrom'])
 

def  best_avg_value(data, start_date, end_date):
    ranged_data = filter(lambda x: in_range(x['time'],start_date, end_date), data)
    r = reduce(lambda a,b:a if avg_price(a) > avg_price(b) else b, ranged_data) # finds data with highest average price in date range
    return avg_price(r)


def  moving_average(data, start_date, end_date):
    ranged_data = filter(lambda x: in_range(x['time'],start_date, end_date), data)
    r = list(map(lambda x:best_avg_value([x], get_date(x['time']), get_date(x['time'])), ranged_data)) # gets list of daily best average values for each data in date range 
    return round(sum(r)/len(r), 2) # mean of r, rounded to 2dp



# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program

    # Example variable initialization
    # data is always the cryptocompare_btc.csv read in using a DictReader
    
    data = []
    with open("cryptocompare_btc.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]
    
    # access individual rows from data using list indices
    first_row = data[0]
    # to access row values, use relevant column heading in csv
    #print(f"timestamp = {first_row['time']}")
    #print(f"daily high = {first_row['high']}")
    #print(f"volume in BTC = {first_row['volumefrom']}")
    #print(moving_average(data, "01/01/2016", "31/01/2016"))
    #print(get_stamp("01/01/2016"))
    #print(moving_average(data, "01/02/2016", "28/02/2016"))
    #print(moving_average(data, "01/12/2016", "31/12/2016"))
    pass

