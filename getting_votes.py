
"""getting the votes from the previous collected links""" 

import requests
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
from functools import reduce
import glob

start = time.time()

files = glob.glob('legi2019*.csv')

read_links = []
for file in files:
    with open(file, newline='') as f:
        for row in csv.reader(f):
            read_links.append(row[0])
            
"""saving the links in a condensed way"""
with open('linkuri_2019.csv', 'w') as f:
    f.write('\n'.join(read_links))
     
"""making DataFrames to manage data, them merging into a final one"""    
voturi = []
for link in read_links:
            test = requests.get(link)     
            test = test.text
            soup = BeautifulSoup(test, 'lxml')
        
            law = soup.find(id="DescriereLunga_ctl00_DESCRIERE_LUNGALabel").text
            lw = law.split('P')[0]
            
            data = pd.read_html(test, header=0)[2]
            data['Pentru'].replace('X', 1, inplace=True)
            data['Contra'].replace('X', 2, inplace=True) 
            data['Abţineri'].replace('X', 3, inplace=True)
            data["Prezent - Nu au votat"].replace('X', 4, inplace=True) 
            data['Grup'].replace('Senatori fără apartenenţă la grupurile parlamentare', 'SFA', inplace=True)
            data[lw] = list(zip(data['Pentru'],data['Contra'],data['Abţineri'],data["Prezent - Nu au votat"]))
            data.drop(['Pentru','Contra','Abţineri',"Prezent - Nu au votat"], axis=1, inplace=True)
            data['Nume, Grup'] = data['Nume'].str.cat(data['Prenume'], sep=' ').str.cat(data['Grup'], sep=' ')
            data.drop(['Nume', 'Prenume', 'Grup'], axis=1, inplace=True)
            voturi.append(data)
            merged = reduce(lambda x, y: pd.merge(x, y, how='outer', on='Nume, Grup'), voturi)

            merged.to_csv('legi_2019.csv', encoding='utf-8-sig')


end = time.time()
print(end-start)

