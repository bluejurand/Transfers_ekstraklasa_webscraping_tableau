# Transfers ekstraklasa webscraping tableau
![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg) 
![Python 3.6](https://img.shields.io/badge/python-3.3-blue.svg) 
![Spyder 4.1.3](https://img.shields.io/badge/spyder-4.1.3-black) 
![BeautifulSoup 4.9.0](https://img.shields.io/badge/BeautifulSoup-4.9.0-blueviolet) 
![Requests 2.23.0](https://img.shields.io/badge/requests-2.23.0-gray) 
![Pandas 0.22.0](https://img.shields.io/badge/pandas-0.22.0-green.svg)  
Repository presenting Transfermarkt data (https://www.transfermarkt.pl/) web scraping for 
analysis of transfers in Polish ekstraklasa in years 2009/2010 - 2019/2020.

## Motivation

To practice web scraping and data visualization in Tableau. 

## Installation

Python is a requirement (Python 3.3 or greater, or Python 2.7). Recommended enviroment is Anaconda distribution to install Python and Spyder (https://www.anaconda.com/download/).

__Installing dependencies__  
To install can be used pip command in command line.  
  
	pip install -r requirements.txt

__Installing python libraries__  
Exemplary commands to install python libraries:  
 
	pip install numpy  
	pip install pandas  
	pip install bs4  

__Running code__  
Everything is executed from file main.py. Go to directory where code is downoladed"\source_code\" and run a command: 

	py main.py
	

Links to transfermarkt web pages and corresponding to them league names are in files in folder "..\input_files\". 
Resulting csv files for every league and one combining all data together are saved in folder "..\output_files\".

## Code examples

	# get_data_from_soup.py module
	import bs4
	import requests
	from fill_each_season_data import create_empty_dataframe, wirte_tables_to_one_dictionary, fill_club_subtables

	def create_data_for_one_league(transfers_dict, league_link):
		for season_counter, transfers_name in enumerate(transfers_dict):
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)' \
				'Chrome/41.0.2228.0 Safari/537.36',
				}
			transfermarkt_link =  '{0}{1}{2}'.format(league_link[:-24], transfers_name[-4:-2], league_link[-22:])
		
			res = requests.get(transfermarkt_link, headers=headers)
			res.raise_for_status()
			soup = bs4.BeautifulSoup(res.content, 'lxml')
			all_tables = soup.find_all('table')
			current_season_dictionary = transfers_dict[transfers_name][:]
			current_season_dictionary = wirte_tables_to_one_dictionary(all_tables, current_season_dictionary)
			current_season_dictionary = fill_club_subtables(current_season_dictionary, soup)
			transfers_dict[transfers_name] = current_season_dictionary
		return transfers_dict

	# fill_each_season_data.py module
	import pandas as pd

	def create_empty_dataframe(first_season_year_start, last_season_year_start):
		seasons_year_start = map("{0:0=2d}".format, range(first_season_year_start, last_season_year_start+1))
		seasons_year_end = map("{0:0=2d}".format, range(first_season_year_start+1, last_season_year_start+2))
		seasons_year_start_list = list(seasons_year_start)
		seasons_year_end_list = list(seasons_year_end)
		names_for_yeach_season = ['transfers' + year_start + year_end for year_start, year_end in zip(seasons_year_start_list, seasons_year_end_list)]
		transfers_dict = dict.fromkeys(list(names_for_yeach_season), [])
		return transfers_dict

	def wirte_tables_to_one_dictionary(tables, transfers_dict_one_season):
		first_irrlevant_tables = 3
		relevant_tables = tables[first_irrlevant_tables:]
		for table in relevant_tables:
			transfers_dataframe = pd.read_html(str(table))
			transfers_dict_one_season.append(transfers_dataframe[0].dropna(thresh=3))
		return transfers_dict_one_season

	def fill_club_subtables(transfers_dict_one_season, soup):
		from fill_each_club_data import (fill_empty_columns, go_to_next_club, get_club_name,
										 fill_dotyczy_klubu_column, MakeCounter, corect_column_names)

		club_counter = 2
		player_nationality_counter = MakeCounter()

		for club_subtable_counter, _ in enumerate(transfers_dict_one_season):

			current_transfers_dict_copy = transfers_dict_one_season[club_subtable_counter][:]
			current_transfers_dict_copy = fill_empty_columns(current_transfers_dict_copy, club_subtable_counter, player_nationality_counter, soup)

			club_counter = go_to_next_club(club_subtable_counter, club_counter)
			club_name = get_club_name(soup, club_counter)
			current_transfers_dict_copy = fill_dotyczy_klubu_column(current_transfers_dict_copy, club_name)
			current_transfers_dict_copy = corect_column_names(current_transfers_dict_copy, club_subtable_counter)
			transfers_dict_one_season[club_subtable_counter] = current_transfers_dict_copy
			player_nationality_counter()
		return transfers_dict_one_season 

## Key Concepts
__Web scraping__  

__Data visualization__  

__Data wrangling__  
  
![Tableau screenshot](https://github.com/bluejurand/Transfers_ekstraklasa_webscraping_tableau/blob/master/Transfers_from_2009_2010_tableau_screenshot.png)
Link to Tableau Public file (dynamic version) - <https://public.tableau.com/views/Transfersekstraklasa09-20/Dashboard1?:display_count=y&publish=yes&:origin=viz_share_link>