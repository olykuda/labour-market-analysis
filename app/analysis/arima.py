#%pylab inline
from app import models
#from .forecast import ForecastModel
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
#import statsmodels.api as sm


def invboxcox(y, lmbda):
    if lmbda == 0:
        return np.exp(y)
    else:
        return np.exp(np.log(lmbda*y+1)/lmbda)

#
# class ARIMA:
#     # def __init__(self):
#     #     df = self.prepare_data()





