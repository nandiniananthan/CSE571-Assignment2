import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import *
from sklearn.decomposition import PCA
from scipy.integrate import simps
from scipy.stats import kurtosis, skew
import scipy.stats

def feature_extract(fData):
    final_md = fData
    global FFT_Feature_Matrix
    FFT_coefficents_val = []
    # import pdb; pdb.set_trace()
    for it in range(final_md.shape[0]):
        FFT_coefficents_val.append(np.abs(np.fft.fft((final_md.iloc[it,::-1]))))
    FFT_Feature_Matrix = []

    for c in range(0,len(FFT_coefficents_val)):
        FFT_Feature_Matrix.append(FFT_coefficents_val[c][1:9]) # Take top 8

    CGM_Velocity= np.zeros(shape=(final_md.shape[0],30))
    for rowindex in range(0,final_md.shape[0]):
        for colindex in range(0,final_md.shape[1]-1):
            CGM_Velocity[rowindex,colindex] = final_md.iloc[rowindex,colindex]-final_md.iloc[rowindex,colindex+1]

    CGM_Velocity = pd.DataFrame(CGM_Velocity)
    Zero_crossing_List = np.zeros(shape=(final_md.shape[0],1))
    for rowindex in range(0,CGM_Velocity.shape[0]):
        for colindex in range(0,CGM_Velocity.shape[1]):
            if CGM_Velocity.iloc[rowindex,colindex] < 0.05:
                Zero_crossing_List[rowindex,0]=colindex

    Group_meanval1 = []
    Group_meanval2 = []
    Group_meanval3 = []
    Group_meanval4 = []
    Group_meanval5 = []

    for i in range(final_md.shape[0]):
        Group_meanval1.append(final_md.iloc[i,0:5].mean())
        Group_meanval2.append(final_md.iloc[i,6:11].mean())
        Group_meanval3.append(final_md.iloc[i,12:17].mean())
        Group_meanval4.append(final_md.iloc[i,18:23].mean())
        Group_meanval5.append(final_md.iloc[i,23:29].mean())

    Skewval1 = []
    Skewval2 = []
    Skewval3 = []
    Skewval4 = []
    Skewval5 = []
    
    Kurt1 = []
    Kurt2 = []
    Kurt3 = []
    Kurt4 = []
    Kurt5 = []
    for i in range(final_md.shape[0]):
        Skewval1.append(skew(final_md.iloc[i,0:5]))
        Skewval2.append(skew(final_md.iloc[i,6:10]))
        Skewval3.append(skew(final_md.iloc[i,11:15]))
        Skewval4.append(skew(final_md.iloc[i,16:20]))
        Skewval5.append(skew(final_md.iloc[i,21:24]))
        
        Kurt1.append(kurtosis(final_md.iloc[i,0:5]))
        Kurt2.append(kurtosis(final_md.iloc[i,6:10]))
        Kurt3.append(kurtosis(final_md.iloc[i,1:15]))
        Kurt4.append(kurtosis(final_md.iloc[i,16:20]))
        Kurt5.append(kurtosis(final_md.iloc[i,21:24]))
    
    feature_matrix = np.stack((
                              np.array(Group_meanval1),
                              np.array(Group_meanval2),
                              np.array(Group_meanval3),
                              np.array(Group_meanval4),
                              np.array(Group_meanval5),
                              np.array(Skewval1),
                              np.array(Skewval2),
                              np.array(Skewval3),
                              np.array(Skewval4),
                              np.array(Skewval5),
                              np.array(Kurt1),
                              np.array(Kurt2),
                              np.array(Kurt3),
                              np.array(Kurt4),
                              np.array(Kurt5)
                              ))

    feature_matrix = np.hstack((np.transpose(feature_matrix),
                            Zero_crossing_List,
                          np.array(FFT_Feature_Matrix),
                          ))
    feature_matrix_CSV = pd.DataFrame(feature_matrix).to_csv('feature_matrix_CSV',index=False)
    pca = PCA(n_components=5)
    reduced_matrix_val = pca.fit_transform(feature_matrix)
    return(reduced_matrix_val)