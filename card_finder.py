def find_card(name):
    import json
    
    all_cards = json.load(open('clash-royale-constants.json', 'r'))
    
    all_card_stats = all_cards["cards_stats"]["building"] + all_cards["cards_stats"]["projectile"] + all_cards["cards_stats"]["spell"] + all_cards["cards_stats"]["troop"]
    chosen_card = None
    
    for card in all_cards["cards"]:
        if name == card["name"]:
            chosen_card = card
            break
        
    chosen_card_stats = None
    for card in all_card_stats:
        if name.replace(" ", "").replace(".","").title() == card["name"]:
            chosen_card_stats = card
            break
        
    stat_string = ''
    if not chosen_card is None:
        
        if chosen_card["type"] == 'Troop' or chosen_card["type"] == 'Spell':
            try:
                stat_string += name + ' does ' + str(chosen_card_stats["damage_per_level"][-6]) + ' damage at tournament standard\n'
            
            except TypeError:
                pass
        if chosen_card["type"] == 'Troop' or chosen_card["type"] == 'Building':
            try:
                stat_string += name + ' has ' + str(chosen_card_stats["hitpoints_per_level"][-6]) + ' hp at tournament standard\n'
            except TypeError:
                pass
    try:
        stat_string += 'More info at https://www.deckshop.pro/card/detail/' + chosen_card["key"]
    except TypeError:
        pass
        
    
    return chosen_card, stat_string