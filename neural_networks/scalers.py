""" Various data normalizers. Mostly useful
to handle NaN values better than sklearn. """
from sklearn.preprocessing import MinMaxScaler as SLMinMaxScaler
import numpy as np

class StandardScaler(object):
    """ Standardize mean and std, and impute nans to 0. """
    def __init__(self):
        self.mean = 0
        self.std = 0

    def fit(self, x):
        self.mean = np.nanmean(x, axis=0, keepdims=True)
        self.std = np.nanstd(x, axis=0, keepdims=True)
        self.std[self.std==0] = 1.

    def transform(self, x):
        x = np.array(x)
        x = (x - self.mean) / self.std
        x[np.isnan(x)] = 0
        return x

    def fit_transform(self, x):
        self.fit(x)
        return self.transform(x)

    def inverse_transform(self, y):
        return y * self.std + self.mean
 

class HalfScaler(object):
    """ Like StandardScaler, but does not rescale dimensions
    upwards from ignore_dim (inclusive) on axis 1. """
    def __init__(self, ignore_dim):
        self.scaler = StandardScaler()
        self.ignore_dim = ignore_dim

    def fit(self, x):
        self.scaler.fit(x[:, self.ignore_dim:])

    def transform(self, x):
        xtr = self.scaler.transform(x[:, self.ignore_dim:])
        return np.hstack([x[:, :self.ignore_dim], xtr])

    def fit_transform(self, x):
        self.fit(x)
        return self.transform(x)

    def inverse_transform(self, y):
        ytr = self.scaler.inverse_transform(y[:, self.ignore_dim:])
        return np.hstack([y[:, self.ignore_dim], ytr])

class MinMaxScaler(object):
    """
    Like sklearn's MinMaxScaler, but applies to multi-dimensional arrays.
    """
    def __init__(self, feature_range):
        self.feature_range=feature_range

    def fit(self, x):
        self.scaler = SLMinMaxScaler(feature_range=self.feature_range)
        self.scaler.fit(x.reshape(-1, 1))

    def transform(self, x):
        shape = x.shape
        return self.scaler.transform(x.reshape(-1, 1)).reshape(shape)

    def fit_transform(self, x):
        self.fit(x)
        return self.transform(x)

    def inverse_transform(self, y):
        shape = y.shape
        return self.scaler.inverse_transform(y.reshape(-1, 1)).reshape(shape)
