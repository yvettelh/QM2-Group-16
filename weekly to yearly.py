import pandas
import datetime


df = pandas.read_csv('data/raw/weekly_charts.csv')
df.drop(columns = ['last-week','peak-rank','weeks-on-board'], inplace = True)
df['date'] = pandas.to_datetime(df['date'])

output = pandas.DataFrame()
for year in range(1960,2022):
    start_date = datetime.datetime(year, 1, 1)
    end_date = datetime.datetime(year, 1, 7)
    temp = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    output = pandas.concat([output, temp], axis=0, join="outer")


output.reset_index( drop = True, inplace=True)
output['date'] = output['date'].dt.year
output.rename(columns={"date": "year"}, inplace = True)
print( output.head())
output.to_csv('data/raw/yearly_charts.csv')
output.head(1000).to_csv('data/raw/yearly_charts_test.csv')
output.head(100).to_csv('data/raw/yearly_charts_test_tiny.csv')