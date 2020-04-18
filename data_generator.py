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
    

if __name__ == "__main__":
    date = gen_dates_by_year(2019)
    #print(date[100:])
