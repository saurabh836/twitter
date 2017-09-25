import tweepy  # https://github.com/tweepy/tweepy
import pprint, json, time
import mytwython
# Twitter API credentials


class Twi_Pos:
    consumer_key = "6THoh0ixs5BqEBHQfaKiwDK8x"
    consumer_secret = "SfFyDbTKG2ohjVSHdbmR9zMJL6Pj4wUpyRvTBEUZA5tL5duVPS"
    access_key = "713252801351131136-saQqIIzfImXd2ftTDIKYlrpraHG31VP"
    access_secret = "rlTNNf1thJVpy1wC6juv3ZM2fGYvha32kXQNtZ62ebqO8"
    lfd = mytwython.lis_findin_dict

    def uni(self, lis):
        new = []
        for n in lis:
            tem = {}
            print type(n)
            print n
            for i in n.iterkeys():
                temp = ['screen_name', 'profile_image_url', 'name']
                if i in temp:
                    k = ""
                    if i == 'screen_name':
                        i = 'profile_url'
                        tid = k
                        k = 'https://twitter.com/' + k
                        tem.update({'id': '@' + tid.encode("ascii")})
                    if i == 'profile_image_url':
                        k = k.replace("normal", "bigger")
                    tem.update({i.encode("ascii"): k.encode("ascii")})
            new.append(tem)
        return new

    def get_twitter(self, screen_name):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        api = tweepy.API(auth)
        a = api.search_users(screen_name)
        x = [j._json for j in a]
        return json.dumps(self.uni(x))

    def pos(self, src_key):
        lfd = mytwython.lis_findin_dict
        auth = tweepy.auth.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        api = tweepy.API(auth)
        # src_key += ' -filter:retweets AND -filter:replies'
        search_results = api.search(q=src_key, count=100)  # , until="2017-09-23 21:57:02")
        sr = []
        for k, i in enumerate(search_results):
            # if k < 1:
                jsn = json.loads((json.dumps(i._json)))
                sr.append(jsn)  # ['user']['screen_name'])
        return {'pos_json': sr, 'sname_cnt': len(lfd(sr, "screen_name"))}

# pprint.pprint()
# lfd = mytwython.lis_findin_dict
t = Twi_Pos()
a = t.pos("#python")
pprint.pprint(a['pos_json'][0])
# a1 = a[0]
# for a1 in a:
#     pprint.pprint(a1['created_at'] + "|" + a1['text'])

# pprint.pprint(len(lfd(a, "screen_name")))

