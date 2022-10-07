import tweepy
import requests
import re
import json
import time
import warnings
import pandas as pd

# Ignore warnings
warnings.filterwarnings('ignore')

# Credentials to access Twitter account
# Fill this in with your twitter developer account credentials
api_key = ""
api_key_secret = ""
access_token = ""
access_token_secret = ""

# Search result URL for new listing in Austin area
# Change this to the url that you want
url = 'https://www.zillow.com/homes/Austin,-TX_rb/'

# Add headers to bypass captchas
req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

# Second header in case the first one doesn't work
req_headers_alt = { 
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
	"Accept-Encoding": "gzip, deflate, br", 
	"Accept-Language": "en-US,en;q=0.5", 
	"Host": "httpbin.org", 
	"Sec-Fetch-Dest": "document", 
	"Sec-Fetch-Mode": "navigate", 
	"Sec-Fetch-Site": "none", 
	"Sec-Fetch-User": "?1", 
	"Upgrade-Insecure-Requests": "1", 
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0" 
}

# Geting new dataframe base on given url
def new_dataframe():
    # Scraping data
    with requests.Session() as s:
        r = s.get(url, headers=req_headers)
        data = json.loads(re.search(r'!--(\{"queryState".*?)-->', r.text).group(1))

    # Storing in pandas dataframe
    df = pd.DataFrame()
    for i in [data]:
        for item in i['cat1']['searchResults']['listResults']:
            df = df.append(item, ignore_index=True)

    # Filters
    df['zestimate'] = df['zestimate'].fillna("N/A")
    df['beds'] = df['beds'].fillna("N/A")
    df['baths'] = df['baths'].fillna("N/A")

    return df

# Compare new dataframe to old dataframe and return new listing properties
def new_listing(old_df, df):
    if old_df.empty:
        return df
    
    # Drop duplicate
    new_df = pd.concat([df,old_df]).drop_duplicates(subset = ['address'],keep=False)

    # Drop the bottom half which is also duplicate
    if not new_df.empty:
        new_df = new_df.drop(new_df.index[new_df.shape[0] // 2:])

    return new_df

# Formating data that looks good in a tweet
def format_tweet(row):
    # Formating zestimate number
    zes = row['zestimate']
    if zes != "N/A": zes = "${:,}".format(zes)

    # Formating bath number because zillow is weird
    baths = str(row['baths'])
    if baths == "0.0": baths = "N/A"

    # Actual Formating string
    tweet = row['price'] + "   -   " + "Zestimate: " + str(zes) + "\n"
    tweet += str(row['beds']) + " bed | " + baths + " bath | " 
    tweet += str(row['area']) + " sqft - " + row['statusText'] + "\n"
    tweet += row['address'] + "\n" +  row['detailUrl']

    return tweet

def main():
    # Initialize twitter bot api
    my_twitter_bot = MyTwiiterBot(api_key, api_key_secret, access_token, access_token_secret)

    # Verify Authentication
    # my_twitter_bot.auth_verify()

    # Store old dataframe to compare to new dataframe
    old_df = pd.DataFrame()
    while True:
        df = new_dataframe()
        new_df = new_listing(old_df, df)
        # If there new lising propety, 
        if not new_df.empty:
            for index, row in new_df.iterrows():
                # For testing purpose
                print(format_tweet(row))

                # Uncomment this line when you ready to tweet
                # my_twitter_bot.tweet(format_tweet(row))
            
            # Save the old dataframe
            old_df = df.copy()
        
        # 60s sleeping cycle
        time.sleep(60)

class MyTwiiterBot:
    # Authenticate to Twitter
    def __init__(self, api_key, api_key_secret, access_token, access_token_secret):
            auth = tweepy.OAuthHandler(api_key, api_key_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            self.api = api
    
    # Check Authentication
    def auth_verify(self):
        try:
            self.api.verify_credentials()
            print("Authentication PASSED")
        except:
            print("Authentication FAILED")

    # Tweeting
    def tweet(self, text):
            self.api.update_status(text)

if __name__ == "__main__":
    main()