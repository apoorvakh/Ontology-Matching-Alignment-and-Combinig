from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import csv

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


with open('Ontology/lsms_mics_map.csv') as csv_file:
    print similar("house_hold","houseHold")

    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    lsms = []
    mics = []

    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if row[0].strip() != "":
                lsms.append(row[0].strip())
            if row[1].strip() != "":
                mics.append(row[1].strip())
            line_count += 1


sim1 = fuzz.ratio("house_hold","houseHold")
sim2 = fuzz.token_sort_ratio("house_hold","houseHold")
sim3 = fuzz.token_set_ratio("".join("house_hold".split("_")),"houseHold")
print sim1, sim2, sim3

def fuzzSimilar(w1, w2):
    return fuzz.token_set_ratio("".join(w1.split("_")),"".join(w2.split("_")))

lics_misc_common = []

for l in lsms:
    maxSim = []
    for m in mics:
        maxSim.append( (fuzzSimilar(l, m), l, m) )
    maxSim.sort(reverse=True)
    #print maxSim[0]

for m in mics:
    maxSim = []
    for l in lsms:
        maxSim.append( (fuzzSimilar(m, l), m, l) )
        #if m == 'Gender/Sex' and l == 'Sex' :
            #print "-------------------", fuzzSimilar(m, l), m, l
    maxSim.sort(reverse=True)
    print maxSim[0]


