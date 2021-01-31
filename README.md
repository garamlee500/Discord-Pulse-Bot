# Discord-Pulse-Bot
A Clash Royale Discord bot
### Try it out on your server using: https://discord.com/api/oauth2/authorize?client_id=770293755285602354&permissions=392256&scope=bot
Note: The bot added using the above link will be running the [latest release](https://github.com/garamlee500/Discord-Pulse-Bot/releases/latest).

<img src="e.jpg" alt = "lord farquaad e meme" width = 20%>

# Features 
- A reddit post fetcher that can fetch memes, news headlines and clash royale memes (from [r/memes](https://www.reddit.com/r/memes/), [r/news](https://www.reddit.com/r/news/) and [r/clashroyale](https://www.reddit.com/r/clashroyale/))
- A clash royale data cruncher, accessing player profiles, clan wars and more!
- An auto clash royale bot checker, to see if that player you just played against was a bot!
- An auto clash royale deck link decoder, to see what decks your friends are uploading!
- A random rock paper scissors game for when you have no friends to play with!
- And more (sort of)! 

# Instructions for use
To run this from your own computer, you will need a [discord bot](https://discord.com/developers/applications/), [reddit bot](https://old.reddit.com/prefs/apps/), and a [clash royale api key](https://developer.clashroyale.com/#/) .
Download this repository and create a file called 'keys.csv' in the same folder. 'keys.csv' should have 5 values: {DiscordApiKey},{ClashRoyaleApiKey},{RedditBotId},{RedditBotSecret},{RedditUsername}. You must install discord.py, pandas, scikitlearn and praw using pip on your computer.

Now run main.py to run the bot. Enter you reddit password when prompted.

# Commands
### General:

- '!hello' - returns a 'nice' and 'friendly' greeting 
- '!help' - returns basic help
- '!info' - give basic info about current bot session
- '!meme' - fetch a meme from the r/memes subreddit (Note: We do not hold responsibility for external content)
- '!news' - get the latest news headlines from r/news
- '!rickroll' - definitely doesn't return a link to 'Never Gonna give you up' by Rick Astley on youtube
- '!rps <rock/paper/scissors>' - play a game of rock paper scissors against the computer
- '!sing' - Get the bot to sing a song

### Clash Royale:
- '!botcheck <playertag>' - check if a player is a supercell created bot - Note: We do not take responsibility for the accuracy of this tool
- '!cardimage <cardname>' - returns an image of the requested card - works with all cards - the feature you never knew you wanted
- '!chest <playertag>' - returns chest cycle info 
- '!claninfo <clantag>' - returns basic clan info
- '!clanmembers <clantag>' - returns *very* detailed info on clan members
- '!clanwar <clantag>' - return info about current clan river race
- '!crmeme' - fetch a meme from the r/clashroyale subreddit 
- '!matchup <player1 tag> <player2 tag>' - Predict friendly battle between two players
- '!playerinfo <playertag>' - returns basic player info

- Post a clashroyale deck link to decode it 