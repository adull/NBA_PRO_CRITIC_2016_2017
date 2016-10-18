class TwitterAPI:
    def __init__(self):
        consumer_key = "cnR1gGNCK7r074goxvTLpgQTo"
        consumer_secret = "4fxMzotbskdjN042n79FOiEieLgDxRHGPprO8plTnPtdyA85DC"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = "701987958056886272-wp7KEjxHLPGvWtJMyaxrQF4IJ6EHdQL"
        access_token_secret = "kk09NukPpYjyPuhmPQWNpzrOTyxnKuHqng9Fqge6peI4H"
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)
