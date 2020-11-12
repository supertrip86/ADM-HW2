import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

def getData():
    months_list = ['October 2019', 'November 2019']
    csv_list = ['../../archive/2019-Oct.csv', '../../archive/2019-Nov.csv']
    df_list = []

    for filename in csv_list:
        df_list.append(pd.read_csv(filename, header='infer').dropna())

    df = pd.concat(df_list)
    
    return months_list, df_list, df


def plotSoldProductsByCategoryPerMonth(df, month):
    dd = df[df.event_type=='purchase'].groupby(['category_code']).event_type.count()
    
    plt.figure(figsize=(16,6))
    plt.plot(dd)
    plt.xticks(rotation='vertical')
    plt.xlabel('Products')
    plt.ylabel('Sales')
    plt.legend((month,))
    
    return plt.show()


def plotMostVisitedSubcategories(df):
    df_views = df[df.event_type=='view'].category_code
    subcategories = df_views.apply(lambda x: x.split('.')[1] if len(x.split('.')) > 1 else x.split('.')[0])
    count = Counter(list(zip(subcategories)))

    plt.figure(figsize=[16,5])
    plt.xticks(range(len(count)), labels=count.keys(), rotation='vertical')
    plt.xlabel('Subcategories')
    plt.ylabel('Views')
    plt.bar(range(len(count)), count.values())
    
    return plt.show()


def mostSoldProductsPerCategory(df):
    groups = df[['event_type','category_code']][df.event_type=='purchase'].groupby(['category_code'])
    result = groups[['event_type']].count().sort_values(by=['event_type'],ascending=False).head(10)

    return result


def findOverallConversionRate(df):
    groups = df.groupby(['category_code','event_type'])

    n_purchase = groups.filter(lambda x: (x['event_type'] == 'purchase').any() ).event_type.count()
    n_views = groups.filter(lambda x: (x['event_type'] == 'view').any() ).event_type.count()

    conversion_rate = n_purchase / n_views

    return conversion_rate

def plotSoldProductsByCategory(df):
    n_purchase = df[df.event_type=="purchase"].groupby(['category_code']).event_type.count()

    plt.figure(figsize=(16,6))
    plt.plot(n_purchase)
    plt.xticks(rotation='vertical')
    plt.xlabel('Products')
    plt.ylabel('Sales')
    
    return plt.show()
                
    
def findConversionRatePerCategory(df):
    d = df[df.event_type!="cart"].groupby(['category_code','event_type']).event_type.apply(lambda x: x.count()).sort_values(ascending=False).to_dict()

    g = {}
    k = {}

    for key in d:
        if key[0] in g:
            g[key[0]][key[1]] = d[key]

            cr = round(g[key[0]]['purchase'] / g[key[0]]['view'], 5)
            k[key[0]] = cr
        else:
            g[key[0]] = {}
            g[key[0]][key[1]] = d[key]

    x, y = zip(*sorted(k.items(), key=lambda x: x[1], reverse=True))

    plt.figure(figsize=(16,6))
    plt.bar(x, y)
    plt.xticks(rotation='vertical')
    plt.xlabel('Products')
    plt.ylabel('Conversion Rates')
    
    return plt.show()
    
    
def proveParetoPrinciple(df):
    customers = df[df.event_type=="purchase"].groupby(['user_id'])
    customers_by_sales = customers.price.sum().reset_index().sort_values('price', ascending=False)

    n = int(len(customers_by_sales)*(1/5))
    m = len(customers_by_sales) - n

    sales_20 = customers_by_sales.head(n)
    sales_80 = customers_by_sales.tail(m)

    ratio_20 = sales_20.price.sum() / customers_by_sales.price.sum()
    ratio_80 = sales_80.price.sum() / customers_by_sales.price.sum()

    data = [ratio_20, ratio_80]
    ticks = ['Best 20%', 'Other customers']

    plt.figure(figsize=(16,4))
    plt.barh([1,2], data)
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.yticks([1,2],ticks)
    plt.xlabel('Percentage of Sales')
    
    return plt.show()


    
# def ops_per_session(dataset):
#     sessions = set(dataset['user_session'])

#     d = {}

#     for session in sessions:
#         events = dataset[dataset.user_session==session].event_type
#         for event in events:
#             if session in d:
#                 if event in d[session]:
#                     d[session][event] += 1
#                 else:
#                     d[session][event] = 1
#                 if (event == 'view') and ('cart' not in d[session]) and ('purchase' not in d[session]):
#                     d[session]['views_before_cart'] += 1
                
#             else:
#                 d[session] = {}
#                 d[session][event] = 1
#                 d[session]['views_before_cart'] = 1
            
#     return d

# def getData(dataset):
#     d = ops_per_session(dataset)

#     data = {'funnels': 0, 'n_views': 0, 'n_purchase': 0, 'n_sessions': len(d), 'n_cart': 0}
    
#     for i in d:
#         if 'cart' in d[i] and 'purchase' in d[i]:
#             data['funnels'] += 1
#         if 'cart' in d[i]:
#             data['n_cart'] += 1
#             data['n_views'] += d[i]['view']
#         if 'purchase' in d[i]:
#             data['n_purchase'] += 1

#     return data

# def getSubcategory(category):
#     allsubcategories = category.split('.')

#     if len(allsubcategories) > 1:
#         return allsubcategories[1]

#     return allsubcategories[0]