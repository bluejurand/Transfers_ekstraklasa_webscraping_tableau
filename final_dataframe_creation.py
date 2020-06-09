import pandas as pd

def create_one_df_per_season(transfers_dictionary):
    transfers_newdict = {}
    for _, transfers_name in enumerate(transfers_dictionary):
        transfers_newdict[transfers_name] = pd.concat(transfers_dictionary[transfers_name], sort=False)
    return transfers_newdict

def create_one_df_per_league(transfers_newdict):
    league_df = pd.DataFrame()
    for key, value in transfers_newdict.items():
        one_season_transfers_df = value
        current_season_years = '20{0}/20{1}'.format(key[-4:-2], key[-2:])
        one_season_transfers_df.loc[:, 'Sezon'] = current_season_years
        league_df = pd.concat([one_season_transfers_df, league_df], ignore_index=True, sort=False)
    return league_df

# def create_final_df(one_df__per_league, league_name):
#     final_df = pd.DataFrame()
#     one_df__per_league.loc[:, 'Liga'] = league_name
#     final_df = pd.concat([one_df__per_league, final_df], sort=False)
    
    
#     return final_df

class MakeFinalDf():
    def __init__(self):
        self.final_df = pd.DataFrame()

    def create_final_df(self, one_df__per_league, league_name):
        one_df__per_league.loc[:, 'Liga'] = league_name
        self.final_df = pd.concat([one_df__per_league, self.final_df], sort=False)
        return self.final_df