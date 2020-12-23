import pandas as pd
import numpy as np
from scipy.interpolate import lagrange

path = "alignment/ex/entrada.csv"
df = pd.read_csv(path)

X = df['x'].values
Y = df['s'].values
h = 0.5

dt = align(X, Y, h)

def align(X, Y, h):
    i = 0
    j = 1
    nrow = len(df.index)
    A = [[X[0], Y[0]]]
    while i < nrow and j < nrow:
        if X[j] == A[-1][0] + h:
            A.append([X[j], Y[j]])
        elif X[j] > A[-1][0] + h:
            L = lagrange(X[i:j+1], Y[i:j+1]) # L = lagrange(X[i:j+1].values, Y[i:j+1].values) if is pd.Series
            A.append([A[-1][0] + h, L(A[-1][0] + h)])
        else:
            j = j + 1
            if A[-1][0] - X[i] > h:
                i = i + 1
    dt = pd.DataFrame(A, columns=['x','y'])
    return dt
