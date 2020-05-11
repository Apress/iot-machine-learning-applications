#Author Puneet Mathur
#Free to distribute with this header
# https://www.pmauthor.com/raspbian/


# -*- coding: utf-8 -*-
"""
Author: Puneet Mathur
Copyright 2020
Free to copy this code with following attribution text: Author Puneet Mathur, www.PMAuthor.com
"""

import pandas as pd
import sqlite3
conn = sqlite3.connect('C:\\ machinemon.db')
#df.to_sql(name='tempdata', con=conn)
curr=conn.cursor()
#query="INSERT INTO TEMPERATURE VALUES(" +"'" + str(datetime.date(datetime.now())) + "'" +"," + "'" + str(datetime.time(datetime.now())) + "'"+ "," + "'" + str(tem) +  "'" + "," + "'" + tempstatus +"'" + ")"   
df = pd.read_sql_query("select * from fielddata;", conn)
print(df)
#curr.execute(query)
#conn.commit()

#Looking at data
print(df.columns)
print(df.shape)
#Looking at datatypes
print(df.dtypes)
df.tail(1)

#Checking for missing values
print(df.isnull().any())

#EDA- Exploratory Data Analysis
import numpy as np
print("----------EDA STATISTICS---------------")
pd.option_context('display.max_columns', 40)
with pd.option_context('display.max_columns', 40):
    print(df.describe(include=[np.number]))

#Correlation results
print("----------Correlation---------------")
with pd.option_context('display.max_columns', 40):
    print(df.corr())

#Dividing data into features and target
target=df['Calldrop']
nm=['CID1','CID2','Speed','OutsideTemperature','OutsideHumidity','SignalStrength','BatteryLevel']
features=df[nm]
with pd.option_context('display.max_columns', 40):
    features.head(1)
    target.head(1)

#Building the Model
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split( features, target, test_size=0.25, random_state=0)

from sklearn.linear_model import LogisticRegression

lr  = LogisticRegression()
lr.fit(x_train, y_train)
# Returns a NumPy Array
# Predict for One Observation (image)
lr.predict(x_test)

predictions = lr.predict(x_test)

# Use score method to get accuracy of model
score = lr.score(x_test, y_test)
print(score)

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
import numpy as np

cm = metrics.confusion_matrix(y_test, predictions)
print(cm)

plt.figure(figsize=(9,9))
sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
plt.ylabel('Actual Calldrops');
plt.xlabel('Predicted Calldrops');
all_sample_title = 'Accuracy Score: {0}'.format(score)
plt.title(all_sample_title, size = 15);

plt.figure(figsize=(7,7))
plt.imshow(cm, interpolation='nearest', cmap='Pastel1')
plt.title('Confusion matrix', size = 15)
plt.colorbar()
tick_marks = np.arange(1)
plt.xticks(tick_marks, ["0", "1"], rotation=45, size = 15)
plt.yticks(tick_marks, ["0", "1"], size = 15)
plt.tight_layout()
plt.ylabel('Actual Calldrops', size = 15)
plt.xlabel('Predicted Calldrops', size = 15)
width, height = cm.shape
for x in range(width):
 for y in range(height):
  plt.annotate(str(cm[x][y]), xy=(y, x), 
  horizontalalignment='center',
  verticalalignment='center')
plt.show()
