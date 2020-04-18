import arrow

def gen_dates_by_year(year):
    assert isinstance(year, int), "Input \'year\' requires an integer."
    
    date_sum = 366 if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)) else 365
    
    i = 0
    start_date = '%s-1-1' % year
    dates = []
    while i < date_sum:
        date = arrow.get(start_date).shift(days=i).format("YYYY-MM-DD")
        dates.append(date)
        i += 1
        
    return dates

if __name__ == "__main__":
    date = gen_dates_by_year(2019)
    print(date[100:])
