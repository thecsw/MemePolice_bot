import twitter
import config

api = twitter.Api(consumer_key = config.consumer_key,
                  consumer_secret = config.consumer_secret,
                  access_token_key = config.access_token_key,
                  access_token_secret = config.access_token_secret)

user = api.GetUser(screen_name='realDonaldTrump')
print(user.created_at)
