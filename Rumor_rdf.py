#encoding=utf-8
import csv

title = "<http://www.kbqa.com/Rumors_%03d> <http://www.kbqa.com/properties#title_value> \"%s\"."

mainSummary = "<http://www.kbqa.com/Rumors_%03d> <http://www.kbqa.com/properties#mainSummary_value> <http://www.kbqa.com/%s> ."
body = "<http://www.kbqa.com/%s> <http://www.kbqa.com/properties#body_value> \"%s\". "

triples = []

i = 0 #计数器
f = open('Rumors.csv','r')
reader = csv.reader(f)
for row in reader:
    i = i + 1

    title_str = title % (i, row[0])
    triples.append(title_str)

    mainSummary_str = mainSummary % (i, row[1])
    triples.append(mainSummary_str)

    body_str = body % (row[1], row[2])
    triples.append(body_str)

filename = r'Rumors.nt'
with open(filename,"w+") as fd:
    fd.write("\n".join(triples))
fd.close()


