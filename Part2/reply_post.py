#! /usr/bin/python
import praw
import pdb
import re
import os
from config_bot import *

# Check that the file that contains our username exists
if not os.path.isfile("config_bot.py"):
    print "You must create a config file with your username and password."
    print "Please see config_skel.py"
    exit(1)

# Create the Reddit instance
user_agent = ("PyFor Eng bot 0.12345")
r = praw.Reddit(user_agent=user_agent)

# and login
r.login(REDDIT_USERNAME, REDDIT_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []

# If we have run the code before, load the list of comments we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = filter(None, comments_replied_to)

# Get the top 5 values from our subreddit
subreddit = r.get_subreddit('smu')
for submission in subreddit.get_hot(limit=5):
    #get comments into an unordered list
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    #Parse through comments to the current submission
    for comment in flat_comments:
        #If we did not already reply to the comment
        if comment.id not in comments_replied_to:
            #Make sure we aren't replying to ourself
            if str(comment.author) != str(REDDIT_USERNAME):
                #Check if the comment matches our regex
                if re.search("fuck tcu", comment.body, re.IGNORECASE):
                    #Yeah! We matched!
                    comment.reply('Yeah! Fuck TCU!')
                    comment.upvote()
                    #This comment has now been replied to
                    comments_replied_to.append(comment.id)
                    print "Bot replying to: ", comment.body

# Write our updated list back to the file
with open("comments_replied_to.txt", "w") as f:
    for comment_id in comments_replied_to:
        f.write(comment_id + "\n")
