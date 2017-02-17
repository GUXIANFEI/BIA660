from collections import OrderedDict
import csv
import datetime
import ast
import numpy


class DataFrame(object):
    @classmethod
    def from_csv(cls, file_path,delimiter_char=',',quote_char='"'):
        with open(file_path,'rU') as infile:
            reader=csv.reader(infile,delimiter=delimiter_char,quotechar=quote_char )
            data=[]
            for row in reader:
                data.append(row)
        return cls(data)

    def __init__(self,list_of_lists,header=True):
        if header:
            self.data=list_of_lists[1:]
            [[column.strip() for column in lines] for lines in self.data]
            self.header=list_of_lists[0]
            if len(self.header)!=len(set(self.header)):
                raise Exception('header are not unique')
        else:
            self.header=['column'+str(index+1) for index,column in enumerate(list_of_lists[0])]
            self.data=list_of_lists
            [[column.strip() for column in lines] for lines in self.data]

        self.data=[OrderedDict(zip(self.header,row)) for row in self.data]

    def __getitem__(self, item):
        # this is for rows only
        if isinstance(item, (int, slice)):
            return self.data[item]

        # this is for columns only
        elif isinstance(item, (str, unicode)):
            return Series([row[item] for row in self.data])

        # this is for rows and columns
        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rowz]
                    elif all([isinstance(thing, (str, unicode)) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], (str, unicode)):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')


        elif isinstance(item, list):
            if isinstance(item[0],(str,unicode)):
                return [[row[column_name] for column_name in item] for row in self.data]
            elif isinstance(item[0],bool):
                return [self.data[index] for index,value in enumerate(item) if value==True]


    def get_rows_column_name(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]

    def add_rows(self,list_of_lists):
        if len(self.header)==len(list_of_lists):
            new_data=[OrderedDict(zip(self.header,list_of_lists))]
            self.data=self.data.append(new_data)
            return self.data
        else:
            raise Exception('different column number')

    def add_column(self,list_of_lists,column_name):
        if len(list_of_lists)==len[self.data]:
            self.data[column_name]=list_of_lists
            return self.data
        else:
            raise Exception('different rows number')

    def sort_by(self,column_name,reverse=1):
        if reverse:
            sorted_data=sorted(self.data,key=lambda x:x[column_name],reverse=True)
            return sorted_data
        else:
            sorted_data=sorted(self.data,key=lambda x:x[column_name])
            return sorted_data

    def group_by(self,column1,column2,fun):
        new_list=[]
        new_list2=[]
        for column_index1 ,value in enumerate(self.data):
            if value==column1:
                column_index1=column_index1
        for row in self.data:
            new_list=new_list[row[column_index1]]
        for column_index2,value in enumerate(new_list):
            if value==column2:
                column_index2 = column_index2
        for rowz in new_list:
            new_list2=new_list2[rowz[column_index2]]

        return fun(new_list2)


def avg(list_of_values):
    return sum(list_of_values) / float(len(list_of_values))



class Series(list):
    def __eq__(self, other):
        ret_list = []
        for item in self:
            ret_list.append(item == other)
        return ret_list

    def __lt__(self,other):
        ret_list=[]
        for item in self:
            ret_list.append(item < other)
        return ret_list

    def __gt__(self,other):
        ret_list=[]
        for item in self:
            ret_list.append(item > other)
        return ret_list

    def __leq__(self,other):
        ret_list=[]
        for item in self:
            ret_list.append(item <= other)
        return ret_list

    def __geq__(self,other):
        ret_list=[]
        for item in self:
            ret_list.append(item >= other)
        return ret_list
