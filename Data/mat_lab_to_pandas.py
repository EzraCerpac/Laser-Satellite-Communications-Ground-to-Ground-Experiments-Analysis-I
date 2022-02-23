from matlab import *
import numpy as np
from scipy.io import loadmat  # this is the SciPy module that loads mat-files
import matplotlib.pyplot as plt
from datetime import datetime, date, time
import pandas as pd

mat = loadmat('Data/matlab/STB_dataset_11.mat')  # load mat-file
mdata = mat['measuredData']  # variable in mat file
mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
# * SciPy reads in structures as structured NumPy arrays of dtype object
# * The size of the array is the size of the structure array, not the number
#   elements in any particular field. The shape defaults to 2-dimensional.
# * For convenience make a dictionary of the data using the names from dtypes
# * Since the structure has only one element, but is 2-D, index it at [0, 0]
ndata = {n: mdata[n][0, 0] for n in mdtype.names}
# Reconstruct the columns of the data table from just the time series
# Use the number of intervals to test if a field is a column or metadata
columns = [n for n, v in ndata.iteritems() if v.size == ndata['numIntervals']]
# now make a data frame, setting the time stamps as the index
df = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
                  index=[datetime(*ts) for ts in ndata['timestamps']],
                  columns=columns)