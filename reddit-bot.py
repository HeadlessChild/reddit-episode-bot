import re
import praw
import time
import MySQLdb
import OpenSSL
import tvdb_api
import tvdb_exceptions

from configparser import ConfigParser

tvshow = "seinfeld"

t = tvdb_api.Tvdb()

r = praw.Reddit("browser-based:SeinfeldEpsisode Script:v1.0 (by /u/HeadlessChild)")

### LOGIN ###
config = ConfigParser()
config.read("login.txt")

username = config.get("Reddit", "Username")
password = config.get("Reddit", "Password")

r.login(username, password, disable_warning=True)
############

### DATABASE ###
db_username = config.get("MySQL", "Username")
db_password = config.get("MySQL", "Password")
db = MySQLdb.connect(host="localhost",
					 user=db_username,
					 passwd=db_password,
					 db="reddit_comments")
cur = db.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS comments(ID TEXT)')
db.commit()
############

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
	comments = subreddit.get_comments(limit=512)
	for comment in comments:
		comment_text = comment.body.lower()
		for p in patterns:
			m = re.search(p, comment_text)
			ID = comment.id
			cur.execute('SELECT * FROM comments WHERE ID=(%s)', [ID])
			result = cur.fetchone()
			if m and not result and str(comment.author) != str(username):
				try:
					try:
						episode_info = t[tvshow][int(m.group('s'))][int(m.group('ep'))]
						comment.reply('**Seinfeld: Season '+m.group('s')+' Episode '+m.group('ep')+'**'+\
									  '\n___\n'\
									  '\n\n**Episode Name:** '+episode_info['episodename']+\
									  '\n\n**Overview:** '+episode_info['overview']+\
									  '\n\n**Director:** '+episode_info['director']+\
									  '\n\n**Writer(s):** '+episode_info['writer']+\
									  '\n\n**First Aired:** '+episode_info['firstaired']+\
									  '\n\n**Rating:** '+episode_info['rating']+\
									  '\n___\n'\
									  '^| ^Hi! ^I\'m ^a ^bot ^for ^the ^subreddit [^/r/seinfeld](https://www.reddit.com/r/seinfeld) '\
									  '^| [^Help ^me ^improve!](https://github.com/HeadlessChild/reddit-episode-bot) '\
									  '^| [^Report ^a ^bug](https://github.com/HeadlessChild/reddit-episode-bot/issues) '\
									  '^| [^Author](https://www.reddit.com/user/HeadlessChild/) '\
									  '^| ^Data ^from ^[TheTVDB](http://thetvdb.com/) ^|')
						cur.execute('INSERT INTO comments (ID) VALUES (%s)', [ID])
						db.commit()
					except (tvdb_exceptions.tvdb_seasonnotfound, tvdb_exceptions.tvdb_episodenotfound, praw.errors.InvalidComment):
						pass
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
								  '\n\n**First Aired:** '+episode_info['firstaired']+\
								  '\n\n**Rating:** '+episode_info['rating']+\
								  '\n___\n'\
								  '^| ^Hi! ^I\'m ^a ^bot ^for ^the ^subreddit [^/r/seinfeld](https://www.reddit.com/r/seinfeld) '\
								  '^| [^Help ^me ^improve!](https://github.com/HeadlessChild/reddit-episode-bot) '\
								  '^| [^Report ^a ^bug](https://github.com/HeadlessChild/reddit-episode-bot/issues) '\
								  '^| [^Author](https://www.reddit.com/user/HeadlessChild/) '\
								  '^| ^Data ^from ^[TheTVDB](http://thetvdb.com/) ^|')
					cur.execute('INSERT INTO comments (ID) VALUES (%s)', [ID])
					db.commit()

while True:
	try:
		run_bot()
		time.sleep(25)
	except (praw.errors.HTTPException, OpenSSL.SSL.SysCallError):
		time.sleep(30)
