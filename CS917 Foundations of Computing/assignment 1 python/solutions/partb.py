import csv
import time
import calendar
from functools import reduce
"""
    Part B
    Please provide definitions for the following functions *WITH EXCEPTION HANDLERS*
"""
#######
# Custom Exception Class
#######

class MyException(Exception): 
 
 #Exception message set by value
 def __init__(self, value): 
     self.parameter = value 
 
 #Exception message to be printed
 def __str__(self): 
     return self.parameter


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
# Exception condition functions
#######

def check_date_data_exceptions(data, start_date, end_date):
    try:
        get_stamp(start_date) # converts dates to stamps, if invalid date raises a KeyError by default. if the date passed is not a string type, a TypeError instead
        get_stamp(end_date)

        # checks dates are within range of data provided, the start date is before the end date and the data being passed isnt empty
        if (get_stamp(start_date) < int(data[0]['time']) or get_stamp(end_date) > int(data[-1]['time'])): # cant use this line for test above since 'or' doesnt guarantee both get_stamp functions will be called
            raise MyException("date value is out of range")
        elif get_stamp(start_date) > get_stamp(end_date):
            raise MyException("end date must be larger than start date")
        elif len(data) == 0 or data == None:
            raise MyException("dataset not found")

        # lookup whether data is keyed properly, raises KeyError by default is one of the keys is not given
        a = (data[0]['time'], data[0]['high'], data[0]['low'], data[0]['open'], data[0]['close'], data[0]['volumefrom'], data[0]['volumeto'])

    except (ValueError, TypeError):
        raise MyException("invalid date value")
    except KeyError:
        raise MyException("requested column is missing from dataset")
    
#######
#######


def  highest_price(data, start_date, end_date):   
    try:
        check_date_data_exceptions(data, start_date, end_date)
        ranged_data = filter(lambda x: in_range(x['time'],start_date, end_date), data)  # finds data within date range
        r = reduce(lambda a,b:a if float(a['high']) > float(b['high']) else b, ranged_data) # finds data with largest 'high' value 
        return float(r['high'])
    except MyException as e:
        print("Error: " + str(e))
    
    
def  lowest_price(data, start_date, end_date):
    try:
        check_date_data_exceptions(data, start_date, end_date)
        ranged_data = filter(lambda x: in_range(x['time'],start_date, end_date), data)
        r = reduce(lambda a,b:b if float(a['low']) > float(b['low']) else a, ranged_data) # finds data with lowest 'low' value in date range
        return float(r['low'])
    except MyException as e:
        print("Error: " + str(e))

def  max_volume(data, start_date, end_date):
    try:
        check_date_data_exceptions(data, start_date, end_date)
        ranged_data = filter(lambda x: in_range(x['time'],start_date, end_date), data)
        r = reduce(lambda a,b:a if float(a['volumefrom']) > float(b['volumefrom']) else b, ranged_data) # finds data with highest 'volumefrom' value in date range    
        return float(r['volumefrom'])
    except MyException as e:
        print("Error: " + str(e))


def  best_avg_value(data, start_date, end_date):
    try:
        check_date_data_exceptions(data, start_date, end_date)
        ranged_data = filter(lambda x: in_range(x['time'],start_date, end_date), data)
        r = reduce(lambda a,b:a if avg_price(a) > avg_price(b) else b, ranged_data) # finds data with highest average price in date range
        return avg_price(r)
    except MyException as e:
        print("Error: " + str(e))


def  moving_average(data, start_date, end_date):
    try:
        check_date_data_exceptions(data, start_date, end_date)
        ranged_data = filter(lambda x: in_range(x['time'],start_date, end_date), data)
        r = list(map(lambda x:best_avg_value([x], get_date(x['time']), get_date(x['time'])), ranged_data)) # gets list of daily best average values for each data in date range 
        return round(sum(r)/len(r), 2) # mean of r, rounded to 2dp
    except MyException as e:
        print("Error: " + str(e))

     

# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program

    # Example variable initialization
    # data is always the cryptocompare_btc.csv read in using a DictReader
    data = []
    with open("cryptocompare_btc.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    #print(get_stamp("1/02/2016"))
    #print(highest_price(data, "1/02/2016", "31/12/2016"))           
    #print(lowest_price(data, "01/02/2016", "28/02/2016"))
    #print(max_volume(data, "01/01/2015", "01/05/2015"))
    #print(best_avg_value(data, "01/12/2016", "31/12/2016"))
    #print(moving_average(data, "01/12/2014", "31/12/2016"))
    
    pass

