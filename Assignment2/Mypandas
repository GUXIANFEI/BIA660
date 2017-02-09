infile = open('SalesJan2009.csv')
lines = infile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]

[len(row) == 12 for row in data]
[(index, row) for index, row in enumerate(data) if len(row) != 12]
things = lines[559].split('"')
len(things[0].split(',')[:-1] + [things[1]] + things[-1].split(',')[1:])
data[559] = things[0].split(',')[:-1] + [things[1]] + things[-1].split(',')[1:]
data[559][2]='13000'

import numpy as np
from collections import OrderedDict


class DataFrame(object):

    def __init__(self,Sales_data):
        self.header=sorted((set(Sales_data[0])),key=Sales_data[0].index)
        thing = []
        sales = []
        for list in Sales_data[1:]:
            for lines in list:
                thing += [lines.strip()]
            sales += [thing]
            thing = []
        self.data = sales

    def transform_type(self, col_name):
        is_time = 0
        try:
            nums = [float(row[col_name].replace(',', '')) for row in self.data]
            return nums, 1 if is_time else 0
        except:
            try:
                nums = [parse(row[col_name].replace(',', '')) for row in self.data]
                nums = [time.mktime(num.timetuple()) for num in nums]
                is_time = 1
                return nums, 1 if is_time else 0
            except:
                print 'text values cannot be calculated'

    def min(self,column_name):
        nums,is_time = self.transform_type(column_name)
        Rmin=min(nums)
        return Rmin
    def max(self,column_name):
        nums,is_time=self.transform_type(column_name)
        Rmax=max(nums)
        return Rmax
    def sum(self,column_name):
        nums,is_time=self.transform_type(column_name)
        Rsum=sum(nums)
        return Rsum
    def median(self,column_name):
        nums,is_time=self.transform_type(column_name)
        Rmedian=np.median(nums)
        return Rmedian
    def std(self,column_name):
        nums,is_time=self.transform_type(column_name)
        Rstd=np.std(nums)
        return Rstd
    def mean(self,colnm_name):
        nums,is_time=self.transform_type(colnm_name)
        Rmean =np.mean(nums)
        return Rmean

    def add_rows(self,list_of_lists):
        len_of_rows=len(self.header)
        if sum(len(row)==len_of_rows for row in list_of_lists)==len(list_of_lists):
            self.data+=[OrdereDict(zip(self.header,row)) for row in list_of_lists]
            return self.data
        else:
            print 'incorrect number of columns'

    def add_colunm(self,list_of_values,column_name):
        if len(list_of_values)==len(self.data):
            self.header=self.header+column_name
            self.data=[OrderedDict(zip(list(old_row.keys())+colunm_name,list(old_row.values())+added_values)) for old_row, add_values in zip(self.data,list_of_values)]
            return self.data
        else:
            print 'incorrect number of rows'
