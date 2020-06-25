import argparse
import cliploader
import os
import pdb
import praw
import re
import shutil
import uploader

# USERNAME = os.environ['USERNAME']
# PASSWORD = os.environ['PASSWORD']
# SUBREDDIT = os.environ['SUBREDDIT']
USERNAME = "digested-bot"
PASSWORD = "leagueoflegends"
SUBREDDIT = "derek_bot"

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='I really hate twitch clips')
    parser.add_argument(
        '-t', '--test', help='tests the application', action='store_true')

    args = parser.parse_args()
    write_to = "posts_replied_to.txt"

    # Create the Reddit instance
    reddit = praw.Reddit(client_id="r_PeCakRaugOjQ", client_secret="P7KMnFPyeUBWB3fM1MpNfKXXPTo", password=PASSWORD, user_agent="USERAGENT", username=USERNAME)

    # # and login
    # reddit.login(USERNAME, PASSWORD)

    # Have we run this code before? If not, create an empty list
    if not os.path.isfile(write_to):
        posts_replied_to = []
    elif args.test:
        posts_replied_to = []
        write_to = "posts_replied_to_TEMP.txt"
    # If we have run the code before, load the list of posts we have replied to
    else:
        # Read the file into a list and remove any empty values
        with open(write_to, "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

    # Get the top 5 values from our subreddit
    subreddit = reddit.subreddit(SUBREDDIT)
    for submission in subreddit.hot(limit=10):

        # If we haven't replied to this post before
        if submission.id not in posts_replied_to:
            # for comment in submission.comments.list():

            # Do a case insensitive search
            # here: [this is a link](https://reddit.com)
            # m = re.search("reddit.com[^\)]*", comment.body, re.IGNORECASE)
            m = re.search(
                "(https?:\/\/(?:[a-z0-9-]+\.)*clips.twitch\.tv(?:\S*)?)", submission.url, re.IGNORECASE)
            n = re.search(
                "(https?:\/\/(?:[a-z0-9-]+\.)*clips.twitch\.tv(?:\S*)?)", submission.selftext, re.IGNORECASE)
            if m or n:
                if m:
                    index = m.group(0)
                else:
                    index = n.group(0)
                print(index)
                clip = cliploader.dl_clip(index)
                print("\n")
                shutil.move("uploader.py-oauth2.json", "main.py-oauth2.json")
                youtube_mirror = uploader.upload(
                    {"title": clip[0], "file": clip[1]})
                # Reply to the post
                submit = False
                while(not submit):
                    try:
                        submission.reply("Here you go: " + youtube_mirror)
                        submit = True
                    except Exception:
                        continue

                # Store the current id into our list
                posts_replied_to.append(submission.id)
                os.remove(clip[1])

    # Write our updated list back to the file
    with open(write_to, "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")
