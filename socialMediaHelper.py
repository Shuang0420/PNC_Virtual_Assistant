import tweepy

def get_api():
    # Fill in the values noted in previous step here
    cfg = {
        "consumer_key": 'W7pro6gR9GTbYw9rydtncb8xO',
        "consumer_secret": 'yjQOYylZ6mkKs76aiWwWSoeiH4BLFXT9CTE6oo7Oc9HhYXFMEp',
        "access_token": '4185617834-etKPJcnbj35lU4A8anpHseCrTLxZMqWvHMZ6SQB',
        "access_token_secret": '4kh178AzqsE4sbd8VvIznq0Nu1pskUAqRgMXHEPGO9RMX'
    }
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


# call this api to post tweet
def tweet(content):
    api = get_api()
    status = api.update_status(status=content)
    # Yes, tweet is called 'status' rather confusing


if __name__ == "__main__":
  tweet('Hello, Alexa bella')
