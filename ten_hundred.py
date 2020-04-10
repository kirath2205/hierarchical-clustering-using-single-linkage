import pandas as pd
import math
import numpy as np

def load_data(filepath):
    dataset=pd.read_csv(filepath)
    return dataset

def calculate_x_y(time_series):
    del time_series['Province/State']
    del time_series['Country/Region']
    del time_series['Lat']
    del time_series['Long']
    data_list=time_series.values.tolist()
    k=data_list[len(data_list)-1]
    x=0
    y=0
    k1=0
    k2=0
    flag=0
    count=0
    list_x=list()
    list_y=list()
    for i in range(len(data_list)-2,-1,-1):
        if(data_list[i]<=k/10 and flag==0):
            x=count+1
            
            flag=1
        k1=data_list[i]
        list_x.append(k1)
        count=count+1
    count=0
    for i in range(len(data_list)-2,-1,-1):
        if(flag==1 and data_list[i]<=k/100):
            y=count-x+1
            flag=2
            k2=data_list[i]
            list_y.append(k2)
        count=count+1
    if(len(list_x)==0):
        x=np.nan
    if(len(list_y)==0):
        y=np.nan
    if(k==0):
        x=np.nan
        y=np.nan
    list_x_y=list()
    list_x_y.append(x)
    list_x_y.append(y)

    return list_x_y
        

def euclidean_distance(list1,list2):
    distance=math.sqrt((abs(list1[0]-list2[0])**2)+(abs(list1[1]-list2[1])**2))
    return distance



def distance_matrix(list1,list2):
    index_1=0
    index_2=0
    smallest=euclidean_distance(list1[0],list2[0])
    for i in range(len(list1)):
       for k in range(len(list2)):
           if(euclidean_distance(list1[i],list2[k])<smallest):
               smallest=euclidean_distance(list1[i],list2[k])
               index_1=i
               index_2=k
    return index_1,index_2,smallest


def hac(dataset):
    list_valid_enteries=list()
    for index,data in dataset.iterrows():
        list_x_y=calculate_x_y(data)
        if(not(np.isnan(list_x_y[0]))):
            if(not(np.isnan(list_x_y[1]))):
                list_valid_enteries.append(list_x_y)
    
    matrix=list()
    row=list()
    dictionary={}
    for index in range(len(list_valid_enteries)):
        dictionary[index]=[]
    for i in range(len(list_valid_enteries)):
        dictionary[i].append(list_valid_enteries[i])
    length1=len(list_valid_enteries)
    
    for i in range(len(list_valid_enteries)-1):
        
        distance=10000000
        cluster1=0
        cluster2=0
        for point in dictionary:
            
            for point2 in dictionary:
                
                i1,i2,smallest=distance_matrix(dictionary[point],dictionary[point2])
                
                if(smallest<distance and point!=point2):
                    distance=smallest
                    cluster1=point
                    cluster2=point2
                    
        if(cluster1<=cluster2):
            index_new_cluster=cluster1

        elif(cluster2<cluster1):
            index_new_cluster=cluster2

        dictionary[length1]=list()
        dictionary[length1]+=(dictionary[cluster1])
        dictionary[length1]+=(dictionary[cluster2])
        length1=length1+1
        if(cluster1<=cluster2):
            row.append(cluster1)
            row.append(cluster2)

        elif(cluster1>cluster2):
            row.append(cluster2)
            row.append(cluster1)
        row.append(distance)
        row.append(len(dictionary[cluster1])+len(dictionary[cluster2]))

        matrix.append(row.copy())
        row.clear()
        del dictionary[cluster1]
        del dictionary[cluster2]
    final_matrix=np.array(matrix)
    print(final_matrix) 
    return final_matrix
         
    

hac(load_data('time_series_covid19_confirmed_global.csv'))


