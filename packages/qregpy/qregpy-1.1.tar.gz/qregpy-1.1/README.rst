# QReg Repository

## Overview

This project implements the Query-Centric Regression, named QReg.
QReg is a ensemble methods based on various base regression models.

Current QReg support linear, polynomial, decision tree, xgboost, gboosting regression as its base models.

## Dependencies
Python 3.6 or higher, requires scipy, xgboost, numpy, scikit-learn

###  How to install
``pip install qregpy``

###  How to use
```
from qregpy import qreg
import pandas as pd

# load the files
df = pd.read_csv("/data/10k.csv")
headerX = ["ss_list_price", "ss_wholesale_cost"]
headerY = "ss_wholesale_cost"

# prepare X and y
X = df[headerX].values
y = df[headerY].values

# train the regression using base models linear regression and XGBoost regression.
reg = qreg.QReg(base_models=["linear","xgboost"], verbose=True).fit(X, y)

# make predictions
reg.predict([[93.35, 53.04], [60.84, 41.96]])
```

---------------
