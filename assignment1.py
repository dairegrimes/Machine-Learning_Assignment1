# Daire Grimes
# C14407812
from __future__ import division
import pandas as pd
import numpy as np


df = pd.read_csv('./data/DataSet.txt')


# Reading in the Feature names
feature_names = []
with open('./data/featureNames.txt', 'r') as features:
    for line in features:
        for word in line.split():
            feature_names.append(word)


df.columns = feature_names

# Separating the cont data from the cat data
df_cont = df.select_dtypes(include=[np.int64])
df_cat = df.select_dtypes(exclude=[np.int64])



#Cleans cont data
cont = df_cont.describe()
#Puts data in description
cont = cont.transpose()

#Cleans cat data
cat = df_cat.describe()
#Puts data in description
cat = cat.transpose()


# Adding in extra columns
catFeat = ['Miss_%', 'mode_%', '2nd_mode', '2nd_mode_freg', '2nd_mode_%']
contFeat = [ 'Miss_%','card']

for feature in contFeat:
    cont[feature]=""

for feature in catFeat:
    cat[feature]=""



# adding in data for cont
for feature in contFeat:
    for column in cont.index:

        if feature in 'Miss_%':
            # number of missing cols - number of cols
            cont[feature][column] = (df.shape[0] - cont['count'][column]) / df.shape[0] * 100
            # Getting the length for the cardinality
        elif feature == 'card':
            cont[feature][column] = len(df_cont[column].unique())


for feature in catFeat:

    for column in cat.index:


        dict1 = dict(df_cat[column].value_counts().head(2))

        if feature == 'Miss_%':
            numMissing = sum(df[column] == " ?")
            cat[feature][column] = (numMissing) / df.shape[0] * 100

        elif feature in 'mode_%':
            cat[feature][column] = cat['freq'][column] / cat['count'][column] * 100

        elif feature in '2nd_mode':
            cat[feature][column] = min(dict1, key=dict1.get)

        elif feature in '2nd_mode_freg':
            cat[feature][column] = dict1[min(dict1, key=dict1.get)]

        elif feature in '2nd_mode_%':
            cat[feature][column] = cat['2nd_mode_freg'][column] / cat['count'][column] * 100





# Dropping id
cat = cat.drop(['id'])

# Creating new column by creating the data frame again
cat.columns = ["Count", "card", "Mode", "Mode_Freq", "Miss_%", "Mode_%", "2nd_Mode", "2nd_mode_freg", "2nd_mode_%"]
cat_desc = cat[["Count","Miss_%", "card", "Mode", "Mode_Freq",  "Mode_%", "2nd_Mode", "2nd_mode_freg", "2nd_mode_%"]]

#adding in FEATURENAME as a heading
cat = cat_desc.rename_axis('FEATURENAME')

#adding to csv
cat.to_csv('./data/C14407812CAT.csv')



# Creating a new column
cont.columns = [ "Count", "Mean", "Std_Dev", "Min", "1st_Quart", "Median", "3rd_Quart", "Max", "Miss_%", "card"]
cont = cont[["Count", "Miss_%", "card", "Min", "1st_Quart", "Mean",   "Median", "3rd_Quart", "Max" ,"Std_Dev",]]

#adding in FEATURENAME as a heading
cont_desc = cont.rename_axis('FEATURENAME')
#adding to csv
cont_desc.to_csv('./data/C14407812CONT.csv')