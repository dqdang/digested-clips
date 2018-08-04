#!/usr/bin/python
import praw
import pdb
import re
import os


# Create the Reddit instance
reddit = praw.Reddit('bot1')

# and login
# reddit.login(USERNAME, PASSWORD)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

# Get the top 5 values from our subreddit
subreddit = reddit.subreddit('derek_bot')
for submission in subreddit.hot(limit=10):

    # If we haven't replied to this post before
    if submission.id not in posts_replied_to:
        # for comment in submission.comments.list():

        # Do a case insensitive search
        # here: [this is a link](https://reddit.com)
        # m = re.search("reddit.com[^\)]*", comment.body, re.IGNORECASE)
        m = re.search("(https?:\/\/(?:[a-z0-9-]+\.)*clips.twitch\.tv(?:\S*)?)", submission.url, re.IGNORECASE)
        n = re.search("(https?:\/\/(?:[a-z0-9-]+\.)*clips.twitch\.tv(?:\S*)?)", submission.selftext, re.IGNORECASE)
        if m or n:
            if m:
                index = comment.body.find(m.group(0))
            else:
                index = comment.body.find(n.group(0))
            # new_comment = comment.body[:index] + "old." + comment.body[index:]
            youtube_mirror = ""
            # Reply to the post
            comment.reply("Here you fucking go: " + youtube_mirror)
            # print("Bot replying to : ", comment.body)

            # Store the current id into our list
            posts_replied_to.append(submission.id)


# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
