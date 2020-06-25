import bs4
import requests
from fill_each_season_data import fill_club_subtables, extract_transfer_table

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
        first_irrlevant_tables = 3
        
        current_season_dictionary = [ extract_transfer_table(table) for table in all_tables[first_irrlevant_tables:] ]
        current_season_dictionary = fill_club_subtables(current_season_dictionary, soup)
        transfers_dict[transfers_name] = current_season_dictionary
    return transfers_dict
