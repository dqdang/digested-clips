# digested-clips
Twitch clips are more unreliable than the printer at work

Host this on a local server. Get one from Google Cloud, AWS, DigitalOcean, etc.

## Instructions:

### Python:
1) Install Python from https://www.python.org/
2) Install pip if your installation didn't come with it from here: https://pip.pypa.io/en/stable/installing/
3) Install requirements:<br>
``$ pip install -r requirements.txt``

### Reddit:
1) Go to https://ssl.reddit.com/prefs/apps/
2) Make app, personal use.
3) pip install praw -> copy praw.ini from pip install location to this file's folder.
4) Fill in information in ``main.py``. Replace ``os.environ["VALUE"]`` with your string. [Lines 10, 11, 12, 13, 14]

### Twitch:
1) Make Twitch account with cid. Create application -> Enable 2-factor authentication.
2) Get authorization code:

    ``https://id.twitch.tv/oauth2/authorize?client_id=CID&redirect_uri=http://localhost&scope=clips:edit&response_type=code``

3) Get access token:

    a.<br>
    ``$ curl -X POST "https://id.twitch.tv/oauth2/token?client_id=CID&client_secret=SECRET&grant_type=client_credentials&scope=clips:edit"
$ {"access_token":"b8zb83g1y02eryihb4zrggjycac15s","expires_in":5616898,"scope":["clips:edit"],"token_type":"bearer"}``<br>
__OR__<br>
    b.<br>
    ``$ curl -X POST "https://id.twitch.tv/oauth2/token?client_id=CID&client_secret=SECRET&code=CODE&grant_type=authorization_code&redirect_uri=http://localhost&scope=clips:edit"
$ {"access_token":"w7ib0e0m3o04nvsdydcmhp2nohkntn","expires_in":13559,"refresh_token":"b7hzdbrk5xc7laaykgs62yov0ljcf13yz4v1bi21hr3p64qcu0","scope":["clips:edit"],"token_type":"bearer"}``

4) Fill in information in ``cliploader.py``. Replace ``os.environ`["VALUE"]`` with your string. [Lines 12, 13]

### Youtube:
1) Make a Google account and create an application here: https://console.developers.google.com/
2) Enable Youtube Data API, create credentials.
3) Create credentials for oauth2
   1) Copy template from https://github.com/googleapis/google-api-python-client/blob/master/docs/client-secrets.md to create a ``client_secrets.json`` file and paste in given information from oauth2.
   2) Put the ``client_secrets.json`` file in the same directory as this README.md file.

### Run:
- If all goes well, just run the main file:<br>
``$ python main.py``

### Notes:
1) On the initial upload, there will be a Google authentication page that will ask for your Youtube login information. Fill it in the first time and you will authenticate the bot for future uploads.
2) If you need to refresh your Twitch access token to download clips, follow the Twitch installation above with option __b.__ for step 3.
