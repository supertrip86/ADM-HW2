import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

dataset = pd.read_csv('./archive/2019-Nov.csv', header='infer', nrows=10000)

dataset.head()

sessions = set(dataset['user_session'])

d = {}
complete = 0

for session in sessions:
    events = dataset[dataset.user_session==session].event_type
    for event in events:
        if session in d:
            if event in d[session]:
                d[session][event] += 1
            else:
                d[session][event] = 1
        else:
            d[session] = {}
            d[session][event] = 1
            
for i in d:
    if len(d[i]) == 3:
        complete += 1

print(complete) # answer 1: 29 is the number of the complete funnels among all user_sessions (in a limited subset of n=10000)

fig, ax = plt.subplots()
dataset.event_type.value_counts(normalize=True).plot(ax=ax, kind='bar') # answer 2: the number of times (in percentage) each user performs one of the indicated operations (view, remove from cart, purchase) during a session