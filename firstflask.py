from flask import Flask, render_template, request, url_for, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import json
import urllib3
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

http = urllib3.PoolManager()

app = Flask(__name__)




current_supply_and_demand_url="http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet"
response = http.request('GET',current_supply_and_demand_url)
soup=BeautifulSoup(response.data, "html.parser")

tables = soup.findAll("table")
depth2 = []
depth3 = []

for t in tables:
  if len(t.find_parents("table")) == 2:
    depth2.append(t)



"""summary detail"""
x=StringIO(depth2[2])
dfsummary = pd.read_html(x, header=0)
dfsummary1=dfsummary[0]
dfsummary1.columns = ['Summary', 'Values']
print dfsummary1


"""Generation detail"""

x=StringIO(depth2[3])
dfgeneration = pd.read_html(x, header=1)
dfgeneration1=dfgeneration[0]

"""Interchange"""
x=StringIO(depth2[4])
dfinterchange = pd.read_html(x, header=1)
dfinterchange1=dfinterchange[0]



for t in tables:
  if len(t.find_parents("table")) == 3:
    depth3.append(t)

print len(depth3)
"""get coal data"""

x=StringIO(depth3[0])
dfs = pd.read_html(x, header=1)
df0=dfs[0]
df0['Generation_Type'] = 'COAL'

print df0


x=StringIO(depth3[1])
dfs = pd.read_html(x)
df1=dfs[0]

"""Get Gas Data"""

simple_cycle_list=[]
combined_cycle_list=[]
cogeneration_list=[]

test=0
i=0
type=0


while i < len(df1):

	if df1[0][i] =='Simple Cycle':
		i=i+1
		type=1
		continue

	elif df1[0][i] =='Cogeneration':
		i=i+1
		type=2
		continue


	elif df1[0][i] =='Combined Cycle':
		i=i+1
		type=3
		continue


	if type ==1:
		simple_cycle_list.append(df1.loc[i])
	elif type ==2:
		cogeneration_list.append(df1.loc[i])
		test=2
	elif type ==3:
		combined_cycle_list.append(df1.loc[i])

	i=i+1

keys = ['ASSET','MC','TNG', 'DCR', 'Generation_Type']
combined_cycle_dictionary = {}
simple_cycle_dictionary={}
cogeneration_dictionary={}







for i in keys:
    combined_cycle_dictionary[i] = None

combined_cycle_list.pop(0)
asset=[]
mc=[]
tng=[]
dcr=[]
Generation_Type=[]
combined_cycle_data=[]
i=0
while i <len(combined_cycle_list):
	temp=combined_cycle_list[i].to_dict()
	asset.append(temp.pop(0))
	mc.append(int(temp.pop(1)))
	tng.append(int(temp.pop(2)))
	dcr.append(int(temp.pop(3)))
	Generation_Type.append('Combined Cycle')
	i += 1

combined_cycle_data.append(asset)
combined_cycle_data.append(mc)
combined_cycle_data.append(tng)
combined_cycle_data.append(dcr)
combined_cycle_data.append(Generation_Type)



dfcombined_cycle = pd.DataFrame(combined_cycle_data)
dfcombined_cycle = dfcombined_cycle.transpose()
dfcombined_cycle.columns = ["ASSET", "MC", "TNG", "DCR", "Generation_Type"]

dfcombined_cycle['MC'] = dfcombined_cycle['MC'].astype('int64')
dfcombined_cycle['TNG'] = dfcombined_cycle['TNG'].astype('int64')
dfcombined_cycle['DCR'] = dfcombined_cycle['DCR'].astype('int64')



for i in keys:
    simple_cycle_dictionary[i] = None

simple_cycle_list.pop(0)
asset=[]
mc=[]
tng=[]
dcr=[]
Generation_Type=[]
cogeneration_data=[]
i=0
while i <len(simple_cycle_list):
	temp=simple_cycle_list[i].to_dict()
	asset.append(temp.pop(0))
	mc.append(int(temp.pop(1)))
	tng.append(int(temp.pop(2)))
	dcr.append(int(temp.pop(3)))
	Generation_Type.append('Simple Cycle')
	i += 1

cogeneration_data.append(asset)
cogeneration_data.append(mc)
cogeneration_data.append(tng)
cogeneration_data.append(dcr)
cogeneration_data.append(Generation_Type)



dfcogeneration = pd.DataFrame(cogeneration_data)
dfcogeneration = dfcogeneration.transpose()
dfcogeneration.columns = ["ASSET", "MC", "TNG", "DCR", "Generation_Type"]

dfcogeneration['MC'] = dfcogeneration['MC'].astype('int64')
dfcogeneration['TNG'] = dfcogeneration['TNG'].astype('int64')
dfcogeneration['DCR'] = dfcogeneration['DCR'].astype('int64')





for i in keys:
    cogeneration_dictionary[i] = None

simple_cycle_list.pop(0)
asset=[]
mc=[]
tng=[]
dcr=[]
Generation_Type=[]
cogeneration_data=[]
i=0
while i <len(simple_cycle_list):
	temp=simple_cycle_list[i].to_dict()
	asset.append(temp.pop(0))
	mc.append(int(temp.pop(1)))
	tng.append(int(temp.pop(2)))
	dcr.append(int(temp.pop(3)))
	Generation_Type.append('Simple Cycle')
	i += 1

cogeneration_data.append(asset)
cogeneration_data.append(mc)
cogeneration_data.append(tng)
cogeneration_data.append(dcr)
cogeneration_data.append(Generation_Type)



dfsimple_cycle = pd.DataFrame(cogeneration_data)
dfsimple_cycle = dfsimple_cycle.transpose()
dfsimple_cycle.columns = ["ASSET", "MC", "TNG", "DCR", "Generation_Type"]

dfsimple_cycle['MC'] = dfsimple_cycle['MC'].astype('int64')
dfsimple_cycle['TNG'] = dfsimple_cycle['TNG'].astype('int64')
dfsimple_cycle['DCR'] = dfsimple_cycle['DCR'].astype('int64')


"""Get Hydro Data"""
x=StringIO(depth3[2])
dfs = pd.read_html(x, header=1)
df2=dfs[0]
df2['Generation_Type'] = 'HYDRO'

"""Get Wind Data"""

x=StringIO(depth3[3])
dfs = pd.read_html(x, header=1)
df3=dfs[0]
df3['Generation_Type'] = 'WIND'


"""Get BIOMASS AND OTHER DATA"""
x=StringIO(depth3[4])
dfs = pd.read_html(x, header=1)
df4=dfs[0]
df4['Generation_Type'] = 'BIOMASS AND OTHER'




for i in keys:
    simple_cycle_dictionary[i] = None

simple_cycle_list.pop(0)
asset=[]
mc=[]
tng=[]
dcr=[]
Generation_Type=[]
simple_cycle_data=[]
i=0
while i <len(simple_cycle_list):
	temp=simple_cycle_list[i].to_dict()
	asset.append(temp.pop(0))
	mc.append(int(temp.pop(1)))
	tng.append(int(temp.pop(2)))
	dcr.append(int(temp.pop(3)))
	Generation_Type.append('Simple Cycle')
	i += 1

simple_cycle_data.append(asset)
simple_cycle_data.append(mc)
simple_cycle_data.append(tng)
simple_cycle_data.append(dcr)
simple_cycle_data.append(Generation_Type)



dfsimple_cycle = pd.DataFrame(simple_cycle_data)
dfsimple_cycle = dfsimple_cycle.transpose()
dfsimple_cycle.columns = ["ASSET", "MC", "TNG", "DCR", "Generation_Type"]

dfsimple_cycle['MC'] = dfsimple_cycle['MC'].astype('int64')
dfsimple_cycle['TNG'] = dfsimple_cycle['TNG'].astype('int64')
dfsimple_cycle['DCR'] = dfsimple_cycle['DCR'].astype('int64')

df_row = pd.concat([df0, dfcombined_cycle,dfsimple_cycle,dfcogeneration,df2,df3,df4])
df_row=df_row.reset_index(drop=True)
print df_row

json_units = df_row.to_json(orient='index')
json_generation_summary=dfgeneration1.to_json(orient='index')
json_interchange=dfinterchange1.to_json(orient='index')
json_summary=dfsummary1.to_json(orient='index')


@app.route("/test", methods=['GET','POST'])
def test():
    return json_units


@app.route("/generation_summary", methods=['GET','POST'])
def test2():
    return json_generation_summary

@app.route("/interchange", methods=['GET','POST'])
def test3():
    return json_interchange

@app.route("/Summary", methods=['GET','POST'])
def test4():
    return json_summary



if __name__ == "__main__":
  app.run()
