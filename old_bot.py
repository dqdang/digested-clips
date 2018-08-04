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
    # print(submission.title)

    # If we haven't replied to this post before
    if submission.id not in posts_replied_to:
        for comment in submission.comments.list():
            # Do a case insensitive search
            # here: [this is a link](https://reddit.com)
            m = re.search("reddit.com[^\)]*", comment.body, re.IGNORECASE)
            if m:
                index = comment.body.find(m.group(0))
                new_comment = comment.body[:index] + "old." + comment.body[index:]
                # Reply to the post
                comment.reply("Here you fucking go: " + new_comment)
                print("Bot replying to : ", comment.body)

                # Store the current id into our list
                posts_replied_to.append(submission.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
