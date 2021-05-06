import pandas
import re


ef = pandas.ExcelFile('co-est2019-annres-06.xlsx')

df = ef.parse(0, skiprows=3)

df = df.iloc[1:59]

# rename county column 
pat = '\.([a-zA-Z\ ]{1,}) County'
counties = []
for s in df.iloc[:,0]:
    hit = re.match(pat, s)
    if hit is None:
        print(s)
        counties.append('')
    else:
        counties.append( hit.groups(0)[0].upper() )
#

df['COUNTY'] = counties