import random

import pandas as pd
#task 1
class KNN:
    def __init__(self, X, y, k):
        self.trainset = X
        self.trainlabel = list(y)
        self.kneighbor = k

        y_set = set(list(y))
        #depend use classification or regression due to label
        if len(y_set) <= 3:
            self.mode_flag = 'classification'
        else:
            self.mode_flag = 'regression'
        pass

    def distance(self,data_point_1,data_point_2):
        """
        Obtain the Euclidean distance between two data points
        :param data_point_1: data_point_1
        :param data_point_2: data_point_2
        :return: Euclidean distance
        """
        data_point_1 = data_point_1.values
        data_point_2 = data_point_2.values

        return sum((data_point_1-data_point_2)**2)**0.5

    def predict(self,data_point):
        """
        For the classification problem: the category of the output for the instance, when sorting, for the new instance,
        according to its k neighbors of the training instance of the category, through the majority of voting methods
        to predict
        For the regression problem: the output is the value of the instance, the regression, for the new instance, take
        its k nearest neighbor training instance of the average value of the forecast

        :param data_point:
        :return:
        """

        #Get the current node to the other nodes of the distance list
        distance_list = []
        for i in range(len(self.trainset)):
            temp_distance = self.distance(self.trainset.iloc[i,:],data_point)
            distance_list.append((self.trainlabel[i],temp_distance))

        #Sort by distance from small to large
        distance_list = sorted(distance_list, key=lambda x:x[1])

        #Take the nearest k nodes
        k_neighbors = distance_list[:self.kneighbor]
        
        key_list = []
        for i in k_neighbors:
            key_list.append(i[0])

        if self.mode_flag == 'regression':
            avg_datapoint = sum(key_list)/float(self.kneighbor)
            ave_absolute_distance = sum(abs(key_list-avg_datapoint))/self.kneighbor
            return avg_datapoint,ave_absolute_distance

        elif self.mode_flag == 'classification':
            labels = {}
            for label in set(key_list):
                labels[label] = key_list.count(label)

            pre_label = labels.keys()[0]
            posterior_probability = float(labels.values()[0])/float(len(key_list))

            return pre_label,posterior_probability

#classification test
data_input = pd.read_csv(r'classification_data.csv')
train_set = data_input.iloc[:,:-1]
train_label = data_input.iloc[:,-1]

my_knn = KNN(train_set,train_label,5)
print my_knn.predict(train_set.iloc[10])

#regression test
data_input = pd.read_csv(r'regression_data.csv',index_col=0)
train_set = data_input.iloc[:,:-1]
train_label = data_input.iloc[:,-1]

my_knn = KNN(train_set,train_label,5)
print my_knn.predict(train_set.iloc[10])
