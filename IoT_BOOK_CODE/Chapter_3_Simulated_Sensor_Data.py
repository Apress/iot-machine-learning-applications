#Author Puneet Mathur
#Free to distribute with this header
# https://www.pmauthor.com/raspbian/

import pandas as pd
import sqlite3
conn = sqlite3.connect('machinemon.db')
#df.to_sql(name='tempdata', con=conn)
curr=conn.cursor()
#query="INSERT INTO TEMPERATURE VALUES(" +"'" + str(datetime.date(datetime.now())) + "'" +"," + "'" + str(datetime.time(datetime.now())) + "'"+ "," + "'" + str(tem) +  "'" + "," + "'" + tempstatus +"'" + ")"   
df = pd.read_sql_query("select * from machinedata;", conn)
print(df)
#curr.execute(query)
conn.commit()

#Looking at data
print(df.columns)
print(df.shape)
#Looking at datatypes
print(df.dtypes)
df['outage']=df['outage'].astype("int")
#Cleaning up and dummy variables
df['tempstatus'] = df['tempstatus'].map({'RED':2, 'ORANGE':1, 'GREEN':0})
df=df.drop('date',1)
df=df.drop('time',1)

#Checking for missing values
print(df.isnull().any())

#EDA- Exploratory Data Analysis
print("----------EDA STATISTICS---------------")
print(df.describe())
print("----------Correlation---------------")
print(df.corr())

#Dividing data into features and target
target=df['outage']
features=df.drop('outage',1)


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
plt.ylabel('Actual label');
plt.xlabel('Predicted label');
all_sample_title = 'Accuracy Score: {0}'.format(score)
plt.title(all_sample_title, size = 15);

plt.figure(figsize=(9,9))
plt.imshow(cm, interpolation='nearest', cmap='Pastel1')
plt.title('Confusion matrix', size = 15)
plt.colorbar()
tick_marks = np.arange(10)
plt.xticks(tick_marks, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], rotation=45, size = 10)
plt.yticks(tick_marks, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], size = 10)
plt.tight_layout()
plt.ylabel('Actual label', size = 15)
plt.xlabel('Predicted label', size = 15)
width, height = cm.shape
for x in xrange(width):
 for y in xrange(height):
  plt.annotate(str(cm[x][y]), xy=(y, x), 
  horizontalalignment='center',
  verticalalignment='center')
plt.show()
