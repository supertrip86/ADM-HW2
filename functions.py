import pandas as pd
from collections import Counter
import numpy as np
import itertools
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


def rateOfCompleteFunnels(df):
    '''
    We consider the whole dataset (which includes all the months we are observing) and create from 
    it several groups, each one containing all the actions each user has ever performed in our shop 
    (the possible actions are: "view", "cart", "purchase"). We then convert the result into a dictionary, 
    where each key is represented by the user_id, and each value is the list of all its recorded actions. 
    As a second step, we extract from the dictionary all the items that contains at least one "view",
    one "cart" and one "purchase" event, and store them in the "users_with_funnels" variable. 
    All checks are necessary, as there are items in the dataset where purchases have been made without 
    previously recording "views" or "carts" events**.
    With the third step we generate, out of the previous variable, another dictionary, containing the number 
    of times each one of the three events occurs in the list. Since we know we are only dealing with elements 
    that contains complete funnels, we simply take the minimum value out of each list, and that value is going 
    to be the number of times each user has performed a complete funnel.
    Eventually, we have a dictionary that stores the exact number of complete funnels made by each user. 
    Users that haven't made at least a complete funnel are not included.
    Another thing we can do, is to see the rate of users that performed a complete funnel among all users.
    '''

    events_per_user = df.groupby(['user_id']).event_type.apply(list).to_dict()
    users_with_funnels = {key: events_per_user[key] for key in events_per_user if (('purchase' in events_per_user[key]) & ('view' in events_per_user[key]) & ('cart' in events_per_user[key]))}
    events_count = {key: [users_with_funnels[key].count(x) for x in users_with_funnels[key]] for key in users_with_funnels}
    complete_funnels_per_user = {key: min(events_count[key]) for key in events_count }
    dataframe_funnels = pd.DataFrame(complete_funnels_per_user.items(), columns=['User ID','Complete Funnels'])
    rate = round(len(complete_funnels_per_user) / len(events_per_user),2)

    return events_per_user, dataframe_funnels, rate


def mostFrequentOperationPerSession(df):
    '''
    We calculate the average number of times each event occurs in each user session. We then plot the result.
    '''

    summed_events = df.groupby(['event_type']).event_type.count()
    n_sessions = len(df.groupby(['user_session']))
    events_list = summed_events.to_dict()
    mean_by_session = summed_events / n_sessions

    plt.figure(figsize=(16, 6))
    plt.hist(events_list, weights=mean_by_session)
    return plt.show()


def averageViewsBeforeCart(df, events_per_user):
    '''
    We make use of the variable "events_per_user" defined in RQ1 - 1 to generate a dictionary containing
    all the views in each user_session until a "cart" or "purchase" event is detected. Then we calculate 
    how many times per session the user views products around the shop, and eventually the average of all 
    these values is printed.
    '''

    get_views_until_cart = {key: list( itertools.takewhile(lambda x: (x=='view'), events_per_user[key] )) for key in events_per_user}
    get_views_number = {key: len(get_views_until_cart[key]) for key in get_views_until_cart}
    views_list = dict.values(get_views_number)
    probability = round(sum(views_list) / len(views_list),2)

    return probability


def purchaseProbabilityAfterCart(df, events_per_user):
    '''
    Again, we make use of the variable "events_per_user" defined in RQ1 - 1, this time to extract all the 
    sessions where the user has put some products in the cart at least once (variable: "potentially_customers"), 
    and all the users that have both added products to the cart and purchased them (variable: "customers").
    The probability is given by the ratio: customers / potentially customers
    Also in this case, calculations would be easier if we could assume that every item, before being purchased, has 
    been viewed and inserted in the cart. Unfortunately, even though it is counterintuitive, this doesn't seems to be the case.
    '''

    potentially_customers = {key: events_per_user[key] for key in events_per_user if ('cart' in events_per_user[key])}
    customers = {key: events_per_user[key] for key in events_per_user if (('purchase' in events_per_user[key]) & ('cart' in events_per_user[key]))}
    ratio = round(len(customers) / len(potentially_customers),2)

    return ratio


def getSoldProductsByCategoryPerMonth(df_list):
    '''
    We iterate over all the datasets contained in df_list. Each element corresponds to a given month. 
    For each dataset, we filter only the rows reporting the sale of a product (the "purchase" event). 
    Then, we group all elements by category, and count the event types (that are now only the purchases). 
    Eventually, we plot each month's sales per product.
    '''

    months = []

    for i in range(len(df_list)):
        months.append(df_list[i][df_list[i].event_type=='purchase'].groupby(['category_code']).event_type.count().reset_index())
    
    return months


def plotSoldProductsByCategoryPerMonth(df, month):
    '''
    Plot the given dataframe as a histogram.
    '''

    df.plot(kind="bar",figsize=(16,10))
    plt.xlabel('Products')
    plt.ylabel('Sales')
    plt.legend((month,))
    plt.twinx().set_xticklabels(df["category_code"])
    plt.show()

    return plt.show()


def plotMostVisitedSubcategories(df):
    '''
    In this case, we refer to the entire dataset of all months. We filter the dataset to get only 
    the events where the user has 'viewed' a product, we select the 'category_code' column and split 
    it into subcategories. If children subcategories are found, we take the first child as our target, 
    otherwise the parent is taken. We group the data based on our target category/subcategory by means 
    of the "Counter" library. Eventually, we plot the result.
    '''
    
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
    '''
    From the dataset, we take the columns we need (event_type and category_code), we extract the events 
    where the user has 'purchased' a product. Then, we sort the values by "sales" in descending order, and 
    eventually print to screen the first 10 results.
    '''

    groups = df[['event_type','category_code']][df.event_type=='purchase'].groupby(['category_code'])
    result = groups[['event_type']].count().sort_values(by=['event_type'],ascending=False).head(10)

    return result


def findOverallConversionRate(df):
    '''
    After grouping the dataset by product_id and event_type, we create two variables: the total number 
    of purchases (n_purchase) and the total number of views (n_views). We output the conversion rate of 
    the store as the ratio between the total number of purchases and the total number of views.
    '''

    groups = df.groupby(['category_code','event_type'])

    n_purchase = groups.filter(lambda x: (x['event_type'] == 'purchase').any() ).event_type.count()
    n_views = groups.filter(lambda x: (x['event_type'] == 'view').any() ).event_type.count()

    conversion_rate = round(n_purchase / n_views,3)

    return conversion_rate

def plotSoldProductsByCategory(df):
    '''
    Same question as RQ2 - 1, only this time we consider the whole dataset, which contains all months
    '''

    n_purchase = df[df.event_type=="purchase"].groupby(['category_code']).event_type.count().reset_index()

    n_purchase.plot(kind="bar",figsize=(16,10))
    plt.xlabel('Products')
    plt.ylabel('Sales')
    plt.twinx().set_xticklabels(n_purchase["category_code"])
    plt.show()
    
    return plt.show()
                
    
def findConversionRatePerCategory(df):
    '''
    We first remove from the dataset the event_type "cart", which is not useful. After that, we groupby the
    columns "category_code" and "event_type", and then count the number of times each "event_type" is 
    repeated per product. The result is stored in a dictionary "d". We iterate through "d" to generate the 
    "products" and "conversion_rates" elements of the list "k", that are needed to plot the requested function. 
    The intermediate dictionary "g" is created to help keeping track of the progress of the iterations over "d". 
    The dictionary "k" is sorted in descending order relatively to its values (the conversion rates), and its 
    elements are associated to x (products) and y (conversion rates). 
    The variables "x" and "y" are finally used to plot the result.
    '''

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
    '''
    First, we create a dataset named "customers" by filtering all the purchases made on our store. 
    We then group the result into several groups, each one containing all the purchases made by each user. After 
    that, we calculate the income made per user by means of the "price" column, and save the result in descending order. 
    We now have a list of all the users according to how much they spent on our store.
    With such information, it is now possible to create two different subsets: the first one containing the 20% 
    of the customers that have spent the most (sales_20), and the second one with the remaining 80% (sales_80).
    At this point, we can observe that 70% of the money we earned during the given observation period are only 
    coming from 20% our customers. The more we increase the size of out dataset, the more we can expect this ratio 
    to tend to 80/20, hence confirming the Pareto principle.
    '''

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

    plt.figure(figsize=(16,2))
    plt.barh([1,2], data)
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.yticks([1,2],ticks)
    plt.xlabel('Percentage of Sales')
    
    return plt.show()