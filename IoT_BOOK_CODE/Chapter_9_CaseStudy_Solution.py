#Author Puneet Mathur
#Free to distribute with this header
# https://www.pmauthor.com/raspbian/

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 08 19:33:25 2019

@author: PUNEETMATHUR
"""
#importing python libraries
import pandas as pd 
from io import StringIO
import requests
import os
os.getcwd()

#Loading dataset
fname="cashcrop_Yield_dataset.csv"
agriculture= pd.read_csv(fname, low_memory=False, index_col=False)
df= pd.DataFrame(agriculture)
print(df.head(1))

#Checking data sanctity
print(df.size)
print(df.shape)
print(df.columns)
df.dtypes

#Check if there are any columns with empty/null dataset
df.isnull().any()
#Checking how many columns have null values
df.info()

#Using individual functions to do EDA
#Checking out Statistical data Mean Median Mode correlation
df.mean()
df.median()
df.mode()

#How is the data distributed and detecting Outliers
df.std()
df.max()
df.min()
df.quantile(0.25)*1.5
df.quantile(0.75)*1.5

#How many Outliers in the Total Food ordered column
df.columns
df.dtypes
df.set_index(['FarmID'])
df['Yield_per_ha'].loc[df['Yield_per_ha'] <=151.50000].count()
df['Yield_per_ha'].loc[df['Yield_per_ha'] >=159.285].count()

#Visualizing the dataset
df.boxplot(figsize=(17, 10))
df.plot.box(vert=False)
df.kurtosis()
df.skew()
import scipy.stats as sp
sp.skew(df['Yield_per_ha'])

#Visualizing dataset
df.plot()
df.hist(figsize=(10, 6))
df.plot.area()
df.plot.area(stacked=False)

#Now look at correlation and patterns
df.corr()

#Change to dataset columns and look at scatter plots closely
df.plot.scatter(x='Yield_per_ha', y='Soil_pH',s=df['Yield_per_ha']*2)
df.plot.hexbin(x='Yield_per_ha', y='Soil_pH', gridsize=20)

#Data Preparation Steps
#Step 1 Split data into features and target variable
# Split the data into features and target label
cropyield = pd.DataFrame(df['Yield_per_ha'])

dropp=df[['Iron mg/kg','Copper mg/kg','Crop','Center','FarmID','Yield_per_ha']]
features= df.drop(dropp, axis=1)
cropyield.columns
features.columns


#Step 2 Shuffle & Split Final Dataset
# Import train_test_split
from sklearn.cross_validation import train_test_split
from sklearn.utils import shuffle

# Shuffle and split the data into training and testing subsets
features=shuffle(features,  random_state=0)
cropyield=shuffle(cropyield,  random_state=0)
# Split the 'features' and 'income' data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, cropyield, test_size = 0.2, random_state = 0)

# Show the results of the split
print("Training set has {} samples.".format(X_train.shape[0]))
print("Testing set has {} samples.".format(X_test.shape[0]))

# Step 3 Model Building & Evaluation
#Creating the the Model for prediction

#Loading model Libraries
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

#Creating Linear Regression object
regr = linear_model.LinearRegression()

regr.fit(X_train,y_train)
y_pred= regr.predict(X_test)
#Printing Codfficients
print('Coefficients: \n',regr.coef_)
#print(LinearSVC().fit(X_train,y_train).coef_)
regr.score(X_train,y_train)
#Mean squared error
print("mean squared error:  %.2f" %mean_squared_error(y_test,y_pred))

#Variance score
print("Variance score: %2f"  % r2_score(y_test, y_pred))

#Plot and visualize the Linear Regression plot
plt.plot(X_test, y_pred, linewidth=3)
plt.show()

#Predicting Yield per hectare for a new farmland
X_test.dtypes
predicted= regr.predict([[26,1500,6.8,0.9,367,32,490,35]])
print(predicted)
