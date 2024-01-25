import pandas as pd
df = pd.read_csv('train.csv')

#convertendo age
#forma 1
#df1 = df['Delivery_person_Age'].replace('NaN ', 'NaN').astype(int)
#forma 2
select_rows = df['Delivery_person_Age'] != 'NaN'
df1 = df.loc[select_rows, :]
print(df1)



