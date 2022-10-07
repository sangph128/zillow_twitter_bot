# zillow_twitter_bot
-This #twitter-bot is designed to scrape the first page of zillow search result and tweeting the new listing property in Austin, TX (you can change to your desire city/zip code). <br />
-You can find my example twitter bot <a href="https://twitter.com/Bot_RealtorATX" target="_blank">here</a> (This bot is terminated due to the risk of getting banned). <br />
-Please note that by using web scraping method, you may get blocked by zillow if you run this code too many times or too frequenly. You can find more about ways to avoid dectection on <a href="https://www.zenrows.com/blog/stealth-web-scraping-in-python-avoid-blocking-like-a-ninja#ip-rate-limit" target="_blank">here</a>. <br />

# Instuctions
-You can find the more detail instuctions for how to use tweepy, docker and hosting on AWS EC2 instance on <a href="https://realpython.com/twitter-bot-python-tweepy/#how-to-make-a-twitter-bot-in-python-with-tweepy" target="_blank">here</a>. <br />
-For better experience, you should activate venv before installing dependencies from requirements.txt:
```
$ python3 -m venv venv
$ source ./venv/Scripts/activate
$ pip3 install -r requirements.txt
```
-Run your code (uncomment line 117 when you ready to tweet):
```
$ python3 zillow_twitter_bot.py
```
## Contact me at sang.pham.8.12.96@gmail.com if you have any question. Have a great day!
