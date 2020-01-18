import numpy as np
import pandas as pd
import datetime as dt

l_month = [1,3,5,7,8,10,12]
s_month = [4,6,9,11]
accepted_years = range(1931,2019)
leap_years = [1932,1936,1940,1944,1948,1952,1956,1960,1964,1968,1972,1976,1980,1984,1988,1992,1996,2000,2004,2008,2012,2016]
bin_volume = 3556
#volume of a cardiff wheelie bin in mililitres (125L)
day = 0
day_check = day + 2
# since the first two rows of the data frame are the date and month, this must not count towards totals.

regions = ["SEEP", "SWEP", "CEP", "NWEP", "NEEP", "SSP", "NSP", "ESP", "NIP"]

def checkinginput() :
    insert = input("Please pick a region where would you'd like to check?")
    insert = insert.upper()
    if insert in regions :        
        global data
        data = "Had_daily_qc.txt"
        data = data[:3] + insert + data[3:]
        return (data)
    else :
        print("sorry I didn't recognise that, please try your answer again")
        insert = input("Please pick a region where would you'd like to check?")
        checkinginput()
        
def checkdate():
    date = input("please enter a date you'd like to check in the format DD/MM/YYYY")
    date = date.split("/")
    # I could use a regex here to include multiple split types, but I want to import as few packages as possible!
    
    # add an error for using the wrong delimiter? 
    
    day = int(date[0])
    month = int(date[1])
    year = int(date[2])
    
    # Splitting the date into variables that are then checked, the initial variable is year and the range is 1932-2019
    
    if year in accepted_years : 
        if  month == 0 or month > 12 :
            print("sorry, that month doesn't exist")
            checkdate()
    # Since the number of days in a month can be either 28 (Feb) 29 (Leap year feb), 30 (Shorter months), or 31 (longer months)
    # this next section is quite long, but it should hopefully detect and maintain a valid date by the user.
            
        else:
            if month in l_month :
                if 1 > day or 31 < day :
                    print("Only 31 days in a long month!")
                    checkdate()
                else : 
                    return day, month, year
            elif month in s_month :
                if 1 > day or 30 < day : 
                    print("Only 31 days in a short month!")                    
                    checkdate()
                else :
                    return day, month, year
            elif month == 2 and year not in leap_years :
                if 1 > day or 28 < day : 
                    print("Only 28 days in February")                    
                    checkdate()
                else :
                    return day, month, year
            elif month == 2 and year in leap_years : 
                if 1 > day or 29 < day :
                    print("Only 29 days in a leap Feburary")
                    checkdate()
                else :
                    return day, month, year
            
    else: 
        print("sorry, that doesn't appear to be a year within the range?")
        checkdate()
    
        
def creatingdata(data, day, month, year) :
    df = pd.read_csv(data, header = None , names = ["year","month", 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31], skiprows = 3, sep ='\s+', na_values = -99.99)
    df_2 = df
    df = df[df.year == year]
    df = df[df.month >= month]
    #trimming the dataset to start the in the month given and slicing out the single year
    df_2 = df_2[df_2.year >= year + 1]
    #slicing every year above the year stated 
    df = df.append(df_2, ignore_index=True)
    return df
    # reconstructing the dataframe thus giving us every year beyond our starting point)
    
def binfill(df):
    month_check = 0
    month_check_end = 1
    day_check = day + 1
    day_check_end = day_check + 1   
    if month in l_month :
        intial_day_count = 31 - (day - 1)
        day_count = 1
        rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
        running_total = rain_value
        for i in range(1,intial_day_count) :
            day_count += 1
            day_check += 1
            day_check_end += 1
            rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
            running_total += rain_value
    elif month in s_month : 
        intial_day_count = 30 - (day - 1)
        day_count = 1
        rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
        running_total = rain_value
        for i in range(1,intial_day_count) :
            day_count += 1
            day_check += 1
            day_check_end += 1
            rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
            running_total += rain_value
    elif month == 2 and year in leap_years :
        intial_day_count = 29 - (day - 1)
        day_count = 1
        rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
        running_total = rain_value
        for i in range(1,intial_day_count) :
            day_count += 1
            day_check += 1
            day_check_end += 1
            rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
            running_total += rain_value
    elif month == 2 and year not in leap_years :
        intial_day_count = 28 - (day - 1)
        day_count = 1
        rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
        running_total = rain_value
        for i in range(1,intial_day_count) :
            day_count += 1
            day_check += 1
            day_check_end += 1
            rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
            running_total += rain_value            
    while running_total <= bin_volume :
        month_check += 1
        month_check_end += 1
        day_check = 2
        day_check_end = 3
        month_checker = df.iloc[month_check:month_check_end,1:2].iat[0,0]
        leap_year_checker = df.iloc[month_check:month_check_end,0:1].iat[0,0]        
        if month_checker in l_month :
            for i in range(1,31) :
                day_count += 1
                day_check += 1
                day_check_end += 1
                rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
                running_total += rain_value
        elif month_checker in s_month : 
            for i in range(1,30) :
                    day_count += 1
                    day_check += 1
                    day_check_end += 1
                    rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
                    running_total += rain_value
        elif month_checker == 2 and leap_year_checker in leap_years :
            for i in range(1,29) :
                    day_count += 1
                    day_check += 1
                    day_check_end += 1
                    rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
                    running_total += rain_value
        elif month_checker == 2 and leap_year_checker not in leap_years :
            for i in range(1,28) :
                    day_count += 1
                    day_check += 1
                    day_check_end += 1
                    rain_value = df.iloc[month_check:month_check_end,day_check:day_check_end].iat[0,0]
                    running_total += rain_value
    end_date = start_date + dt.timedelta(day_count)
    return end_date, day_count


print("Walking around in Cardiff one day I saw a wheelie bin full of rain and asked myself \"how long must that have taken?\" Using MET data, now you can find out!")
print("South East - 'seep', South West & North Wales - 'swep', Central - 'cep', North West & South Wales - 'nwep', ")
print("North East - 'neep', South Scotland - 'ssp', North Scotland - 'nsp', East Scotland - 'esp', or Northern Ireland - 'nip'")

insert = checkinginput()

day, month, year = checkdate()

start_date = dt.date(year,month,day)

df = creatingdata(data, day, month, year)

end_date, day_count = binfill(df)

start_date = str(start_date)
end_date = str(end_date)

print("Starting from " , start_date , " it'd take " , day_count , " days until " , end_date , "to fill a 125 Litre bin")
