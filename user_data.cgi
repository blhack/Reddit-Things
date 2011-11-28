#!/usr/bin/python

import thingist
import simplejson
import cgi
import urllib
import time
import google_charts

now = time.time()

form = cgi.FieldStorage()
user = form.getvalue("user","")
user = cgi.escape(user)

user = "dolljuliet"

comments = {}

def load_comments(json):
	for child in json['data']['children']:
		ups = child['data']['ups']
		downs = child['data']['downs']
		id = child['data']['id']
		earliest = child['data']['created_utc']
		comments[id] = {"ups":ups,"downs":downs,"date":earliest}
	if json['data'].has_key('after'):
		after = json['data']['after']
	else:
		after = ""
	return(after,earliest)

if len(user) > 0:
	req = urllib.urlopen("http://www.reddit.com/user/%s/comments/.json" % (user))
	json = simplejson.loads(req.read())
	after,earliest = load_comments(json)

	while len(comments) < 200 and len(comments) > 0:
		if len(after) == 0:
			break
		req = urllib.urlopen("http://www.reddit.com/user/%s/comments/.json?after=%s" % (user,after))
		print "http://www.reddit.com/user/%s/comments/.json?after=%s" % (user,after)
		try:
			json = simplejson.loads(req.read())
			after,earliest = load_comments(json)
			if len(json['data']['children']) < 25:
				break
		except:
			pass
	if len(comments) > 0:
		ups = 0
		downs = 0
		scores = []
		ages = []
		lowest = 1
		highest = 1
		for comment in comments:
			ups+= comments[comment]['ups']
			downs+= comments[comment]['downs']
			age = (now - comments[comment]['date']) / 86400
			score = comments[comment]['ups']-comments[comment]['downs']
			if score > highest and score != 0:
				highest = score
			if score < lowest and score != 0:
				lowest = score
			scores.append(score)
			ages.append(int(age))

		elapsed = now-int(earliest)
		days = elapsed/86400.0
		comments_per_day = len(comments)/days

	#print "Elapsed: %s - Comments per day: %s - Average points: %s"  % (elapsed,comments_per_day,(ups-downs)/len(comments))
	age_string = ""
	score_string = ""
	ages_data = google_charts.scale(ages)
	scores_data = google_charts.scale(scores)

	for age in ages_data['series']:
		age_string = "%s,%s" % (age_string,age)
	for score in scores_data['series']:
		score_string = "%s,%s" % (score_string,score)

	chd_string = "t:%s|%s&chxr=0,%s,%s|2,%s,%s" % (age_string[1::],score_string[1::],ages_data['lowest'],ages_data['highest'],scores_data['lowest'],scores_data['highest'])
	url = "https://chart.googleapis.com/chart?cht=s&chd=%s&chxt=x,x,y,y&chs=600x300&chxl=1:|age|3:|karma&chxp=1,50|3,50" % (chd_string)

	thingist.labs_init()

	print "<html>"
	print """
	<h1>Look at somebody else:</h1>
	<form action=/labs/user_average.cgi method=GET>
	<input type=text name=user>
	<input type=submit>
	</form>
	"""
	print "<h1>Some info for %s</h1>" % (user)
	print "(All data for the last %s days)" % (days)
	print "<h1>Comment performance</h1>"
	print "<br />"
	print "<img src=%s>" % (url)
	print "<h1>Comments Per Day: %s</h1>" % (comments_per_day)
	print "<h1>Total Comments: %s</h1>" % (len(comments))
	print "<h1>Total upvotes: %s" % (ups)
	print "<h1>Total downvotes: %s" % (downs)
	print "<h1>Average Score: %s" % ((ups-downs)/len(comments))
	print "</html>"

else:
	thingist.labs_init()

	print """
	<h1>What is your username?</h1>
	<form action=/labs/user_average.cgi method=GET>
	<input type=text name=user>
	<input type=submit>
	</form>
	"""
