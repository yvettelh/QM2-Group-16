import pandas

df = pandas.read_csv('data/raw/yearly_charts.csv')

for i in range(0, 310):
    df = df.loc[20*i:]
    df2 = df.head(20)
    df2.to_csv('data/raw/final_unprocessed'+ str(i + 1)+'.csv')