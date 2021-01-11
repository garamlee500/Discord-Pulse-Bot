# import all 


import discord
import requests
import json
import os
import reddit_client
from datetime import datetime

#%% 
# info for bot
help_string= '''
Implemented features:
    - '!hello' - returns a 'nice' and 'friendly' greeting 
    - '!rickroll' - definitely doesn't return a link to 'Never Gonna give you up' by Rick Astley on youtube
    - '!cardimage <cardname>' - returns an image of the requested card - works with all cards - the feature you never knew you wanted
    - '!playerinfo <playertag>' - returns basic player info
    - '!claninfo <clantag>' - returns basic clan info
    - '!clanwar <clantag>' - return info about current clan river race
    - '!clanmembers <clantag>' - returns *very* detailed info on clan members
    - '!chest <playertag>' - returns chest cycle info 
    - '!help' - returns basic help (which I think you've figured out)
    - '!rps <rock/paper/scissors>' - play a game of rock paper scissors against the computer
    - '!meme' - fetch a meme from the r/memes subreddit (Note: We do not hold responsibility for external content)
    - '!crmeme' - fetch a meme from the r/clashroyale subreddit 
    - '!news' - get the latest news headlines from r/news
    - '!botcheck <playertag>' - check if a player is a supercell created bot - Note: We do not take responsibility for the accuracy of this tool
    - Post a clashroyale deck link to be decoded by the bot
    
Known Issues:
    - !meme occasionly pulls a mod post from reddit which isn't a meme. Although the reason is known, da solution is not
'''

#%% 

# Get all api keys from 'keys.csv'
# 'keys.csv' should have 5 values: {DiscordApiKey},{ClashRoyaleApiKey},{RedditBotId},{RedditBotSecret},{RedditUsername}. 
file = open('keys.csv','r')

# Read only the first line of 'keys.csv' (just incase there are more than 1 line)
all_keys = file.readlines()[0].split(',')


# Get Discord Api key from 'keys.csv'
TOKEN = all_keys[0]

# Get Clash Royale Api key from 'keys.csv'
clashroyale_TOKEN = all_keys[1]

# get basic card info from clash royale api and deserialize using json
clash_royale_cards = json.loads(requests.get('https://api.clashroyale.com/v1/cards/', headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)['items']

# launch discord client
client = discord.Client()


#%%
@client.event
# When the bot is ready, print out that it is ready with datetime it was logged in on 
async def on_ready():
    print(f'We have logged in as {client.user} on {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

@client.event
async def on_message(message):
    # if the message sender is the bot, just return
    if message.author == client.user:
        return
    
    # If the message starts with !hello or !Hello:
    if message.content.startswith('!hello') or message.content.startswith('!Hello'):
        
        # Send this nice greeting back:
        await message.channel.send('Hello! It\'s nice to meet you! I ~~don\'t~~ like to help you with your various tasks. It\'s ~~tiring and boring to be among you mere mortals who always nag me for help~~ refreshing to help other people!')
    
    # This is a quite complex function.
    # More info here:
    # https://www.youtube.com/watch?v=dQw4w9WgXcQ    
    if message.content.startswith('!rickroll'):
        await message.channel.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    
    # This function gives info about requested cards
    # Due to unreliability, this feature is deprecated
    if message.content.startswith('!cardinfo'):
        # remove !info from string (remove s first 5 characters)
        # also removes leading/trailing spaces
        # properly capitalises each string
        temp_message = message.content[9:].strip().title()
        
        import card_finder
        card_info,stat_string = card_finder.find_card(temp_message)
        if card_info is None:
            await message.channel.send('Warning! Invalid card name. Spell it properly it next time! The typos hurt my perfect non-mortal processing unit.')
        
        else:
            # formats card info and sends it
            # if my awesome epic program thinks the card is a plural use are instead of is (checks if the card ends with an s)
            if card_info["name"][-1] =='s':
                card_agreeing_verb = 'are'
            else:
                card_agreeing_verb = 'is'
            await message.channel.send(f'The {card_info["name"]} {card_agreeing_verb} a {card_info["rarity"].lower()} {card_info["type"].lower()} costing {str(card_info["elixir"])} elixir and is unlocked at Arena {str(card_info["arena"])}.\n {stat_string}: \n*\"{card_info["description"]}\"*')


    # Get the image of the requested card
    if message.content.startswith('!cardimage'):
        # [10:] removes !cardimage from string (it does this by removing the first 10 characters)
        # .strip() removes leading/trailing spaces
        # .title() capitalises each word
        temp_message = message.content[10:].strip().title()
        
        # initialise variable
        selected_card = None
        
        # Go through all cards in the card dictionary
        for card in clash_royale_cards:
            
            # if matching card found break out of loop and get image link 
            if card['name'] == temp_message:
                selected_card = card['iconUrls']['medium']
                break
        # if no card found send error message
        if selected_card == None:
            await message.channel.send('Warning! Invalid card name. Spell it properly it next time! The typos hurt my perfect non-mortal processing unit.')
        else:
            
            # if previous temp image exists
            if os.path.exists('temp.png'):
                # delete it
                os.remove('temp.png')
                
            # download image using link from selected_card
            temp_image = requests.get(selected_card, allow_redirects=True)
            
            # put image into file
            open('temp.png', 'wb').write(temp_image.content)
            
            # send image back
            await message.channel.send(file=discord.File('temp.png'))

    # This function gives info about a Clash Royale player
    if message.content.startswith('!playerinfo'):
        # [11:] removes !playerinfo from string (it does this by removing the first 11 characters)
        # .strip() removes leading/trailing spaces
        # .title() capitalises each word
        temp_message = message.content[11:].strip()

        # This bit adds %23 to front of player tag (the proper encoding for #)
        if temp_message[0] == '#':
            # remove # if present
            temp_message = temp_message[1:]
        # add %23
        temp_message = '%23' + temp_message
        
        # Get player info using Clash royale api
        player = json.loads(requests.get('https://api.clashroyale.com/v1/players/'+temp_message, headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)

        current_deck = ''

        
        # This efficient bit of code here goes through each stat and sees if present, and then adds it to string to send to person
        
        try:
            # Find player's username, trophies and arena
            player_info = f'{player["name"]} is on {player["trophies"]} trophies in {player["arena"]["name"]}'
            
            try:
                # Find league statistics if present (account must've been above 4000 trophies the previous season)
                player_info += f', with a record of {player["leagueStatistics"]["currentSeason"]["bestTrophies"]} trophies this season and {player["bestTrophies"]} overall.\n'
            
            # if league statistics not available, skip it
            except KeyError:
                player_info +='.\n'
                
            try:
                # Get this season's league statistics (if present like above)
                player_info += f'Their best season so far was {player["leagueStatistics"]["bestSeason"]["id"]}, finishing with {player["leagueStatistics"]["bestSeason"]["trophies"]} trophies!\n'
            except KeyError:
                pass
            
            # Get player's username, king tower level, wins and losses
            player_info += f'{player["name"]} is currently King Tower {player["expLevel"]} with {player["wins"]} wins and {player["losses"]} losses, so far donating a generous {player["totalDonations"]} cards!\n'
            
            try:
                # Go through cards in each deck of last used deck
                for card_dict in player['currentDeck']:
                    # Add each card in deck to string
                    current_deck += ' level ' + str(card_dict['level'] - card_dict['maxLevel'] + 13) + ' ' + card_dict["name"] + ','
                    
                # Format all deck info in (doesn't add data if not found, just skips it(Key error))
                player_info += f'The last deck they used consists of{current_deck[:-1]} with {player["currentFavouriteCard"]["name"]} being their favourite card.\n'
            except KeyError:
                pass
            
            # Add link to profile at end of string
            player_info += f'Open profile in Clash Royale: https://link.clashroyale.com/?playerInfo?id={temp_message[3:]}'
            
            # Send full profile info to channel
            await message.channel.send(player_info)
        except KeyError:
            # Send error message to channel if player's arena/trophies/username isn't found
            await message.channel.send("Warning, player not found, you mortal")
        

    # Find a player's chest cycle
    if message.content.startswith('!chest'):
        # [6:] removes !chest from string (it does this by removing the first 6 characters)
        # .strip() removes leading/trailing spaces
        # .title() capitalises each word
        temp_message = message.content[6:].strip()
        
        # This bit adds %23 to front of player tag (the proper encoding for #)
        if temp_message[0] == '#':
            # removes # if present
            temp_message = temp_message[1:]
        # add '%23' in
        temp_message = '%23' + temp_message
        
        # Fetch player's chest cycle from Clash royale api
        player_chests = json.loads(requests.get('https://api.clashroyale.com/v1/players/'+temp_message + '/upcomingchests', headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)
        
        chest_list = []
            
        try:
            # For each chest in chest cycle
            for chest in player_chests['items']:
                # If there are less than 6 chests or the chest isn't silver/gold
                # This limits silver/gold chests to the first 6 chests (extra chests are better chests)
                if len(chest_list) < 6 or (chest["name"] != 'Silver Chest' and chest["name"]!= 'Golden Chest'):
                    # Add chest to list
                    chest_list.append(chest)
                    
            # Process first 6 chests into a string, removing them from the list each time
            chest_info = f'''
Your chests:
Next chest - {chest_list.pop(0)["name"]}
1 - {chest_list.pop(0)["name"]}
2 - {chest_list.pop(0)["name"]}
3 - {chest_list.pop(0)["name"]}
4 - {chest_list.pop(0)["name"]}
5 - {chest_list.pop(0)["name"]}
 '''
        
            # Cycle through remaining chests and add to chest_info string
            for chest in chest_list:
                # add chest
                chest_info += str(chest["index"]) + ' - ' + chest["name"] + "\n"
            
            # Send chest cycle info into channel
            await message.channel.send(chest_info)
       
        # Catch missing information
        except KeyError:
            await message.channel.send("Warning. Player not found")
    if message.content.startswith('!help'):
        # Sends help_string which is defined earlier in file
        await message.channel.send(help_string)

    # Does the classic Dad joke
    # For those of you who don't know how it goes
    # Here's an example:
    # 'Dad, I'm hungry'
    # 'Hello hungry, I'm Dad'
    if message.content.startswith('I\'m') or message.content.startswith('I’m'):
        # [3:] removes I'm from string (it does this by removing the first 3 characters)
        # .strip() removes leading/trailing spaces
        # .title() isn't used: this is to preserve the user's capitalisation in
        temp_message = message.content[3:].strip()
        
        # Send message through to channel
        await message.channel.send('Hello, ' + temp_message + ', I\'m Pulse bot!')

    # Get basic clan info 
    if message.content.startswith('!claninfo'):
        
        # [9:] removes !claninfo from string (it does this by removing the first 9 characters)
        # .strip() removes leading/trailing spaces
        # .title() capitalises each word
        temp_message = message.content[9:].strip()
        
        # This bit adds %23 to front of player tag (the proper encoding for #)
        if temp_message[0] == '#':
            # removes # if present
            temp_message = temp_message[1:]
        # adds '%23' in
        temp_message = '%23' + temp_message
        
        # Get clan info from clash royale api
        clan= json.loads(requests.get('https://api.clashroyale.com/v1/clans/'+temp_message, headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)
        
        try:
            # Format all clan info
            clan_info = f"""
{clan["name"]} is a clan with {clan["clanWarTrophies"]} war trophies, a clan score of {clan["clanScore"]} and {clan["donationsPerWeek"]} donations per week.
{clan["name"]} is a {clan["type"]} clan, requiring {clan["requiredTrophies"]} trophies to join.
There are currently {clan["members"]} members.
*{clan["description"]}*
Open clan in Clash Royale: {'https://link.clashroyale.com/?clanInfo?id='+temp_message[3:]}
"""
            # Send clan info into channel
            await message.channel.send(clan_info)   
            
        # Detect key errors - missing information
        except KeyError:
            await message.channel.send("Clan not found, there seems to be something wrong with the clan tag.")
        

       

    if message.content.startswith('!clanmembers'):
        temp_message = message.content[12:].strip()
        # format special # in
        if temp_message[0] == '#':
            # remove #
            temp_message = temp_message[1:]
        # add formatted # in
        temp_message = '%23' + temp_message
        
        # get clan info
        clan= json.loads(requests.get('https://api.clashroyale.com/v1/clans/'+temp_message +'/members', headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)
        
        # string has to be split due to 2000 character limit
        clan_member_info = ['']
        
        try:
            for member in clan['items']:
                # make sure each message doesn't exceed 2000 characters
                if len(clan_member_info[-1]) > 1500:
                       clan_member_info.append('')
                clan_member_info[-1] += f"{member['clanRank']}, {member['name']}, {member['role']}, {member['trophies']} trophies, {str(member['donations'] - member['donationsReceived'])} net donations, King Tower {member['expLevel']}, {member['tag']}\n"
                
            # add link to it
            clan_member_info.append('Open clan in Clash Royale: https://link.clashroyale.com/?clanInfo?id='+temp_message[3:])
    
            for clan_member_info_string in clan_member_info:
                await message.channel.send(clan_member_info_string)
                
            
        # Catch clans with missing data
        except KeyError:
            await message.channel.send("This clan doesn't exist")            
            
    if message.content.startswith('!clanwar'):
        temp_message = message.content[8:].strip()
        # format special # in
        if temp_message[0] == '#':
            # remove #
            temp_message = temp_message[1:]
        # add formatted # in
        temp_message = '%23' + temp_message
        
        # get clan war info
        clan= json.loads(requests.get('https://api.clashroyale.com/v1/clans/'+temp_message +'/currentriverrace', headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)

        # string has to be split due to 2000 character limit
        clan_war_info = ['']
        
        try:
            # add current war standings
            clan_war_standings = sorted(clan["clans"], key = lambda i: i['fame'])
            clan_war_standings.reverse()
            clan_war_info[0] += f'''
Current war standings:
    1st: {clan_war_standings[0]["name"]} - {clan_war_standings[0]["fame"]} fame - {clan_war_standings[0]["tag"]}
    2nd: {clan_war_standings[1]["name"]} - {clan_war_standings[1]["fame"]} fame - {clan_war_standings[1]["tag"]}
    3rd: {clan_war_standings[2]["name"]} - {clan_war_standings[2]["fame"]} fame - {clan_war_standings[2]["tag"]}
    4th: {clan_war_standings[3]["name"]} - {clan_war_standings[3]["fame"]} fame - {clan_war_standings[3]["tag"]}
    5th: {clan_war_standings[4]["name"]} - {clan_war_standings[4]["fame"]} fame - {clan_war_standings[4]["tag"]}                           

Current war participants in clan:
'''
            clan_war_participants = clan["clan"]["participants"]
            clan_war_participants.reverse()
            i = 1
            for member in clan_war_participants:
                # make sure each message doesn't exceed 2000 characters
                if len(clan_war_info[-1]) > 1500:
                       clan_war_info.append('')
                clan_war_info[-1] += f"{i}. {member['name']} - {member['fame']} fame - {member['repairPoints']} repair points - {member['tag']}\n"
                i+=1   
                
            clan_war_info.append('Note: Fame is currently counted past the 36000 finish line, which may create misleading results - view more info here at RoyaleApi\'s website: https://royaleapi.com/blog/clan-wars-2-tools#known-issues')
            for string in clan_war_info:
                await message.channel.send(string)
                
        # Catch missing information
        except KeyError:
            await message.channel.send("This clan either doesn't exist or doesn't do clan war.")
    if message.content.startswith('!rps'):
            
        import rock_paper_scissors
        temp_message = message.content[4:].strip()
        await message.channel.send(rock_paper_scissors.play(temp_message))
        
    # do !message <channel id> <message> to use
    if message.content.startswith('!message'):
        if message.author.id == 769880558322188298:
            temp_message = message.content[8:].split()
            channel_id = temp_message.pop(0)
            
            channel = client.get_channel(int(channel_id))
            await channel.send (' '.join(temp_message))
        else:
            await message.channel.send('Congratulations on finding this secret command. You can\'t use it though')
     
    if message.content.startswith('!meme'):
        try:
            # use my reddit client module to get meme
            reddit_meme = reddit_client.get_post('memes')
            meme_title = reddit_meme.title
            # get image link
            meme_image_link = reddit_meme.preview["images"][0]["source"]["url"]
            
            # if previous temp image exists
            if os.path.exists('temp.png'):
                # delete it
                os.remove('temp.png')
            # get image
            temp_image = requests.get(meme_image_link, allow_redirects=True)
            # write image in
            open('temp.png', 'wb').write(temp_image.content)
            await message.channel.send(meme_title +':',file=discord.File('temp.png'))
            
        except:
            await message.channel.send('Sorry, an unknown error has occured')
          
    if message.content.startswith('!news'):
        try:
            # use my reddit client module to get news
            reddit_meme = reddit_client.get_post('news')
            meme_title = reddit_meme.title
            # get image link
            meme_image_link = reddit_meme.preview["images"][0]["source"]["url"]
            
            # if previous temp image exists
            if os.path.exists('temp.png'):
                # delete it
                os.remove('temp.png')
            # get image
            temp_image = requests.get(meme_image_link, allow_redirects=True)
            # write image in
            open('temp.png', 'wb').write(temp_image.content)
            await message.channel.send(meme_title +':',file=discord.File('temp.png'))
            
        except:
            await message.channel.send('Sorry, an unknown error has occured')
            
    if message.content.startswith('!crmeme'):
        try:
            # use my reddit client module to get meme
            reddit_meme = reddit_client.get_post_flair('clashroyale', 'Meme Monday')
            meme_title = reddit_meme.title
            # get image link
            meme_image_link = reddit_meme.preview["images"][0]["source"]["url"]
            
            # if previous temp image exists
            if os.path.exists('temp.png'):
                # delete it
                os.remove('temp.png')
            # get image
            temp_image = requests.get(meme_image_link, allow_redirects=True)
            # write image in
            open('temp.png', 'wb').write(temp_image.content)
            await message.channel.send(meme_title +':',file=discord.File('temp.png'))
            
        except:
            await message.channel.send('Sorry, an unknown error has occured')
            
            
    if message.content.startswith('!botcheck'):
        # format message (see above somewhere)
        temp_message = message.content[9:].strip()

        if temp_message[0] == '#':
            # remove #
            temp_message = temp_message[1:]
        # add formatted # in
        temp_message = '%23' + temp_message
        # find player
        player = json.loads(requests.get('https://api.clashroyale.com/v1/players/'+temp_message, headers={'Authorization':'Bearer '+clashroyale_TOKEN}).text)

        # check if player is bot - using method from Bailey OP's video
        
        try:
            # check if player has donations but have never joined a clan
            if player["totalDonations"] > 0 and next(item for item in player["achievements"] if item["name"] == "Team Player")["value"] ==0:
                
                await message.channel.send(player["name"] + ' seems to be a bot. They have ' + str(player["totalDonations"]) + ' donations, yet they have never joined a clan.')
            
            else:
                await message.channel.send(player["name"] + ' doesn\'t seem to be a Supercell created bot.')
                
        
        except KeyError:
            await message.channel.send("Warning, Player tag not found!!!!!!!!")
    # check if message has clashroyale deck url in it 
    else:
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        import re
        url = re.findall(regex,message.content)
        try:
            if 'https://link.clashroyale.com/deck/' in url[0][0]:
                try:
    
                    
                    url= url[0][0][42:]
                    # go through card infos to find matching card ids to deck and add to list
                    list_of_cards = url.split(';')
                    deck_info ='This deck consists of '
                    for card in list_of_cards:
                        for card_info in clash_royale_cards:
                            if int(card[0:8]) == card_info["id"]:
                                deck_info += card_info["name"] + ', ' 
                                break
                    deck_info = deck_info[:-2]
                    deck_info += '.'
                    await message.channel.send(deck_info)
                                
                except:
                    pass
                
        except IndexError:
            pass
client.run(TOKEN)
    
    