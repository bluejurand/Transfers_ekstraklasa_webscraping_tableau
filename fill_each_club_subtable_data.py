def get_player_nationality(player_nationality_counter, player_nationality):
    player_counter = player_nationality_counter.get_current_val()
    current_player_nationality = player_nationality[player_counter].find('img').get('title')
    return current_player_nationality

def check_if_player_have_next_club(table_counter, current_transfers_dict_copy, club_nat, club_country_counter, club_subtable_counter):

    def check_transfer_type_club(club_subtable_counter):
        if club_subtable_counter % 2 == 0:
            club_header_type = 'Klub oddający'
        else:
            club_header_type = 'Klub pozyskujący'
        return club_header_type

    next_club_name = club_nat[club_country_counter].find('a').text
    club_header_type = check_transfer_type_club(club_subtable_counter)

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
