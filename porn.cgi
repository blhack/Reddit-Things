#!/usr/bin/python

import simplejson
import re
import urllib
import urlparse
import time

def fetch_json(url):
	req = urllib.urlopen(url)
	data = req.read()
	json = simplejson.loads(data)
	return(json)

def load_rage(json):
	name = ""
	for entry in json['data']['children']:
		url = entry['data']['url']
		domain = entry['data']['domain']
		name = entry['data']['name']
		title = entry['data']['title']
		comments = entry['data']['num_comments']
		if domain in ['i.imgur.com','imgur.com']:
			if urlparse.urlparse(url).path.split(".")[-1] in ['jpg','JPG','JPEG','jpeg','png','PNG']:
				pass
			else:
				url = url + ".png"

		if urlparse.urlparse(url).path.split(".")[-1] in ['jpg','JPG','JPEG','jpeg','png','PNG']:
			items[name] = {"name":name,"title":title,"url":url,"comments":comments}

		else:
			pass
			#print "(Debug) Not adding: %s" % (url)

	return(name)

if __name__ == "__main__":
	print "content-type:text/html\n"
	items = {}
	now = time.time()
	try:
		input = open("saved_porn.json","r")
		saved = input.read()
		items = simplejson.loads(saved)
		modified = items['modified']
	except:
		modified = 0

	age = now - modified

	if age > 60:
		print "Age was greater than 60..."
		print age
		items = {}
		json = fetch_json("http://www.reddit.com/r/earthporn+machineporn+humanporn+spaceporn+abandonedporn+adrenalineporn+archiporn.json")
		name = load_rage(json)
		url = "http://www.reddit.com/r/earthporn+machineporn+humanporn+spaceporn+abandonedporn+adrenalineporn+archiporn/.json?after=%s" % (name)
		while len(items) < 50:
			json = fetch_json(url)
			name = load_rage(json)
			url = "http://www.reddit.com/r/earthporn+machineporn+humanporn+spaceporn+abandonedporn+adrenalineporn+archiporn/.json?after=%s" % (name)

	print "<h1>Not Porn</h1><br />"
	for item in items:
		if item == "modified":
			continue
		item = items[item]
		name = item['name'].split("_")[-1]
		title = item['title']
		url = item['url']
		comments = item['comments']

		try:
			print "<h2>%s</h2><br />" % (title)
		except:
			print "Somethign else <br />"
		if not re.search("nsfw",title,flags=re.I):
			print "<img src=%s width=1180>" % (url)
		else:
			print "Link is NSFW: <a href='%s'>%s</a><br />" % (url,url)
		print "<br />"
		print "<a href='http://www.reddit.com/comments/%s/'>%s Comments</a>" % (name,comments)
		print "<br />"
	if age > 60:
		items['modified'] = time.time()
		output = simplejson.dumps(items)
		saved = open("saved_porn.json", "w")
		saved.write(output)
		saved.close()
	if age <= 60:
		print "This document is %s seconds old" % (age)
	print "<!-- There is no spoon, but there is a spork!  Welcome to KFC! -->"
	print """<!-- THIS SHIT IS BANANAS
	             L...
                     WiDDW
                    .W,,,tD
                    W,,,,,W
                    W,,,,,W
                   j;iit:.E.
                  .,ifii,;.D
                 .:;jf,i;;.,
                .i;i;t;ii:;:.
                itti;;;i;, .i
                jf;;it;...   .
                ff,.:....   ,
     WWEE       ;Li:...  ..: ;        DKK
    ,W . f       Lj:...:,it,.,      .Dj DKK
    Kt   ..      ff:,tfj.;i,        E     W
          ,K     ;j:,ti,...         W     W
    DL    W,     ,;:...,. .;,.     EW     E
    G    LEG     E.:::,;tti,;.      W   .W
     KKKLWW      E,i,;tttt:::      tWWK DK
       :  WW     E,fi,,,;;,:::    DWtiWKW
           KW    ft,Ki;,,;.:,    KW.
            WW   .D,,Wtt,:;tWtDKWW
             KWWWWW,,,,DLtj;WWDj.
                  W,,,,,,,,;W
                  E,,,,,,,;;W
                   W,,,,,,,;W
                   W,,,,,,;;W
                   Ej,,,,,,;K
                    W,,,,,,,E.
                    W,,,,,;;E.
                     W,,,,;;D.
                     W,,,,;;L,
                      W,,,;;Li
                      Wi,,;;jj
                       W,,;;tL
                      EWE;EWWD
                      W,WK: W;
                     jK     EW
                     WG      W
                    .W       WW
                    WW       .W
                GWWWWD.      .WKWWKt
              WW,    :KW    WK:    jWK
             W         W   .E        GL
             W       :WK    WG       ,K
             .WWWWWWWE       iWWWWWWWK
	-->
	"""
	print "</html>"
