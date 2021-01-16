import pandas as pd
import json
import requests

# Clans to use for data
clan_tags = ['%23L2PGJUJ2', '%23YGP9GQVR','%2382CP0UVP', '%238YLJ8UL2', '%23L2JCP2V',
             '%2329C98ULY', '%232J2CJJJV','%239VQJ0YUJ', '%23989VGGV8', '%23L00UR290',
             '%23P8JLV8JL', '%23Y8GLLUQ', '%23P22VP929', '%239GGLPGL2', '%23P29QLPGP',
             '%23PPUV80QJ', '%239L99UYVR','%239GPQQC82', '%23P0YVURGY', '%239V89UQGL',
             '%2399LG89L8', '%239GV8G0GY','%2398R20QV2', '%2399GVGJJG', '%239JU8JYGQ',
             '%239GRJRCP2', '%239J9YUPGL','%23P2UP2RJV', '%23YGY2VUV8', '%23P0PU0GVP',
             '%23PJP8J9JG', '%239CVUPPVJ','%239R8YUL0J', '%239GU8PLG8', '%23P9CPCJ0P',
             '%239JJVQ2UJ', '%23PPV08U8R','%239UL8L282', '%23PUY0QL9P', '%239UGP2RU9',
             '%23PLRQCVGR', '%23PJGJQLLY']

# Generate data
def generate_data(clashroyale_TOKEN, write_to_file = False):
    # Dictionary of all data to be converted to pandas dataframe later
    battle_log_data_frame_dic = {'Results':[],
                                 'PlayerStartingTrophies':[],
                                 'OpponentStartingTrophies':[],
                                 'PlayerMaxTrophies':[],
                                 'OpponentMaxTrophies':[],
                                 'PlayerKingTowers':[],
                                 'OpponentKingTowers':[]}

    # Go through all clans in clan tags
    for clan in clan_tags:
        # Get clan info from clashroyale api
        clan_info = json.loads(requests.get('https://api.clashroyale.com/v1/clans/'+ clan +'/members', headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)
        
        # Go through each player's battle logs
        for player in clan_info["items"]:
            
            # Format # out of tag and add %23 (proper encoding)
            playertag = '%23' + player["tag"][1:]
            
            # Fetch player's battle log from clash royale api 
            battlelog = json.loads(requests.get('https://api.clashroyale.com/v1/players/'+playertag +'/battlelog', headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)
            
            # Go through each battl
            for battle in battlelog:
                # If battle was friendly and there was only one person on our team (1v1 check)
                if battle["type"] == 'friendly' and len(battle["team"]) ==1:
                    
                    # If both players had the same crowns - draw
                    if battle["team"][0]["crowns"] == battle["opponent"][0]["crowns"]:
                        
                        # add draw (0.5) to list of data
                        battle_log_data_frame_dic["Results"].append(0.5)
                        
                    # If player had more crowns - win
                    elif battle["team"][0]["crowns"] > battle["opponent"][0]["crowns"]:
                        
                        # add win (1) to list of data
                        battle_log_data_frame_dic["Results"].append(1)
                        
                    # If player had less crowns - loss
                    elif battle["team"][0]["crowns"] < battle["opponent"][0]["crowns"]:
                        
                        # add loss (0) to list of data
                        battle_log_data_frame_dic["Results"].append(0)
                        
                    # Add starting trophy data to dictionary
                    battle_log_data_frame_dic["PlayerStartingTrophies"].append(battle["team"][0]['startingTrophies'])
                    battle_log_data_frame_dic["OpponentStartingTrophies"].append(battle["opponent"][0]['startingTrophies'])
                    
                    # Get info from api about the players
                    current_player = json.loads(requests.get('https://api.clashroyale.com/v1/players/'+playertag, headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)
                    current_opponent = json.loads(requests.get('https://api.clashroyale.com/v1/players/%23'+battle["opponent"][0]["tag"][1:], headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)
                    
                    # Add info about player/opponent's max trophies
                    battle_log_data_frame_dic["PlayerMaxTrophies"].append(current_player['bestTrophies'])
                    battle_log_data_frame_dic["OpponentMaxTrophies"].append(current_opponent['bestTrophies'])
                            
                    # Add info about player/opponent's king tower(higher king tower indicates lower skill if trophies equal)
                    battle_log_data_frame_dic["PlayerKingTowers"].append(current_player['expLevel'])
                    battle_log_data_frame_dic["OpponentKingTowers"].append(current_opponent['expLevel'])
    
    # Write dataframe into file
    if write_to_file:
        # convert dic to dataframe
        data = pd.DataFrame.from_dict(battle_log_data_frame_dic)
        
        # convert dataframe to csv
        data = data.to_csv()
        
        # put csv data into battlelogs.csv
        f= open('battlelogs.csv', 'w')
        f.write(data)
        f.close()
        return
    else:
        # return data in dataframe
        return pd.DataFrame.from_dict(battle_log_data_frame_dic)

# Generate ai model for !matchup
def generate_ai_model(clashroyale_TOKEN):
    # find df with dataframe - if it doesn't exist generate it
    try: 
        df = pd.read_csv('battlelogs.csv', index_col=0)
    # if file not found
    except FileNotFoundError:
        # generate data
        df = generate_data(clashroyale_TOKEN)
        
    # pick all columns except for result as input
    X = df.loc[:,df.columns!='Results']
    # Selet Results for outputs
    y = df[['Results']] 
    
    # Our ai system to use
    from sklearn import svm

    # Train ai
    clf_svm = svm.SVC(random_state=0, probability=True) # starts ai thing
    clf_svm.fit(X, y)
    
    return clf_svm


