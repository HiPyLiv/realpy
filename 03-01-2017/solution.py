#!/usr/bin/env python

import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

df = pd.read_csv('temperatures.txt', index_col=0, sep="\t\t", header=0, names=['run', 'temperature'], engine='python')

dat_files = [f for f in glob.glob(os.path.join('TOF', 'data', '*dat'))]
paths, indeces = [], []
for dat in dat_files:
    paths.append(dat)
    fname_parts = os.path.basename(dat).rsplit('.', 1)[0].split('_')
    indeces.append(int(fname_parts[0][3:]))
df['dat_file'] = pd.Series(paths, index=indeces)

L = 2.81387
Q = 17.5

total = np.zeros((0, 3))
for run in df.index:
    in_mat = np.loadtxt(df.loc[run].dat_file)
    out_mat = np.zeros((in_mat.shape[0], 3))
    # TODO: Revise this equation
    out_mat.T[0] *= 0.001 / (506.56 * L) / np.sin(Q)
    out_mat.T[1] *= 100 / in_mat.T[1].max()
    out_mat.T[2] = df.loc[run].temperature
    total = np.concatenate((total, out_mat), axis=0)
