# compare algorithms

import numpy as np
from pandas import read_csv
from matplotlib import pyplot
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Load dataset
names = ['U', 'R', 'Up', 'Down', 'L', 'xMovement', 'yMovement', 'xPos', 'yPos']
dataset = read_csv('test1.csv', names=names)
print(dataset)
# Split-out validation dataset
array = dataset.values
X = array[1:, 1:8]
y = array[1:, 0]

X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1, shuffle=True)
# Spot Check Algorithms
models = [('LR', LogisticRegression(solver='liblinear', multi_class='ovr')), ('LDA', LinearDiscriminantAnalysis()),
          ('KNN', KNeighborsClassifier()), ('CART', DecisionTreeClassifier()), ('NB', GaussianNB()),
          ('SVM', SVC(gamma='auto'))]
# evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=2, random_state=1, shuffle=True)
    cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
# Compare Algorithms

pyplot.boxplot(results, labels=names)
pyplot.title('Algorithm Comparison')
pyplot.show()

# Ploting is fun


xPlot = array[1:, 7].astype(int)
yPlot = array[1:, 8].astype(int)


# data = np.array((xPlot.astype(int), yPlot.astype(int))).astype(int)

heatmap, xedges, yedges = np.histogram2d(xPlot, yPlot, bins=(512, 384))
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
pyplot.clf()

pyplot.imshow(heatmap.T, extent=extent, origin='lower')
pyplot.show()

# Make predictions on validation dataset
model = SVC(gamma='auto')
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)

# Evaluate predictions
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
