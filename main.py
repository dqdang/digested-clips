import argparse
import cliploader
import os
import pdb
import praw
import re
import shlex
import shutil
import subprocess
import uploader

R_USERNAME = os.environ["USERNAME"]
R_PASSWORD = os.environ["PASSWORD"]
R_CID = os.environ["R_CID"]
R_SECRET = os.environ["R_SECRET"]
SUBREDDIT = os.environ["SUBREDDIT"]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='I really hate twitch clips')
    parser.add_argument(
        '-t', '--test', help='tests the application', action='store_true')

    args = parser.parse_args()
    write_to = "posts_replied_to.txt"

    # Create the Reddit instance
    reddit = praw.Reddit(client_id=R_CID, client_secret=R_SECRET,
                         password=R_PASSWORD, user_agent="USERAGENT", username=R_USERNAME)

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

    while True:
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
                    if os.path.exists("uploader.py-oauth2.json"):
                        shutil.move("uploader.py-oauth2.json",
                                    "main.py-oauth2.json")

                    cmd = shlex.split("python uploader.py --file {} -t {}".format(
                        clip[1], clip[0]))
                    out = subprocess.Popen(cmd,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)
                    stdout, stderr = out.communicate()
                    stdout = str(stdout)
                    print(stdout)
                    if "successfully uploaded" in stdout:
                        mir_index1 = stdout.find(
                            "https://www.youtube.com/watch?v=")
                        # 32 = https://www.youtube.com/watch?v= ---- 11 = id
                        mir_index2 = mir_index1 + 32 + 11
                        youtube_mirror = stdout[mir_index1:mir_index2]
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
