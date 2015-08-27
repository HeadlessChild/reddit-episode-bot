import re
import praw
import time
import tvdb_api
from configparser import ConfigParser

tvshow = "seinfeld"

t = tvdb_api.Tvdb()

r = praw.Reddit("browser-based:SeinfeldEpsisode Script:v1.0 (by /u/HeadlessChild)")

#Load comment id's
with open('comment-ids.txt') as f:
	cache = f.read().splitlines()

### LOGIN ###
config = ConfigParser()
config.read("login.txt")

username = config.get("Reddit", "Username")
password = config.get("Reddit", "Password")

r.login(username, password, disable_warning=True)

pattern1 = re.compile(r"""(?:s|season)(?:\s)(?P<s>\d+)(?:.*)(?:e|x|episode|\n)(?:\s)(?P<ep>\d+)""", re.VERBOSE)
pattern2 = re.compile(r"""(?:s|season)(?P<s>\d+)(?:e|x|episode|\n)(?:\s)(?P<ep>\d+)""", re.VERBOSE)
pattern3 = re.compile(r"""(?:s|season)(?:\s)(?P<s>\d+)(?:e|x|episode|\n)(?P<ep>\d+)""", re.VERBOSE)
pattern4 = re.compile(r"""(?:s|season)(?P<s>\d+)(?:e|x|episode|\n)(?P<ep>\d+)""", re.VERBOSE)
pattern5 = re.compile(r"""(?:s|season)(?P<s>\d+)(?:.*)(?:e|x|episode|\n)(?P<ep>\d+)""", re.VERBOSE)
pattern6 = re.compile(r"""(?:s|season)(?:\s)(?P<s>\d+)(?:.*)(?:e|x|episode|\n)(?P<ep>\d+)""", re.VERBOSE)
pattern7 = re.compile(r"""(?:s|season)(?P<s>\d+)(?:.*)(?:e|x|episode|\n)(?:\s)(?P<ep>\d+)""", re.VERBOSE)

patterns = [pattern1, pattern2, pattern3, pattern4, pattern5, pattern6, pattern7 ]

def run_bot():
	subreddit = r.get_subreddit("seinfeld")
	comments = subreddit.get_comments(limit=25)
	for comment in comments:
		comment_text = comment.body.lower()
		for p in patterns:
			m = re.search(p, comment_text)
			if m and comment.id not in cache and str(comment.author) != str(username):
				try:
					episode_info = t[tvshow][int(m.group('s'))][int(m.group('ep'))]
					comment.reply('**Seinfeld: Season '+m.group('s')+' Episode '+m.group('ep')+'**'+\
								  '\n___\n'\
								  '\n\n**Episode Name:** '+episode_info['episodename']+\
								  '\n\n**Overview:** '+episode_info['overview']+\
								  '\n\n**Director:** '+episode_info['director']+\
								  '\n\n**Writer(s):** '+episode_info['writer']+\
								  '\n\n**Rating:** '+episode_info['rating']+\
								  '\n___\n'\
								  '^| ^Hi! ^I\'m ^a ^bot ^for ^the ^subreddit [^/r/seinfeld](https://www.reddit.com/r/seinfeld) '\
								  '^| [^Help ^me ^improve!](https://github.com/HeadlessChild/reddit-episode-bot) '\
								  '^| [^Report ^a ^bug](https://github.com/HeadlessChild/reddit-episode-bot/issues) '\
								  '^| [^Author](https://www.reddit.com/user/HeadlessChild/) '\
								  '^| ^Data ^from ^[TheTVDB](http://thetvdb.com/) ')
					cache.append(comment.id)
					for i in cache:
						with open('comment-ids.txt', 'ab') as f:
							f.write(i+"\n")
				except praw.errors.RateLimitExceeded as error:
					print("Rate limit exceeded, must sleep for "
							"{} mins".format(float(error.sleep_time / 60)))
					time.sleep(error.sleep_time)
					episode_info = t[tvshow][int(m.group('s'))][int(m.group('ep'))]
					comment.reply('**Seinfeld: Season '+m.group('s')+' Episode '+m.group('ep')+'**'+\
								  '\n___\n'+\
								  '\n\n**Episode Name:** '+episode_info['episodename']+\
								  '\n\n**Overview:** '+episode_info['overview']+\
								  '\n\n**Director:** '+episode_info['director']+\
								  '\n\n**Writer(s):** '+episode_info['writer']+\
								  '\n\n**Rating:** '+episode_info['rating']+\
								  '\n___\n'\
								  '^| ^Hi! ^I\'m ^a ^bot ^for ^the ^subreddit [^/r/seinfeld](https://www.reddit.com/r/seinfeld) '\
								  '^| [^Help ^me ^improve!](https://github.com/HeadlessChild/reddit-episode-bot) '\
								  '^| [^Report ^a ^bug](https://github.com/HeadlessChild/reddit-episode-bot/issues) '\
								  '^| [^Author](https://www.reddit.com/user/HeadlessChild/) '\
								  '^| ^Data ^from ^[TheTVDB](http://thetvdb.com/) ')
					cache.append(comment.id)
					for i in cache:
						with open('comment-ids.txt', 'ab') as f:
							f.write(i+"\n")


while True:
	run_bot()
	time.sleep(25)
