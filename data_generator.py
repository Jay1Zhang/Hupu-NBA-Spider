# -*- coding: utf-8 -*-
# @Time    : 2020/04/18 21:30
# @Author  : jyz
# @FileName: data_generator.py
# @description: 初始化数据生成器

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
    
def gen_dates_by_month(year, month):
    date_sum = 31 if month in [1, 3, 5, 7, 8, 10 ,12] else 30
    if month == 2:
        date_sum = 28
        if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
            date_sum += 1

    i = 0
    start_date = '%s-%s-01' % (year, month)
    dates = []
    while i < date_sum:
        date = arrow.get(start_date).shift(days=i).format("YYYY-MM-DD")
        dates.append(date)
        i += 1

    return dates


if __name__ == "__main__":
    #dates = gen_dates_by_year(2019)
    #print(date[100:])
    dates = gen_dates_by_month(2016, 2)
    print(dates)
