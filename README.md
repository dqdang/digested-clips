# digested-clips
Reddit posts -> Twitch clips -> YouTube mirror

**NOTE: This project no longer works. Google's new guidelines as of 2021 have disabled public video uploading by bots:**<br>
https://support.google.com/youtube/answer/7300965?hl=en

Host this on a local server. Get one from Google Cloud, AWS, DigitalOcean, etc.

## Instructions:

### Python:
1) Install Python 3 from https://www.python.org/downloads/.
2) Install pip if your installation didn't come with it from here: https://pip.pypa.io/en/stable/installing/
3) Install requirements:<br>
``$ pip install -r requirements.txt``

### Reddit:
1) Go to https://ssl.reddit.com/prefs/apps/
2) Make app, personal use.
3) Copy praw.ini from pip install location to this file's folder. Use ``pip show praw`` to find the location.
4) Fill in information in ``main.py``. Replace ``os.environ["VALUE"]`` with your string; e.g ``R_USERNAME = "digested-clips"`` and ``SUBREDDIT = "valorant"`` [Lines 12, 13, 14, 15, 16]

### Twitch:
1) Make Twitch account with client ID. You can find your client ID here: https://dev.twitch.tv/docs/v5. Enable 2-factor authentication as well.
2) Get authorization code:

    ``https://id.twitch.tv/oauth2/authorize?client_id=CID&redirect_uri=http://localhost&scope=clips:edit&response_type=code``

3) Get access token:<br>

    ``$ curl -X POST "https://id.twitch.tv/oauth2/token?client_id=CID&client_secret=SECRET&code=CODE&grant_type=authorization_code&redirect_uri=http://localhost&scope=clips:edit"``<br>
    ``$ {"access_token":"TOKEN","expires_in":13559,"refresh_token":"R_TOK","scope":["clips:edit"],"token_type":"bearer"}``<br>

4) Fill in information in ``cliploader.py``. Replace ``os.environ`["VALUE"]`` with your string; e.g ``T_CID = "daj2kgh23nxlr0h83k6uifd9"`` [Lines 12, 13]

### Youtube:
1) Make a Google account and create an application here: https://console.developers.google.com/
2) Create client_secrets for Google's oauth2 security flow.
   1) Copy the web template from https://github.com/googleapis/google-api-python-client/blob/master/docs/client-secrets.md to create a ``client_secrets.json`` file and paste in given information from oauth2.
   2) Put the ``client_secrets.json`` file in the same directory as this README.md file.
3) **Click the dropdown button** on https://console.developers.google.com/ on the left of the page next to GoogleAPIs. There you can **create a new project**.
4) After creating the new project, make sure to **select** it in **the dropdown box** again and there should be a button that says "ENABLE APIs AND SERVICES". Click it and enter in the search box "youtube data". Select the one that says **YouTube Data API V3** and click **Enable**. Wait a bit for it to enable. This will allow your application to use the YouTube Data API.
5) Click **GoogleAPIs** to go back to the home application screen and click **Credentials**. Select **Create OAuth client ID**.
6) Google may ask you to set a product name. Just click the configure button and click "External" (Can't select "Internal" unless you're a G Suite user).  Give the bot a name and click save at the bottom. Click **Credentials ** and select **Create OAuth client ID** again.
7) Select **Web application** and choose a name (this can be anything).
8) Afterwards, a popup window will show the application's client ID and secret. Use these values in your ``client_secrets.json`` file.

### Run:
- If all goes well, just run the main file:<br>
``$ python main.py``

### Notes:
1) On the initial upload, there will be a Google authentication page that will ask for your Youtube login information. Fill it in the first time and you will authenticate the bot for future uploads.
2) If the bot needs to refresh the Twitch access token to download clips, follow the Twitch installation above with option __b__ for step 3. R_TOK will hold the refresh token.
   1) Make a POST request with the refresh token.<br>
   ``$ curl -X POST "https://id.twitch.tv/oauth2/token?client_id=CID&client_secret=SECRET&&refresh_token=R_TOK&grant_type=refresh_token"``
   2) You will need to replace the T_TOK in cliploader.py.
