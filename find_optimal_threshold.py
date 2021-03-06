from numpy import sqrt
from numpy import argmax
from numpy import arange
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import f1_score
from matplotlib import pyplot

# generate dataset
X, y = make_classification(n_samples=10000, n_features=2, n_redundant=0, n_clusters_per_class=1, weights=[0.99], flip_y=0, random_state=7)

print(X.shape, y.shape)

X

y

# split into train/test sets
trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.4, random_state=7, stratify=y)

print(trainX.shape, testX.shape, trainy.shape, testy.shape)

# fit a model
model = LogisticRegression(solver='lbfgs')
model.fit(trainX, trainy)

# predict probabilities
yhat = model.predict_proba(testX)

print(yhat.shape)

yhat

# keep probabilities for the positive outcome only
yhat = yhat[:, 1]

print(yhat.shape)

yhat

"""##Optimal Threshold for ROC Curve"""

# calculate roc curves
fpr, tpr, thresholds = roc_curve(testy, yhat)

print(fpr.shape, tpr.shape, thresholds.shape)

fpr

tpr

thresholds

# calculate the g-mean for each threshold
gmeans = sqrt(tpr * (1-fpr))

gmeans

# locate the index of the largest g-mean
ix = argmax(gmeans)

ix

print('Best Threshold=%f, G-Mean=%.3f' % (thresholds[ix], gmeans[ix]))

# plot the roc curve for the model
pyplot.figure(figsize=(10,8))
pyplot.plot([0,1], [0,1], linestyle='--', label='No Skill')
pyplot.plot(fpr, tpr, marker='.', label='Logistic')
pyplot.scatter(fpr[ix], tpr[ix], marker='o', color='black', label='Best')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
pyplot.legend()
# show the plot
pyplot.show()

# get the best threshold
J = tpr - fpr
ix = argmax(J)
best_thresh = thresholds[ix]
print('Best Threshold=%f' % (best_thresh))

"""##Optimal Threshold for Precision-Recall Curve"""

# calculate pr-curve
precision, recall, thresholds = precision_recall_curve(testy, yhat)

# convert to f score
fscore = (2 * precision * recall) / (precision + recall)

print(fscore.shape)

fscore

# locate the index of the largest f score
ix = argmax(fscore)
print('Best Threshold=%f, F-Score=%.3f' % (thresholds[ix], fscore[ix]))

ix

# plot the roc curve for the model
pyplot.figure(figsize=(10,8))
no_skill = len(testy[testy==1]) / len(testy)
pyplot.plot([0,1], [no_skill,no_skill], linestyle='--', label='No Skill')
pyplot.plot(recall, precision, marker='.', label='Logistic')
pyplot.scatter(recall[ix], precision[ix], marker='o', color='black', label='Best')
# axis labels
pyplot.xlabel('Recall')
pyplot.ylabel('Precision')
pyplot.legend()
# show the plot
pyplot.show()

"""##Default Threshold of 0.5"""

# predict labels
yhat = model.predict(testX)

print(yhat.shape)

yhat

# evaluate the model
score = f1_score(testy, yhat)
print('F-Score: %.5f' % score)

"""##Optimal Threshold Tuning"""

# predict probabilities
yhat = model.predict_proba(testX)

yhat.shape

yhat

# keep probabilities for the positive outcome only
probs = yhat[:, 1]

probs.shape

probs

# define thresholds
thresholds = arange(0, 1, 0.001)

thresholds.shape

thresholds

# apply threshold to positive probabilities to create labels
def to_labels(pos_probs, threshold):
  return (pos_probs >= threshold).astype('int')

# evaluate each threshold
scores = [f1_score(testy, to_labels(probs, t)) for t in thresholds]

len(scores)

scores

# get best threshold
ix = argmax(scores)
print('Threshold=%.3f, F-Score=%.5f' % (thresholds[ix], scores[ix]))

ix

