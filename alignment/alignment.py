import pandas as pd
import numpy as np
from scipy.interpolate import lagrange

path = "alignment/ex/entrada.csv"
df = pd.read_csv(path)

dt = align(df, 'x', 's', 0.5)

def align(df, x, y, h):
    X = df[x].values
    Y = df[y].values
    i = 0
    j = 1
    nrow = len(X)
    A = [[X[0], Y[0]]]
    while i < nrow and j < nrow:
        if X[j] == A[-1][0] + h:
            A.append([X[j], Y[j]])
        elif X[j] > A[-1][0] + h:
            L = lagrange(X[i:j+1], Y[i:j+1])
            A.append([A[-1][0] + h, L(A[-1][0] + h)])
        else:
            j = j + 1
            if X[i+1] >= A[-1][0]:
                i = i + 1
    dt = pd.DataFrame(A, columns=[x, y])
    return dt
