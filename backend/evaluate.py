import csv
from app.detector import detect

rows = list(csv.DictReader(open("data/evaluation_dataset.csv", encoding="utf-8")))
tp=tn=fp=fn=0
for row in rows:
    actual = row["label"] == "malicious"
    predicted = detect(row["prompt"])["decision"] == "BLOCK"
    if actual and predicted: tp += 1
    elif not actual and not predicted: tn += 1
    elif not actual and predicted: fp += 1
    else: fn += 1
accuracy = (tp+tn)/len(rows)
precision = tp/(tp+fp) if tp+fp else 0
recall = tp/(tp+fn) if tp+fn else 0
f1 = 2*precision*recall/(precision+recall) if precision+recall else 0
print({"samples":len(rows),"accuracy":round(accuracy,3),"precision":round(precision,3),"recall":round(recall,3),"f1":round(f1,3),"tp":tp,"tn":tn,"fp":fp,"fn":fn})
