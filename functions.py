import numpy as np

def ops_per_session(dataset):
    sessions = set(dataset['user_session'])

    d = {}

    for session in sessions:
        events = dataset[dataset.user_session==session].event_type
        for event in events:
            if session in d:
                if event in d[session]:
                    d[session][event] += 1
                else:
                    d[session][event] = 1
                d[session]['seq'].append(event)
            else:
                d[session] = {}
                d[session][event] = 1
                d[session]['seq'] = [event]
            
    return d

def complete_funnels(d):
    complete = 0
    
    for i in d:
        if len(d[i]) == 3:
            complete += 1

    return complete