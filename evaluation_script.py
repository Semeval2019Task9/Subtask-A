'''
Evaluation script for the Semeval 2019 Task 9 competition.
Written by Tobias Daudert
Contact: tobias.daudert@insight-centre.org

Input: submission.csv which has to be in the same folder as this script. The accepted structure is: id, sentence, prediction
Reference: goldstandard.csv which has to be in the same folder as this script.
Output: scores.txt
'''

import numpy as np
import csv
from sklearn.metrics import f1_score



def getf1_score(gdata, tdata):
	f1scoremicro = f1_score(gdata, tdata)
	return f1scoremicro


def f1_weight(v1,v2):
	gold_total, predicted_total = 0, 0
	gold_total = len(v1)
	predicted_total = len(v2)
	if (gold_total > 0):
		return np.absolute(float(predicted_total) / float(gold_total))
	else:
		return 0.0


def final_score(f1s, f1weight):
	return f1s * f1weight

def build_dicts(v1,v2):
	golddicttemp = []
	inputdicttemp = []

	for gold in v1:	
		for inputeval in v2:
			if gold == inputeval:
				golddicttemp.append(int(v1[gold]))
				inputdicttemp.append(int(v2[inputeval]))
				
	return [golddicttemp, inputdicttemp]

#This will store the result in scores.txt which you can find in the same folder as this script.
def writeresults(winput):
	file = open("scores.txt", "w")
	file.write("F1-SCORE: " + winput)
	file.close()


golddict = {}
inputdict = {}

#Place the goldstandard.csv and the submission.csv in the same folder as this evaluation script
#The structure of submission.csv has to be: "id, sentence, prediction" with prediction in [0,1]
inputfilename = "submission.csv"
filename = "goldstandard.csv"


with open(filename) as data_file:    
	Goldstandard = csv.reader(data_file, delimiter=',')
	for gold in Goldstandard:
		if len(gold[0]) > 0 and len(gold[2]) > 0:
			golddict[gold[0]] = int(gold[2])
with open(inputfilename) as data_file2:    
	Input = csv.reader(data_file2, delimiter=',')
	for inputt in Input:
		if len(inputt[0]) > 0 and len(inputt[2]) > 0:
			inputdict[inputt[0]] = int(inputt[2])



golddictlist = build_dicts(golddict,inputdict)[0]
inputdictlist = build_dicts(golddict,inputdict)[1]
f1score = getf1_score(golddictlist,inputdictlist)
f1weight = f1_weight(golddict,inputdict)
finsco = final_score(f1score, f1weight)
writeresults('%s' % finsco)



