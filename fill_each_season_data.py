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

    club_counter = MakeCounter(2)
    player_nationality_counter = MakeCounter(0)
    player_nationality = soup.find_all(class_="zentriert nat-transfer-cell")
    club_nat = soup.find_all(class_="no-border-links verein-flagge-transfer-cell")
    club_country_counter = MakeCounter(0)

    for club_subtable_counter, _ in enumerate(transfers_dict_one_season):

        current_transfers_dict_copy = transfers_dict_one_season[club_subtable_counter][:]
        current_transfers_dict_copy = fill_empty_columns(current_transfers_dict_copy, club_subtable_counter, player_nationality_counter, player_nationality, club_nat, club_country_counter)

        club_counter = go_to_next_club(club_subtable_counter, club_counter)
        club_name = get_club_name(soup, club_counter)
        current_transfers_dict_copy = fill_dotyczy_klubu_column(current_transfers_dict_copy, club_name)
        current_transfers_dict_copy = corect_column_names(current_transfers_dict_copy, club_subtable_counter)
        transfers_dict_one_season[club_subtable_counter] = current_transfers_dict_copy
        player_nationality_counter()
    return transfers_dict_one_season
