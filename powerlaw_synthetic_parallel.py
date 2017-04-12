# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

df = pd.read_csv("./news_events_powerlaw.csv")
df["bucket"] = df["bucket"] + 1

def ksdistance(f1, f2):    
    cdf_f1 = [0.0]
    cdf_f2 = [0.0]
    for i in range(len(f1)):
        cdf_f1.append(cdf_f1[-1] + f1[i])
        cdf_f2.append(cdf_f2[-1] + f2[i])
    #print zip(cdf_f1, cdf_f2)
    tmplist = []
    for i in range(len(f1)+1):
        tmplist.append( float(abs(cdf_f1[i] - cdf_f2[i])) )
    return max(tmplist)

def bestgamma(degrees, thelist, kmin):
    gamma = -1
    est_tmp, est_n = 0, 0
    for j, p_j in zip(degrees[kmin:], thelist[kmin:]):
        f_j = p_j
        est_tmp +=  f_j * np.log( 1.0 * j / (degrees[kmin] - 0.5) )
        est_n += f_j 
    gamma = 1.0 + est_n / est_tmp
    
    #Eq. (2.5) in the paper "Power-law distributions in empirical data"
    C = 1.0 / sum([np.power(i,-gamma) for i in degrees[kmin:]]) 
    return gamma, C

def ideal(degrees, gammaval, C, kmin, m):
    tmp = np.zeros(len(degrees))
    for i, deg in zip(range(kmin,m,1), degrees[kmin:m]):
      tmp[i] = C * np.power(deg, -gammaval)
    return tmp

# set the lower bound
kmin = 2

gamma, C = bestgamma(df["bucket"], df["pdf"], kmin)
print "Fitting results:", gamma, C
f2 = ideal(df["bucket"], gamma, C, kmin, df.shape[0])
df['f2'] = pd.Series(f2, index=df.index)

# we just plot the part which has been used for fitting
df["pdf4fit"] = df["pdf"]
df["pdf4fit"][:kmin] = 0
df["pdf4fit"] = df["pdf4fit"] / (df["pdf4fit"].sum())
df.head()

print ksdistance(df["pdf4fit"], df["f2"])

# the fitted distribution
import struct

def synthetic(degrees, f2):
    np.random.seed(None)
    tmp = np.zeros(df.shape[0])
    for i in range(5000):
        deg = np.random.choice(degrees, p=f2)
        tmp[deg] += 1
    tmp = tmp / tmp.sum()
    return tmp

from joblib import Parallel, delayed

ks_list = []
def ks_list(df):
    f3 = synthetic(df.index, df['f2'])
    return ksdistance(df["pdf4fit"], f3) 

print Parallel(n_jobs=-1)(delayed(ks_list)(df) for _ in range(2500))
