#import matplotlib.pyplot as plt
import csv
import time
import calendar
from functools import reduce

"""
    Part D
    Please provide definitions for the following clas and functions
"""

class Investment:
    def __init__(self,data=None, start_date="", end_date=""):
        self.start_date = end_date
        self.end_date = start_date
        self.data = data
        
    def set(self, data, start_date, end_date): # sets all main variables passed
        self.data, self.start_date, self.end_date = self.check_none(data, start_date, end_date)
        
    def check_none(self, data, start_date, end_date): # used to pass class variables if params not passed to a function
        if data is None:
            data = self.data
        if start_date is None:
            start_date = self.start_date
        if end_date is None:
            end_date = self.end_date
        return (data, start_date, end_date)

    def get_date(self, stamp): # input date ("dd/mm/yy"), returns timestamp
        return time.strftime("%d/%m/%Y", time.gmtime(int(stamp)))

    def get_stamp(self, date):  # input timestamp, returns date("dd/mm/yy")
        return int(calendar.timegm(time.strptime(date, "%d/%m/%Y")))

    def in_range(self, stamp, start_date, end_date): # returns bool if timestamp within date range
        if int(stamp) >= self.get_stamp(start_date) and int(stamp) <= self.get_stamp(end_date):
            return True
        else:
            return False

    def avg_price(self, a): # returns average price i.e ratio shown
        return float(a['volumeto'])/float(a['volumefrom'])

    def highest_price(self, data=None, start_date=None, end_date=None):
        data, start_date, end_date = self.check_none(data, start_date, end_date)
        
        start_stamp = self.get_stamp(start_date)
        end_stamp = self.get_stamp(end_date)

        temp = None
        for row in data:
            if int(row['time']) >= start_stamp and int(row['time']) <= end_stamp:
                if temp == None or float(row['high']) >= temp:
                    temp = float(row['high'])
            elif int(row['time']) > end_stamp:
                break    # sorted by dates, no point checking dates after
        return temp

    def lowest_price(self, data=None, start_date=None, end_date=None):
        data, start_date, end_date = self.check_none(data, start_date, end_date)
        
        start_stamp = self.get_stamp(start_date)
        end_stamp = self.get_stamp(end_date)

        temp = None
        for row in data:
            if int(row['time']) >= start_stamp and int(row['time']) <= end_stamp:
                if temp == None or float(row['low']) <= temp:
                    temp = float(row['low'])
            elif int(row['time']) > end_stamp:
                break    # sorted by dates, no point checking dates after
         #replace None with an appropriate return value
        return temp
    

    def  max_volume(self, data=None, start_date=None, end_date=None):
        data, start_date, end_date = self.check_none(data, start_date, end_date)
        ranged_data = filter(lambda x: self.in_range(x['time'],start_date, end_date), data)
        r = reduce(lambda a,b:a if float(a['volumefrom']) > float(b['volumefrom']) else b, ranged_data) # finds data with highest 'volumefrom' value in date range    
        return float(r['volumefrom'])
     
    def  moving_average(self, data=None, start_date=None, end_date=None):
        data, start_date, end_date = self.check_none(data, start_date, end_date)
        ranged_data = filter(lambda x: self.in_range(x['time'],start_date, end_date), data)
        r = list(map(self.avg_price, ranged_data)) # gets list of daily best average values for each data in date range 
        return sum(r)/len(r) # mean of r, no longer rounded to 2dp
        
    def best_avg_value(self, data=None, start_date=None, end_date=None):
        data, start_date, end_date = self.check_none(data, start_date, end_date)
        
        start_stamp = self.get_stamp(start_date)
        end_stamp = self.get_stamp(end_date)
    
        temp = None
        for row in data:
            if int(row['time']) >= start_stamp and int(row['time']) <= end_stamp:
                ratio = self.avg_price(row)
                if temp == None or ratio >= temp:
                    temp = ratio
            elif int(row['time']) > end_stamp:
                break    # sorted by dates, no point checking dates after
        return temp



def regression(investment,xs, ys, X,Y): # linear regression model
    numerat = 0
    denom = 0
    start_stamp = investment.get_stamp(investment.start_date)
    end_stamp = investment.get_stamp(investment.end_date)
    
    for i in range(0, len(xs)):
        if int(xs[i])>= start_stamp and int(xs[i]) <= end_stamp:
            denom += (xs[i] - X)*(xs[i] - X)
            numerat += (xs[i] - X)*(ys[i] - Y)
    m = numerat / denom # gradient
    b = Y - m*X # y-intercept
    return (m,b)

def predict_next_average(investment):
    start_stamp = float(investment.get_stamp(investment.start_date))
    end_stamp = float(investment.get_stamp(investment.end_date))
    
    X = (start_stamp + end_stamp)/2.0 # average x
    Y = investment.moving_average() # average y
    xs = list(map(lambda d:float(d['time']), investment.data)) # x or time values
    ys = list( map(lambda x:investment.best_avg_value(start_date=investment.get_date(x), end_date=investment.get_date(x)), xs) ) # y or avg values  
    m,b= regression(investment, xs, ys, X, Y) # gradient and intercepts of line
    
    return m * (end_stamp+86400) + b; # next value
   

# classify_trend(investment) -> str
# investment: Investment type
def classify_trend(investment):
        start_stamp = investment.get_stamp(investment.start_date)
        end_stamp = investment.get_stamp(investment.end_date)

        X = (start_stamp + end_stamp)/2.0 # mean x
        xs = list(map(lambda d:int(d['time']), investment.data)) # x values

        ys_low = list( map( lambda x:investment.lowest_price(start_date=investment.get_date(x),end_date=investment.get_date(x) ), xs )) # y values
        ys_high = list( map( lambda x:investment.highest_price(start_date=investment.get_date(x),end_date=investment.get_date(x) ), xs ))

        Y_low = sum(ys_low)/len(ys_low) # mean y values
        Y_high = sum(ys_high)/len(ys_high)

        m_low,b_low = regression(investment, xs, ys_low, X, Y_low) # gradient and intercepts of line
        m_high,b_high = regression(investment, xs, ys_high, X, Y_high)

        if (m_low > 0 and m_high > 0): # gradient of lines tell u if the system is increasing, etc
            return "increasing"
        elif (m_low < 0 and m_high < 0):
            return "decreasing"
        elif (m_low < 0 and m_high > 0):
            return "volative"
        else:
            return "other"

	



# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program
    data = []
    with open("cryptocompare_btc.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]
    inv = Investment()
    inv.set(data, "04/05/2015", "27/05/2015")
    #inv.start_date = "04/05/2015"
    #inv.end_date = "27/05/2015"
    
    #inv.start_date = "01/02/2016"
    #inv.end_date = "28/02/2016"
  
    #inv.start_date = "01/1/2016"
    #inv.end_date = "31/1/2016"
    #print(inv.highest_price())
    print(predict_next_average(inv))
    print(classify_trend(inv))
