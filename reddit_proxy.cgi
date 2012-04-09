#!/usr/bin/python

import simplejson
import re
import urllib
import urlparse
import time
import urllib2

def fetch_json(url):
	#print "Imma fetchin' me some jsons!"
	user_agent = "gibson_ awesome image bot for ipad"
	headers = {"User-Agent":user_agent}
	values = {}
	req = urllib2.Request(url=url,headers=headers)
	response = urllib2.urlopen(req)
	data = response.read()
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
		if entry['data']['thumbnail'] == "nsfw":
			nsfw = 1
		else:
			nsfw = 0
		
		if urlparse.urlparse(url).path.split(".")[-1] in ['jpg','JPG','JPEG','jpeg','png','PNG']:
			pass

		elif re.search("flickr",urlparse.urlparse(url)[1]):
			try:
				flickr_id = urlparse.urlparse(url)[2].split("/")[3]
				api_key = 'SET THIS'
				flickr_url = "http://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key=%s&photo_id=%s&format=json&nojsoncallback=1" % (api_key,flickr_id)
				req = urllib.urlopen(flickr_url)
				data = req.read()
				flickr_json = simplejson.loads(data)
				url = flickr_json["sizes"]["size"][-1]["source"]
			except:
				pass

		elif re.search("imgur",url):
			url = url + ".png"

		if urlparse.urlparse(url).path.split(".")[-1] in ['jpg','JPG','JPEG','jpeg','png','PNG']:
			items[name] = {"name":name,"title":title,"url":url,"comments":comments,"nsfw":nsfw}

		else:
			pass

	return(name)

if __name__ == "__main__":
	print "content-type:application/json\n"
	items = {}
	now = time.time()
	try:
		input = open("saved_pics.json","r")
		saved = input.read()
		items = simplejson.loads(saved)
		modified = items['modified']
	except:
		modified = 0

	age = now - modified
	if age > 600:
		items = {}
		json = fetch_json("http://www.reddit.com/r/earthporn+architectureporn+abandonedporn+spaceporn.json")
		name = load_rage(json)
		url = "http://www.reddit.com/r/earthporn+architectureporn+abandonedporn+spaceporn/.json?after=%s" % (name)
		try:
			while len(items) < 50:
				json = fetch_json(url)
				name = load_rage(json)
				url = "http://www.reddit.com/r/earthporn+architectureporn+abandonedporn+spaceporn/.json?after=%s" % (name)
		except:
			pass
		json = fetch_json("http://www.reddit.com/r/pics.json")
		name = load_rage(json)
		url = "http://www.reddit.com/r/pics/.json?after=%s" % (name)
		try:
			while len(items) < 50:
				json = fetch_json(url)
				name = load_rage(json)
				url = "http://www.reddit.com/r/pics/.json?after=%s" % (name)
		except:
			pass


	for item in items:
		if item == "modified":
			continue
		item = items[item]
		name = item['name'].split("_")[-1]
		title = item['title']
		url = item['url']
		if item.has_key("nsfw"):
			nsfw = 1
		else:
			nsfw = 0
		comments = item['comments']

	if age > 600:
		items['modified'] = time.time()
		output = simplejson.dumps(items)
		saved = open("saved_pics.json", "w")
		saved.write(output)
		saved.close()

	del items["modified"]
	print simplejson.dumps(items)
