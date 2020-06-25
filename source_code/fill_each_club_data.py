def go_to_next_club(club_subtable_counter, club_counter):
    if (club_subtable_counter % 2 == 0 and club_subtable_counter != 0):
        club_counter()
    return club_counter

def get_club_name(soup, club_counter):
    table_header = soup.find_all(class_="table-header")
    club_name = table_header[club_counter.get_current_val()].find_all('a')[1].text
    return club_name

def fill_dotyczy_klubu_column(current_transfers_dict_copy, club_name):
    club_transfers_number = len(current_transfers_dict_copy.columns)
    current_transfers_dict_copy.insert(club_transfers_number, 'Dotyczy klubu', club_name)
    return current_transfers_dict_copy

class MakeCounter():
    def __init__(self, start_value):
        self._val = start_value

    def __call__(self):
        self._val += 1
        return self._val

    def get_current_val(self):
        return self._val

def fill_empty_columns(current_transfers_dict_copy, club_subtable_counter, player_nationality_counter, player_nationality, club_nat, club_country_counter):
    from fill_each_club_subtable_data import (get_player_nationality, check_transfer_type,
                                              check_if_player_have_next_club)
    
    def get_current_player_nationality(current_transfers_dict_copy, table_counter):
        current_player_nationality = current_transfers_dict_copy.loc[table_counter, "Narodowość"]
        return current_player_nationality

    for table_counter, _ in current_transfers_dict_copy.iterrows():
        current_player_nationality = get_current_player_nationality(current_transfers_dict_copy, table_counter) 
        if not current_player_nationality in ['Bez nabytków', 'Bez odejść']:
            current_transfers_dict_copy = check_if_player_have_next_club(table_counter, current_transfers_dict_copy, club_nat, club_country_counter, club_subtable_counter)
            club_country_counter()
            player_nationality_counter()
        if not current_player_nationality in ['b.i.', 'Bez nabytków', 'b.i.b.i.', 'Bez odejść']:
            current_transfers_dict_copy.loc[table_counter, "Narodowość"] = get_player_nationality(player_nationality_counter, player_nationality)
        current_transfers_dict_copy.loc[table_counter, "Rodzaj transferu"] = check_transfer_type(club_subtable_counter)

    return current_transfers_dict_copy

def corect_column_names(current_transfers_dict_copy, club_subtable_counter):
    if club_subtable_counter % 2 == 0:
        club_in_out = 'oddający'
        footballer = 'Nabytki'
    else:
        club_in_out = 'pozyskujący'
        footballer = 'Odejścia'

    new_club_country_name = 'Klub pozyskujący/oddający państwo'
    new_club_name = 'Klub pozyskujący/oddający nazwa'
    change_club_columns = {'Klub {}'.format(club_in_out): new_club_country_name, 'Klub {}.1'.format(club_in_out): new_club_name}
    current_transfers_dict_copy = current_transfers_dict_copy.rename(columns=change_club_columns)
    change_footballer_columns = {'{}'.format(footballer): 'Piłkarz', '{}'.format(footballer): 'Piłkarz'}
    current_transfers_dict_copy = current_transfers_dict_copy.rename(columns=change_footballer_columns)
    return current_transfers_dict_copy
