# Add the functions in this file
import json

def load_journal(json_file):
    # data will be a list of py dicts
    f = open(json_file)
    data = json.load(f)
    return data

def compute_phi(data, ev):
    #         number of times
    n11 = 0 # squirrel and event both happened
    n00 = 0 # squirrel and event both did not happen
    n10 = 0 # squirrel happened, event did not
    n01 = 0 # squirrel did not, event happened
    n1p = 0 # total squirrel happened
    n0p = 0 # total squirrel did not happen
    np1 = 0 # total event happened
    np0 = 0 # total event did not happen
    for day in range(len(data)):
        for event in data[day]["events"]:
            if event == ev:
                if data[day]["squirrel"]==True:
                    n11 += 1;
                    np1 += 1;
                    n1p += 1;
                else:
                    n01 += 1;
                    n0p += 1;
                    np1 += 1;
            else:
                if data[day]["squirrel"]==False:
                    n00 += 1;
                    n0p += 1;
                    np0 += 1;
                else:
                    n10 += 1;
                    np0 += 1;
                    n1p += 1;

    phi = (n11*n00 - n10*n01)/((n1p*n0p*np1*np0)**0.5)

    return phi

def compute_correlations(file):
    data = load_journal(file)
    list_events = []
    phi_events = []
    dict  = {}
    for entry in range(len(data)):
        for event in data[entry]["events"]:
            if event not in list_events:
                list_events.append(event)
                phi = compute_phi(data, event)
                phi_events.append(phi)
    d = {i:j for i,j in zip(list_events, phi_events)}
    #d = dict(zip(list_events, phi_events))
    return d

def diagnose(file):
    d = compute_correlations(file)
    temp = max(d.values())
    high_positive = [key for key in d if d[key]==temp]
    temp = min(d.values())
    high_negative = [key for key in d if d[key]==temp]

    return high_positive, high_negative
