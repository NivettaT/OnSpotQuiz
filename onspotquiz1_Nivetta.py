# -*- coding: utf-8 -*-
"""OnSpotQuiz1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19ZX1gf6E7e2B2oVWfX97Rj9PmDdH81VB
"""

import pandas as pd
import numpy as np
import random
np.random.seed(42)
data = pd.read_csv('/content/DSAI-LVA-DATASET for Quiz.csv')
data.head()
data = data.drop('ParentEducation',axis = 1)
selected_values = ['Masters','Bachelors','High School','School','Not Educated']
random_values = [random.choice(selected_values) for _ in range(len(data))]
data['ParentEducation'] = random_values
data.head()
threshold = 50
for index, row in data.iterrows():
    if row['PreviousTestScore'] >= threshold and row['PreviousTestScore'] < 80:
        data.at[index, 'Pass'] = 'Pass with low score'
    elif row['PreviousTestScore'] >= 80:
        data.at[index, 'Pass'] = 'Pass with high score'
    else:
        data.at[index, 'Pass'] = 'Fail'
data.head()

data.info()

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
le = LabelEncoder()
data['ParentEducation']=le.fit_transform(data['ParentEducation'])
data['Pass']=le.fit_transform(data['Pass'])
data.head()

import seaborn as sns
import matplotlib.pyplot as plt
correlation_matrix = data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Heatmap of Correlation Matrix')
plt.show()

for i in data.columns:
  sns.histplot(data[i], kde=True)
  plt.title(f"Histplot of {i}")
  plt.xlabel(i)
  plt.ylabel('Frequency')
  plt.show()

sns.countplot(x='Pass', data=data)
plt.title('Countplot of Target Variable')
plt.xlabel('Pass')
plt.ylabel('Count')
plt.show()

split_ratio = 0.8
split_index = int(len(data) * split_ratio)

# Split the DataFrame
data_part1 = data.iloc[:split_index]
data_part2 = data.iloc[split_index:]

# Write data to separate files
data_part1.to_csv('Train.csv', index=False)
data_part2.to_csv('Test.csv', index=False)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

train_data = pd.read_csv('/content/Train.csv')
test_data = pd.read_csv('/content/Test.csv')

X_train, y_train = train_data.drop('Pass', axis=1), train_data['Pass']
X_test, y_test = test_data.drop('Pass', axis=1), test_data['Pass']

lr = LogisticRegression()
lr.fit(X_train, y_train)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

lr_pred = lr.predict(X_test)
rf_pred = rf.predict(X_test)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
knn_pred = knn.predict(X_test)

acc_score_rf = accuracy_score(y_test,rf_pred)
print("Accuracy score of random forest: ",acc_score_rf)
acc_score = accuracy_score(y_test,lr_pred)
print("Accuracy score of Logistic Regression: ",acc_score)
acc_score_knn = accuracy_score(y_test,knn_pred)
print("Accuracy score of knn: ",acc_score_knn)