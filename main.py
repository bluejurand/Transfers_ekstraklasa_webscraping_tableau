from fill_each_season_data import create_empty_dataframe
from get_data_from_soup import create_data_for_one_league
from final_dataframe_creation import create_one_df_per_season, create_one_df_per_league, MakeFinalDf

first_season_year_start = 9
last_season_year_start = 19
transfermarkt_links = dict()
final_df_instance = MakeFinalDf()

transfermarkt_links['polish_league'] = 'https://www.transfermarkt.pl/pko-ekstraklasa/transfers/wettbewerb/' \
    'PL1/plus/?saison_id=2009&s_w=&leihe=0&intern=0'
transfermarkt_links['germany_league'] = 'https://www.transfermarkt.pl/1-bundesliga/transfers/wettbewerb/' \
    'L1/plus/?saison_id=2009&s_w=&leihe=0&intern=0'
transfermarkt_links['ukrainian_league'] = 'https://www.transfermarkt.pl/premier-liha/transfers/wettbewerb/' \
    'UKR1/plus/?saison_id=2009&s_w=&leihe=0&intern=0'
transfermarkt_links['czech_league'] = 'https://www.transfermarkt.pl/fortuna-liga/transfers/wettbewerb/' \
    'TS1/plus/?saison_id=2009&s_w=&leihe=0&intern=0'
transfermarkt_links['slovakian_league'] = 'https://www.transfermarkt.pl/fortuna-liga/transfers/wettbewerb/' \
    'SLO1/plus/?saison_id=2009&s_w=&leihe=0&intern=0'
transfermarkt_links['romanian_league'] = 'https://www.transfermarkt.pl/liga-1/transfers/wettbewerb/' \
    'RO1/plus/?saison_id=2009&s_w=&leihe=0&intern=0'
transfermarkt_links['hungarian_league'] = 'https://www.transfermarkt.pl/nemzeti-bajnoksag/transfers/wettbewerb/' \
    'UNG1/plus/?saison_id=2009&s_w=&leihe=0&intern=0'
transfermarkt_links['austrian_league'] = 'https://www.transfermarkt.pl/bundesliga/transfers/wettbewerb/' \
    'A1/plus/?saison_id=2009&s_w=&leihe=0&intern=0'
transfermarkt_links['russian_league'] = 'https://www.transfermarkt.pl/premier-liga/transfers/wettbewerb/' \
    'RU1/plus/?saison_id=2009&s_w=&leihe=0&intern=0'

for league_name, league_link in transfermarkt_links.items():
    transfers_dict = create_empty_dataframe(first_season_year_start, last_season_year_start)
    transfers_dict = create_data_for_one_league(transfers_dict, league_link)
    transfers_newdict = create_one_df_per_season(transfers_dict)
    one_df__per_league = create_one_df_per_league(transfers_newdict)
    one_df__per_league.to_csv('Transfers_{}_from_2009_2010.csv'.format(league_name))
    
    final_df = final_df_instance.create_final_df(one_df__per_league, league_name)
    
final_df.to_csv('Transfers_all_leagues_from_2009_2010.csv'.format(league_name))
