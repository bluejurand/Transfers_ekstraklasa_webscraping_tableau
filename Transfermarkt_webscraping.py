# -*- coding: utf-8 -*-
"""
Created on Mon May 25 10:04:01 2020

@author: mjur1
"""

import pandas as pd
import bs4, requests
from copy import deepcopy

def wirte_tables_to_one_dictionary(tables, current_transfers_string_1_year):
    first_irrlevant_tables = 3
    for table in tables[first_irrlevant_tables:]:
        transfers_dataframe = pd.read_html(str(table))
        transfers_dict[current_transfers_string_1_year].append(transfers_dataframe[0].dropna(thresh=3))    
    return transfers_dict

def fill_club_subtables(transfers_dict_copy, current_transfers_string_2_years):

    def fill_empty_coulmns(current_transfers_dict_copy, player_nationality_counter):
        
        def get_player_nationality(player_nationality_counter):
            current_player_nationality = player_nationality[player_nationality_counter].find('img').get('title')
            return current_player_nationality
        
        def check_if_player_have_next_club(table_counter, current_transfers_dict_copy):
            
            def check_transfer_type(club_subtable_counter):
                if club_subtable_counter % 2 == 0:
                    club_header_type = 'Klub oddający'
                else:
                    club_header_type = 'Klub pozyskujący'
                return club_header_type
            
            next_club_name = club_nat[club_country_counter].find('a').text
            club_header_type = check_transfer_type(club_subtable_counter)
            
            if not next_club_name in ['Nieznany', 'Bez klubu', 'Koniec kariery', 'Sperre', 'pauzuje']:
                next_club_country = club_nat[club_country_counter].find('img').get('title')
                current_transfers_dict_copy.loc[table_counter, club_header_type] = next_club_country
            elif next_club_name == 'Nieznany':
                current_transfers_dict_copy.loc[table_counter, club_header_type] = 'Nieznana'
            else:
                current_transfers_dict_copy.loc[table_counter, club_header_type] = '-'
            return current_transfers_dict_copy
        
        def check_transfer_type(club_subtable_counter):
            if club_subtable_counter % 2 == 0:
                transfer_kind = 'Kupno'
            else:
                transfer_kind = 'Sprzedaż'
            return transfer_kind
        
        club_country_counter = 0

        for table_counter, table_row in current_transfers_dict_copy.iterrows():
            player_nationality_counter += 1
            current_transfers_dict_copy.loc[table_counter, "Narodowość"] = get_player_nationality(player_nationality_counter)
            current_transfers_dict_copy.loc[table_counter, "Rodzaj transferu"] = check_transfer_type(club_subtable_counter)
            current_transfers_dict_copy = check_if_player_have_next_club(table_counter, current_transfers_dict_copy)
            club_country_counter += 1
            
        return current_transfers_dict_copy, player_nationality_counter    
    
    def go_to_next_club(club_subtable_counter, club_counter):
        if (club_subtable_counter % 2 == 0 and club_subtable_counter != 0):
            club_counter += 1
        return club_counter

    def get_club_name(table_header, club_counter):
        club_name = table_header[club_counter].find_all('a')[1].text
        return club_name
    
    def fill_Dotyczy_klubu_column(current_transfers_dict_copy, club_name):
        club_transfers_number = len(current_transfers_dict_copy.columns)
        current_transfers_dict_copy.insert(club_transfers_number, 'Dotyczy klubu', club_name)
        return current_transfers_dict_copy

    club_counter = 2
    player_nationality_counter = 0

    for club_subtable_counter, _ in enumerate(transfers_dict_copy[current_transfers_string_2_years]):

        current_transfers_dict_copy = transfers_dict_copy[current_transfers_string_2_years][club_subtable_counter]
        current_transfers_dict_copy, player_nationality_counter = fill_empty_coulmns(current_transfers_dict_copy, player_nationality_counter)

        club_counter = go_to_next_club(club_subtable_counter, club_counter)
        club_name = get_club_name(table_header, club_counter)
        current_transfers_dict_copy = fill_Dotyczy_klubu_column(current_transfers_dict_copy, club_name)
        player_nationality_counter += 1
    return transfers_dict_copy

year_start = 9
year_end = 19
seasons = list(range(year_start, year_end+2))
seasons = ["{0:0=2d}".format(seasons[n]) for n in range(0, len(seasons))]

transfers_dict={}
for x in range(0, len(seasons)-1):
    transfers_dict['transfers{}'.format(seasons[x])]=[]
    
transfers_dict_copy = {}

for season_counter, season in enumerate(seasons[:-1]):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
    selected_ligue_transfermarkt_link = ("https://www.transfermarkt.pl/pko-ekstraklasa/transfers/wettbewerb/" +
    "PL1/plus/?saison_id=20{}&s_w=&leihe=0&intern=0".format(season))

    res = requests.get(selected_ligue_transfermarkt_link, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content,'lxml')
    tables = soup.find_all('table')
    
    current_transfers_string_1_year = 'transfers{}'.format(season)
            
    transfers_dict = wirte_tables_to_one_dictionary(tables, current_transfers_string_1_year)

    player_nationality = soup.find_all(class_="zentriert nat-transfer-cell")
    club_nat = soup.find_all(class_="no-border-links verein-flagge-transfer-cell")
    table_header = soup.find_all(class_="table-header")
    
    current_transfers_string_2_years = 'transfers{0}{1}'.format(seasons[season_counter],
                                                        seasons[season_counter+1])
    
    transfers_dict_copy[current_transfers_string_2_years] = deepcopy(transfers_dict[current_transfers_string_1_year])

    transfers_dict_copy = fill_club_subtables(transfers_dict_copy, current_transfers_string_2_years)
        
# Change dictonary data to one dataframe
transfers_newdict = {}

for season_counter, season in enumerate(seasons[:-1]):
    current_transfers_string_2_years = 'transfers{0}{1}'.format(seasons[season_counter],
                                                        seasons[season_counter+1])
    for club_subtable_counter in range(0, len(transfers_dict_copy[current_transfers_string_2_years])):
        if club_subtable_counter % 2 == 0:
            in_out = "Kupno"
            club_in_out = 'oddający'
            footballer = 'Nabytki'
        else:
            in_out = "Sprzedaż"
            club_in_out = 'pozyskujący'
            footballer = 'Odejścia'
        transfers_dict_copy[current_transfers_string_2_years][club_subtable_counter] = transfers_dict_copy[current_transfers_string_2_years][club_subtable_counter].rename(columns={'Klub {}'.format(club_in_out): 'Klub pozyskujący/oddający państwo', 'Klub {}.1'.format(club_in_out): 'Klub pozyskujący/oddający nazwa'})
        transfers_dict_copy[current_transfers_string_2_years][club_subtable_counter] = transfers_dict_copy[current_transfers_string_2_years][club_subtable_counter].rename(columns={'{}'.format(footballer): 'Piłkarz', '{}'.format(footballer): 'Piłkarz'})
    transfers_newdict[current_transfers_string_2_years] = pd.concat(transfers_dict_copy[current_transfers_string_2_years], sort=False)#, keys=transfers_dict_copy.keys())

# Unpack a dictionary of dataframes and set key as column value
final_df = pd.DataFrame()
for key, value in transfers_newdict.items():
    transfers_dataframe = value
    transfers_dataframe.loc[:,'Sezon'] = '20{0}/20{1}'.format(key[-4:-2], key[-2:])
    final_df = pd.concat([transfers_dataframe, final_df], ignore_index=True, sort=False)
final_df

# Save final dataframe as csv file
final_df.to_csv('Transfers_Ekstraklasa_from_2009_2010_TEST.csv')#, index=False)
