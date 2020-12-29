import praw

# get all keys from csv file
file = open('keys.csv','r')

all_keys = file.readlines()[0].split(',')


reddit = praw.Reddit(client_id=all_keys[2], # id of project
                     client_secret=all_keys[3], # secret
                     password= input('Password: \n'),
                     user_agent='PrawTut', # praw
                     username=all_keys[4])


visited_posts = []

try:
    file = open("visited_submissions.csv", 'r+')
    
except:
    file = open("visited_submissions.csv", 'w')

for line in file:
    # read file add all visited subs
    visited_posts += (line.split(","))
    
    
def get_post(subreddit):
    file = open("visited_submissions.csv", 'r+')

    new_posts = reddit.subreddit(subreddit).hot(limit=500) # get post
    for post in new_posts:
        
        # if post hasn't ben chosen yet use this post
        if not post.id in visited_posts:
            chosen_post = post
            visited_posts.append(post.id)
            break
    file.write(','.join(visited_posts))
    file.close()
    
    return chosen_post

def get_post_flair(subreddit, flair):
    file = open("visited_submissions.csv", 'r+')

    # Fetch top reddit posts in subbreddit of this week using praw
    new_posts = reddit.subreddit(subreddit).top('week', limit=5000)
    for post in new_posts:
        
        # if post hasn't ben chosen yet use this post and flair matches
        if not post.id in visited_posts and post.link_flair_text == flair:
            chosen_post = post
            visited_posts.append(post.id)
            break
    file.write(','.join(visited_posts))
    file.close()
    
    return chosen_post