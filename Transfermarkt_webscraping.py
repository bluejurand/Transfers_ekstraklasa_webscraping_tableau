# -*- coding: utf-8 -*-
"""
Created on Mon May 25 10:04:01 2020

@author: mjur1
"""

import pandas as pd
import bs4, requests
from copy import deepcopy

year_start = 9
year_end = 19
seasons = list(range(year_start, year_end+2))
seasons = ["{0:0=2d}".format(seasons[n]) for n in range(0, len(seasons))]

transfers_dict={}
for x in range(0, len(seasons)-1):
    transfers_dict['transfers{}'.format(seasons[x])]=[]
    
transfers_dict_copy = {}

#for t in range(0, len(seasons)-1):
for t in enumerate(seasons[:-1]):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
    productUr1 = "https://www.transfermarkt.pl/pko-ekstraklasa/transfers/wettbewerb/PL1/plus/?saison_id=20{}&s_w=&leihe=0&intern=0".format(seasons[t])

    res = requests.get(productUr1, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content,'lxml')

    tables = soup.find_all('table')
    
    i = 0
    for table in tables:
        i += 1
        if i > 3:
            df = pd.read_html(str(table))
            transfers_dict['transfers{}'.format(seasons[t])].append(df[0].dropna(thresh=3))

    player_nationality = soup.find_all(class_="zentriert nat-transfer-cell")
    club_nat = soup.find_all(class_="no-border-links verein-flagge-transfer-cell")
    table_header = soup.find_all(class_="table-header")
    transfers_dict_copy['transfers{0}{1}'.format(
        seasons[t], seasons[t+1])] = deepcopy(transfers_dict['transfers{}'.format(seasons[t])])

    k = 1
    l = 0
    for j in range(0, len(transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])])):
        # Check transfer list type if it is in or out
        if j % 2 == 0:
            transfer_type = 'Klub oddający'
            transfer_kind = 'Kupno'
        else:
            transfer_type = 'Klub pozyskujący'
            transfer_kind = 'Sprzedaż'
        for i in range(0, len(transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])][j])):
            l += 1
            transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])][j].loc[i, "Narodowość"] = player_nationality[l].find('img').get('title')
            transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])][j].loc[i, "Rodzaj transferu"] = transfer_kind
            if not club_nat[i].find('a').text in ['Nieznany', 'Bez klubu', 'Koniec kariery']:
                transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])][j].loc[i, transfer_type] = club_nat[i].find('img').get('title')
            elif club_nat[i].find('a').text == 'Nieznany':
                transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])][j].loc[i, transfer_type] = 'Nieznana'
            else:
                transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])][j].loc[i, transfer_type] = '-'
        if (j % 2 == 0 and j != 0):
            k += 1
        transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])][j].insert(
            len(transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])][j].columns),
            'Dotyczy klubu',table_header[k].find_all('a')[1].text)
        l += 1
        
# Change dictonary data to one dataframe
transfers_newdict = {}
for t in range(0, len(seasons)-1):
    for j in range(0, len(transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])])):
        if j % 2 == 0:
            in_out = "Kupno"
            club_in_out = 'oddający'
            footballer = 'Nabytki'
        else:
            in_out = "Sprzedaż"
            club_in_out = 'pozyskujący'
            footballer = 'Odejścia'
        transfers_dict_copy['transfers{0}{1}'.format(seasons[t],seasons[t+1])][j] = transfers_dict_copy['transfers{0}{1}'.format(seasons[t],seasons[t+1])][j].rename(columns={'Klub {}'.format(club_in_out): 'Klub pozyskujący/oddający państwo', 'Klub {}.1'.format(club_in_out): 'Klub pozyskujący/oddający nazwa'})
        transfers_dict_copy['transfers{0}{1}'.format(seasons[t],seasons[t+1])][j] = transfers_dict_copy['transfers{0}{1}'.format(seasons[t],seasons[t+1])][j].rename(columns={'{}'.format(footballer): 'Piłkarz', '{}'.format(footballer): 'Piłkarz'})
    transfers_newdict['transfers{0}{1}'.format(seasons[t], seasons[t+1])] = pd.concat(transfers_dict_copy['transfers{0}{1}'.format(seasons[t], seasons[t+1])], sort=False)#, keys=transfers_dict_copy.keys())

# Unpack a dictionary of dataframes and set key as column value
final_df = pd.DataFrame()
for key, value in transfers_newdict.items():
    df = value
    df.loc[:,'Sezon'] = '20{0}/20{1}'.format(key[-4:-2], key[-2:])
    final_df = pd.concat([df, final_df], ignore_index=True, sort=False)
final_df

# Save final dataframe as csv file
final_df.to_csv('Transfers_Ekstraklasa_from_2009_2010.csv')#, index=False)
