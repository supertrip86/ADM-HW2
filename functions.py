import numpy as np
                
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