import bs4

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import unicodedata
import time 

import pandas as pd
import datetime
%matplotlib inline
from dateutil.parser import parse

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np

import matplotlib.pyplot as plt
from pandas import Series
from scipy.spatial import distance

#task1
def scrape_data(start_date, from_place, to_place, city_name):
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/flights/explore/')
    from_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
    from_input.click()
    actions = ActionChains(driver)
    actions.send_keys(from_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    to_input=driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(to_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(3)
    names=driver.find_elements_by_class_name('LJTSM3-v-c')
    result_city_name=[]
    for name in names:
         result_city_name.append(name.text)    
    normal_name=[]
    for data in result_city_name:
        normal = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
        normal_name.append(normal)  
    for index, value in enumerate(normal_name):
        if city_name.title() in value:
            number=index
            print number
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    test = results[number]
    bars = test.find_elements_by_class_name('LJTSM3-w-x')

    data = []
    for bar in bars:
        ActionChains(driver).move_to_element(bar).perform()
        time.sleep(0.002)
        data.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
               test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))

    clean_data = [(float(d[0].replace('$', '').replace(',', '')), (parse(d[1].split('-')[0].strip()) - datetime.datetime(2017,4,2,0,0)).days, d[1].split('-')[0].strip()) for d in data]

    filter_date = []
    for x in clean_data:
        if x[1]>= start_date:
            filter_date.append(x)

    df = pd.DataFrame(filter_date, columns=['Price', 'st', 'Date_of_Flight'])
    df=df[[0,2]]
    return df
    
    
    
    
    
#task 2   
def scrape_data_90(start_date, from_place, to_place, city_name):
driver = webdriver.Chrome()
driver.get('https://www.google.com/flights/explore/')
from_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
from_input.click()
actions = ActionChains(driver)
actions.send_keys(from_place)
actions.send_keys(Keys.ENTER)
actions.perform()
to_input=driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
to_input.click()
actions = ActionChains(driver)
actions.send_keys(to_place)
actions.send_keys(Keys.ENTER)
actions.perform()
time.sleep(3)
names=driver.find_elements_by_class_name('LJTSM3-v-c')
result_city_name=[]
for name in names:
     result_city_name.append(name.text)    
normal_name=[]
for data in result_city_name:
    normal = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
    normal_name.append(normal)  
for index, value in enumerate(normal_name):
    if city_name.title() in value:
        number=index
        print number
results = driver.find_elements_by_class_name('LJTSM3-v-d')
test = results[number]
bars = test.find_elements_by_class_name('LJTSM3-w-x')

data = []
for bar in bars:
    ActionChains(driver).move_to_element(bar).perform()
    time.sleep(0.003)
    data.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
           test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))

next_page=driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[4]/div/div[2]/div[3]/div/div[2]/div[2]/div/div[2]/div[5]/div')
next_page.click()

time.sleep(3)

next_page=driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[4]/div/div[2]/div[3]/div/div[2]/div[2]/div/div[2]/div[5]/div')
next_page.click()

time.sleep(3)

results = driver.find_elements_by_class_name('LJTSM3-v-d')
test = results[number]
bars = test.find_elements_by_class_name('LJTSM3-w-x')


for bar in bars:
    ActionChains(driver).move_to_element(bar).perform()
    time.sleep(0.003)
    data.append((test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
           test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
clean_data = [(float(d[0].replace('$', '').replace(',', '')), (parse(d[1].split('-')[0].strip()) - datetime.datetime(2017,4,7,0,0)).days, d[1].split('-')[0].strip()) for d in data]

filter_date = []
for x in clean_data:
    if x[1]>= start_date:
        filter_date.append(x)

df = pd.DataFrame(filter_date, columns=['Price', 'st', 'Date_of_Flight'])
df=df[[0,2]]
df=df.iloc[:90,:]
return df


#task3
def task_3_dbscan(data):
    df=data
    for i in range(len(df)):
        df.set_value(i,'Date',i+1)

    X = StandardScaler().fit_transform(df[['Date_of_Flight', 'Price']])
    db = DBSCAN(eps=.3, min_samples=2).fit(X)

    labels = db.labels_
    clusters = len(set(labels))
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    plt.subplots(figsize=(12,8))

    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                markeredgecolor='k', markersize=14)

    plt.title("Total Clusters: {}".format(clusters), fontsize=14, y=1.01)

    plt.savefig('task_3_dbscan.png')

    df['dbscan_labels'] = db.labels_

    x_axis=[]
    y_axis=[]
    for a in X.T[0]:
        x_axis.append(a)
    for b in X.T[1]:
        y_axis.append(b)
    df['x_axis']=x_axis
    df['y_axis']=y_axis

    noise_point=df[df['dbscan_labels']==-1]
    noise_p=noise_point[['x_axis','y_axis']].values.T.tolist()
    
    rf = df.groupby('dbscan_labels')['y_axis','x_axis'].agg('mean') 

    dist=[]
    for x in zip(rf.values.T.tolist()[0][1:], rf.values.T.tolist()[1][1:]):
        for y in zip(noise_p[0],noise_p[1]):
            dist.append(distance.euclidean(x,y))

    lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

    belong_cluster=[]
    for m in lol(dist,clusters-1):
        for index, value in enumerate(m):
            if value == min(m):
                belong_cluster.append(index-1)
    for index, number in enumerate(belong_cluster):
        if noise_point.iloc[index]['Price'] <= np.mean(df[df['dbscan_labels']==number]['Price'])-2*np.std(df[df['dbscan_labels']==number]['Price']):
            return noise_point.iloc[index][[0,1]]
        
    
def task_3_IQR(data):
    df=data
    df['Price'].plot.box()
    plt.savefig('task_3_IQR.png')

    Q1=df['Price'].quantile(.25)
    Q3=df['Price'].quantile(.75)
    IQR=Q3-Q1
    scope=Q1-1.5*IQR
    if len(df[df['Price']<=scope])>0:
        return df[df['Price']<=scope]
    else:
        return 'NO GOOD PRICE'
    

#task4

def task_4_dbscan(data):
    df=data
    for i in range(len(df)):
        df.set_value(i,'Seq',i+1)
    day_lenth= math.sqrt(20 ** 2 / 3)
    radius = np.sqrt(np.square(20) + np.square(day_lenth))
    X = df[['Price','Seq']]
    db = DBSCAN(eps=radius, min_samples=3).fit(X)
    df['label'] = db.labels_

    unique_labels = list(set(db.labels_))

    for i in unique_labels:
        if len(df[df['label']==i])>=5:
            return df[df['label']==i][0:5]


#from_place='new york'
#to_place='South America'
#city_name='curacao'
#start_date= 5

#scrape_data_90(start_date=5, from_place='new york', to_place='South America', city_name='curacao')
#The from_place, to_place and city_name parameter should add " ' ", and start_data parameter should be integer.
