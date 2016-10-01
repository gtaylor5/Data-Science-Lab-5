# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import sqlite3
from bs4 import BeautifulSoup

# year|tropical_storms|hurricanes|major_hurricanes|deaths|damage|Strongest 

r = requests.get('https://en.wikipedia.org/wiki/Atlantic_hurricane_season')
soup = BeautifulSoup(r.text,'html.parser')
tables = soup.body.find_all('table')
data = []
for table in tables:
    table_rows = table.find_all('tr')
    for row in table_rows:
        columns = row.find_all('td')
        if len(columns) is 2 or 0:
            continue
        columns = [element.text.strip() for element in columns]
        data.append(columns)
  
final_data = []
for d in data:
    if len(d) == 0:
        continue
    if len(d) <= 9:
        d[4] = d[4].replace("~","")
        d[4] = d[4].replace("+","")
        d[4] = d[4].replace(",","")
        d[4] = d[4].replace("Not known","0")
        d[4] = d[4].replace("Unknown","0")
        d[4] = d[4].replace("None","0")
        d[4] = d[4].replace("Numerous","0")
        d[5] = d[5].replace("$","")
        d[5] = d[5].replace("+","")
        d[5] = d[5].replace("Unknown","1") #unknown = 1 million
        if "million" in d[5]:
            d[5] = d[5].replace("million","")
            d[5] = d[5].replace(u'\xa0',u' ')
        elif "billion" in d[5]:
            d[5] = d[5].replace("billion","")
            d[5] = d[5].replace(u'\xa0',u' ')
            d[5] = float(d[5])*1000
        else:
            if len(d) >=8:
                d[5] = d[5].replace(",","")
                d[5] = float(d[5])/1000000
    else:
        d[5] = d[5].replace("~","")
        d[5] = d[5].replace("+","")
        d[5] = d[5].replace(",","")
        d[5] = d[5].replace("Not known","0")
        d[5] = d[5].replace("Unknown","0")
        d[5] = d[5].replace("None","0")
        d[5] = d[5].replace("Numerous","0")
        d[6] = d[6].replace("$","")
        d[6] = d[6].replace("+","")
        d[6] = d[6].replace("Unknown","1") #unknown = 1 million
        d[6] = d[6].replace(">","")
        d[6] = d[6].replace(",","")
        if "million" in d[6]:
            d[6] = d[6].replace("million","")
            d[6] = d[6].replace(u'\xa0',u' ')
        elif "billion" in d[6]:
            d[6] = d[6].replace("billion","")
            d[6] = d[6].replace(u'\xa0',u' ')
            d[6] = float(d[6])*1000
        else:
            if len(d) >=8:
                d[6] = float(d[6])/1000000
    datas = [0]*4
    j = 0;
    for i in range(len(datas)):
        if len(d) <= 9:
            datas[i] = d[j]
            j+=1
        else:
            if j == 1:
                datas[i] = d[j]
                j+=1
            datas[i] = d[j]
            j+=1
    if d[4] is "Not known" or d[4] is "None" or d[4] is "Unknown":
        d[4] = 0 #zero if unknown
    elif d[4] is "Numerous":
        d[4] = 10 #numerous = 10
    else:
        if len(d) < 9:
            datas.append(d[4])
            if len(d) is 6:
                datas.append(0)
                datas.append("Strongest Storm: "+str(d[5]))
            elif len(d) is 7:
                datas.append(0)
                datas.append("Strongest Storm: "+str(d[5]))
                datas[6] += (" Notes: "+d[6])
            elif len(d) is 8:
                datas.append(d[5])
                datas.append("Strongest Storm: "+d[6])
                datas[6] += (" Notes: " + d[7])
            final_data.append(datas)
        elif len(d) is 9:
            datas.append(d[4])
            datas.append(d[5])
            datas.append("Strongest Storm: "+d[6])
            datas[6] += " Retired Names: "+str(d[7])
            datas[6] += (" Notes: " + d[8])
            final_data.append(datas)
        elif len(d) >= 10:
            datas.append(d[5])
            datas.append(d[6])
            datas.append("Strongest Storm: "+d[7])
            datas[6] += " Retired Names: "+str(d[8])
            datas[6] += (" Notes: " + d[9])
            final_data.append(datas)
                    
            



conn = sqlite3.connect('/home/gtaylor5/Desktop/atlantic_hurricanes.db')
print "success"
c = conn.cursor()
c.execute('''CREATE TABLE hurricanes (year int, tropicalstorms int, hurricanes int, majorhurricanes int, deaths int, damage int, notes text)''')
print "success"

for data in final_data:
    myTupe = (data[0],data[1],data[2],data[3],data[4],data[5],data[6])
    c.execute("insert into hurricanes values (?,?,?,?,?,?,?)", myTupe)
conn.commit()
for row in c.execute('SELECT * FROM hurricanes;'):
    print row

val = c.execute('SELECT * from hurricanes where damage = (select MAX(damage) FROM hurricanes);')
for i in val:
    print i
print "success"
    