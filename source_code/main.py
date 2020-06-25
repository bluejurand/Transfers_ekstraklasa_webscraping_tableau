from fill_each_season_data import create_empty_dataframe
from get_data_from_soup import create_data_for_one_league
from final_dataframe_creation import create_one_df_per_season, create_one_df_per_league, MakeFinalDf
import sys
sys.path.append("..")

def load_content_txt(file_name):
    with open(file_name, "r") as f:
        content = f.readlines()
    content_without_newlines = [x.strip() for x in content]
    return content_without_newlines

first_season_year_start = 9
last_season_year_start = 19
transfermarkt_links = dict()
final_df_instance = MakeFinalDf()

transfermarkt_links_txt = load_content_txt("../input_files/links_transfermarkt.txt")
league_names = load_content_txt("../input_files/league_names.txt")

for link_iterator, link in enumerate(transfermarkt_links_txt):
    transfermarkt_links[league_names[link_iterator]] = link

for league_name, league_link in transfermarkt_links.items():
    transfers_dict = create_empty_dataframe(first_season_year_start, last_season_year_start)
    transfers_dict = create_data_for_one_league(transfers_dict, league_link)
    transfers_newdict = create_one_df_per_season(transfers_dict)
    one_df__per_league = create_one_df_per_league(transfers_newdict)
    one_df__per_league.to_csv('../output_files/Transfers_{}_from_2009_2010.csv'.format(league_name))
    final_df = final_df_instance.create_final_df(one_df__per_league, league_name)

final_df.to_csv('../output_files/Transfers_all_leagues_from_2009_2010.csv'.format(league_name))
