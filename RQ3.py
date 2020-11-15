#-------------RQ3_1---------------------

import pandas as pd
dataset = pd.read_csv("/home/sssiyam/Desktop/2019-Oct.csv",header="infer",
                      parse_dates=['event_time'],date_parser=pd.to_datetime)
def plot_RQ3():
    
    x = input('please insert the category:')

    catagorised=dataset[dataset.category_code == x ]
    catagorised2=catagorised[catagorised.brand.notnull()]
    catagorised3=catagorised2[catagorised2.event_type=='purchase']
    import matplotlib.pyplot as plt
    plt.figure()
    catagorised3.groupby('brand').price.mean().plot()
    plt.title('Average price of products for each Brand', fontsize=15)
    plt.xlabel('Brand Names')
    plt.ylabel('Average prices')
    plt.show()
plot_RQ3()

#------------RQ3_2--------------------

#Here we have applied groupby functions for more than one filed, 'catagory_code & 'brand' on our dataset {filter1}, as the task was to find out 
#the bran with the highest average price for each catagories.
#Then we have applied mean() function for the price of the products to calculate the average price of product for each brand on each catagory grouped.
#On filter2 we have again used groupby by 'catagory_code' and we sorted the price on ascending order using apply() function.
#We had to change the column name as it was overlapping with the index name and creating ambiguity. 
#Then on 'HighestAvgPrc' we have used groupby for the last time by 'CategoryCode' and tried out to find out the highest average price for each catagory.
#In the end we sorted the average price on ascending orders using sort_values() function.

filter1=dataset.groupby(['category_code','brand'], as_index = False).price.mean()
filter2=filter1.groupby('category_code').apply(pd.DataFrame.sort_values,'price',ascending = False)
filter2.columns=['CategoryCode','brand','price'] #colnames have been changed to avoid confusion with inedx name / col name ambiguous
HighestAvgPrc= filter2.groupby('CategoryCode').max()
HighestAvgPrc.sort_values('price')

