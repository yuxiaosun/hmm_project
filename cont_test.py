from continous_hmm import continuoushmm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from sklearn.cluster import KMeans
hmm=continuoushmm(n=6,m=8,p=4,uniform_initialize=True)
print hmm.g
alpha=np.ones( (6,25))*1/25
beta=np.ones( (6,25) )*1/25
traindata=pd.read_csv("test.csv")
observations=traindata.ix[:,2:6]
observations=observations.as_matrix()
kmeans = KMeans(n_clusters=8)
cluster_no=kmeans.fit_predict(traindata.ix[:, 2:6].values)
Mujk=kmeans.cluster_centers_
Mumatrix=np.zeros ((6,8,4))
for j in xrange(6):
    for k in xrange(8):
        Mumatrix[j][k]=Mujk[k]
hmm.meansmatrix=Mumatrix
hmm.gaamamixcal(alpha,beta,observations)
