import pandas

df = pandas.read_csv('election_2020_ca_bycounty_manual.csv')

df.rename(columns={'County':'COUNTY'}, inplace=True)
df['COUNTY'] = [s.upper() for s in df['COUNTY'].values]

others = list(df)
others.remove('COUNTY')
for col in others:
    newcol = []
    for val in df[col].values:
        if isinstance(val,str):
            val = int( val.replace(',','') )
        newcol.append(val)
    df[col] = newcol
#
