import pandas as pd
import numpy as np
import Feature_extractor
import pickle

T = pd.read_csv('test.csv',header=None)
T = Feature_extractor.feature_extract(X)

loaded_model = pickle.load(open('RF', 'rb'))

result = loaded_model.predict(T) # Contains an array of the predicted results
print('predicted>>',result)



