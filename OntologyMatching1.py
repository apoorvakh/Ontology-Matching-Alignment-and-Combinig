import string
import math
from scipy import spatial

classFileA = open("onto1.txt", 'r')
propertyFileA = open("PropertiesOA.txt", 'r')

classFileB = open("onto3.txt", 'r')
propertyFileB = open("PropertiesOB.txt", 'r')

# All concepts and properties from all ontologies (can be done pair-wise, to reduce memory for each vector).
vectorSpaceSet = set()

classLinesA = classFileA.readlines()
#!print classesA
classLinesB = classFileB.readlines()

propertyLinesA = propertyFileA.readlines()
propertyLinesB = propertyFileB.readlines()

domains = [classLinesA, classLinesB, propertyLinesA, propertyLinesB]
for d in domains:
    for l in d:
        vectorSpaceSet.update(set(l[:-1].split(" ")))

vectorSpace = list(vectorSpaceSet)
vectorSpace.sort()
#!print vectorSpaceSet, vectorSpace

# Construct a tree to maintain the inheritance of classes and get the levels for calculating the log.

# for each element in vectorSpace, we need to find its vector with respect to its ontology.

# get all concepts and their children and parents.
# concept : { 'C' : [ set of childern ] , 'P' : [set of parents ] }
conceptsA = dict()
conceptsB = dict()
#OA
a = set()
[a.update(s) for s in [set(l[:-1].split(" ")) for l in classLinesA]]
for c in a:
    conceptsA[c] ={'C':[], 'P':[]}
for l in classLinesA:
    split = l[:-1].split(" ")
    conceptsA[split[0]]['P'].append( split[1] )
    conceptsA[split[1]]['C'].append( split[0] )
#print conceptsA
#OB
b = set()
[b.update(s) for s in [set(l[:-1].split(" ")) for l in classLinesB]]
for c in b:
    conceptsB[c] ={'C':[], 'P':[]}
for l in classLinesB:
    split = l[:-1].split(" ")
    conceptsB[split[0]]['P'].append( split[1] )
    conceptsB[split[1]]['C'].append( split[0] )
#print conceptsB

# for properties I can just iterate through the lines in the file while calculating their vectors.

# but for getting all elements of an ontology, have to get property names
# propertyName : [ domain, range ]
#OA
propertiesA = dict()
for pL in propertyLinesA:
    split = pL[:-1].split(" ")
    print pL
    propertiesA[split[0]] = [split[1], split[2]]
#print propertiesA
#OB
propertiesB = dict()
for pL in propertyLinesB:
    split = pL[:-1].split(" ")
    propertiesB[split[0]] = [split[1], split[2]]
#print propertiesB



def parentLine(concepts, c, feature):
    if c == feature:
        return 1
    if len(concepts[c]['P']) == 0 :
        return 0
    for p in concepts[c]['P']:
        d = parentLine(concepts, p, feature)
        if d == 0:
            continue
        else :
            return 1 + d
    return 0

def childLine(concepts, c, feature):
    if c == feature:
        return 1
    if len(concepts[c]['C']) == 0 :
        return 0
    for p in concepts[c]['C']:
        d = parentLine(concepts, p, feature)
        if d == 0:
            continue
        else :
            return 1 + d
    return 0


vectorsOfOA = dict()
# vectors for concepts of A
for c in conceptsA:
    vectorsOfOA[c] = [] # dict()
    for feature in vectorSpace:
        weight = 0.0
        if feature == c:
            weight = 1.0
        else:
            # see if feature is in a child or a parent line
            #parent line
            if len(conceptsA[c]['P']) > 0:
                depth = parentLine(conceptsA, c, feature)
                depth = depth - 1
                #print c, feature, depth
                if depth > 0:
                    weight = math.log(1/depth+1)
            #child line
            if len(conceptsA[c]['C']) > 0:
                depth =childLine(conceptsA, c, feature)
                depth = depth - 1
                #print c, feature, depth
                if depth > 0:
                    weight = math.log(1/depth+1)

        vectorsOfOA[c].append(weight)
# vectors of properties of A
for p in propertiesA:
    vectorsOfOA[p] = [0 for f in vectorSpace]
    vectorsOfOA[p][vectorSpace.index(propertiesA[p][0])] = 1
    vectorsOfOA[p][vectorSpace.index(propertiesA[p][1])] = 1
    vectorsOfOA[p][vectorSpace.index(p)] = 1
print "#"*30
print "\nVectors for Ontology A :"
for k, v in vectorsOfOA.iteritems():
    print "%15s : %s" % (k, v)


vectorsOfOB = dict()
# vectors for concepts of A
for c in conceptsB:
    vectorsOfOB[c] = [] # dict()
    for feature in vectorSpace:
        weight = 0.0
        if feature == c:
            weight = 1.0
        else:
            # see if feature is in a child or a parent line
            #parent line
            if len(conceptsB[c]['P']) > 0:
                depth = parentLine(conceptsB, c, feature)
                depth = depth - 1
                #print c, feature, depth
                if depth > 0:
                    weight = math.log(1/depth+1)
            #child line
            if len(conceptsB[c]['C']) > 0:
                depth =childLine(conceptsB, c, feature)
                depth = depth - 1
                #print c, feature, depth
                if depth > 0:
                    weight = math.log(1/depth+1)

        vectorsOfOB[c].append(weight)
for p in propertiesB:
    vectorsOfOB[p] = [0 for f in vectorSpace]
    vectorsOfOB[p][vectorSpace.index(propertiesB[p][0])] = 1
    vectorsOfOB[p][vectorSpace.index(propertiesB[p][1])] = 1
    vectorsOfOB[p][vectorSpace.index(p)] = 1
print "#"*30
print "\nVectors for Ontology B :"
for k, v in vectorsOfOB.iteritems():
    print "%15s : %s" % (k, v)
"""
dataSetI = vectorsOfOA['Institution']
dataSetII = vectorsOfOA['Institution']
result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
print result
"""
# vector assignment :
print "#"*40
print "\nVector Assignment. Matching 2 most corresponding vectors from each ontology :\n"
# match a concept from one ontology to a concept in another ontology
print "_"*85
print "| %25s | %25s | %25s |" % ("A", "B", "Cosine Similarity")
print "_"*85

conceptMatches = []
for cA in conceptsA:
    maxSim = [0,""]
    for cB in conceptsB:
        result = 1 - spatial.distance.cosine(vectorsOfOA[cA],vectorsOfOB[cB])
        if maxSim[0] < result:
            maxSim = [result, cB]
    conceptMatches.append((cA, maxSim[1]))
    print "| %25s | %25s | %25s |" % (cA, maxSim[1], maxSim[0])
# 3/4 is right

propertyMatches = []
for pA in propertiesA:
    maxSim = [0,""]
    for pB in propertiesB:
        result = 1 - spatial.distance.cosine(vectorsOfOA[pA],vectorsOfOB[pB])
        if maxSim[0] < result:
            maxSim = [result, pB]
    propertyMatches.append((pA, maxSim[1]))
    print "| %25s | %25s | %25s |" % ( pA, maxSim[1], maxSim[0])
print "_"*85

tp = 0
tn = 0
fp = 0
fn = 0
for m in conceptMatches:
    if m[0] == m[1]:
        tp = tp+1

classFileA.close()
classFileB.close()
propertyFileA.close()
propertyFileB.close()



