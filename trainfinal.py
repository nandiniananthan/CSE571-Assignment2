import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
import Feature_extractor
import pickle

dataval1 = pd.read_csv('Data/meald.csv')
dataval2 = pd.read_csv('Data/nomeal.csv')

Final_dataval1 = pd.DataFrame(Feature_extractor.feature_extract(dataval1))
Final_dataval2 = pd.DataFrame(Feature_extractor.feature_extract(dataval2))

print("Data Loaded .....")
# import pdb; pdb.set_trace()
Final_dataval1['5'] = 1
Final_dataval2['5'] = 0

Final_data = pd.concat([Final_dataval1,Final_dataval2],ignore_index=True, sort =False)

# Preparing to split out validation dataset
array = Final_data.values
X = array[:,0:5]
Y = array[:,5]
validation_size = 0.2

seed = 42

# Splitting out training set
X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y,test_size=validation_size, random_state=seed)
kf = KFold(n_splits=5)
kf.get_n_splits(X)


# K Nearest Neighbor
knn_accuracies = {}
for k in range(25,100):
    model = KNeighborsClassifier(n_neighbors=k,algorithm='auto')
    model.fit(X_train,Y_train)
    Y_predictionsval = model.predict(X_test)
    correct_or_no = np.array(Y_predictionsval) - np.array(Y_test)
    numbers_correct = np.sum(correct_or_no == 0)
    total_samples = len(correct_or_no)
    knn_accuracies[str(k)] = numbers_correct/total_samples

pickle.dump(model, open('KNN', 'wb'))



key_max = max(knn_accuracies.keys(), key=(lambda k: knn_accuracies[k]))
print('Accuracy of best K value (%d)\t\t%f' % (int(key_max),knn_accuracies[key_max]))

# Random Forest
model = RandomForestClassifier(criterion='entropy', n_estimators=12,
                                random_state=1, n_jobs=2)
model.fit(X_train,Y_train)
Y_predictionsval = model.predict(X_test)

correct_or_no = np.array(Y_predictionsval) - np.array(Y_test)
numbers_correct = np.sum(correct_or_no == 0)
total_sample = len(correct_or_no)
print('Accuracy of RF: %.2f' % (numbers_correct/total_sample))
pickle.dump(model, open('RF', 'wb'))