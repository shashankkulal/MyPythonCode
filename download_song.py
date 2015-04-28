import urllib2
import urllib
import requests
import sys
import lxml.html
from clint.textui import progress
from random import randint
from BeautifulSoup import BeautifulSoup

movie_name=raw_input("Enter movie name: ")

def make_url(movie_name):
	url="http://www.songsmp3.com/1/bollywood-music/list-" + movie_name[0] + ".html"
	get_page(url)

def get_page(url):
	links = []
	movie = movie_name
	movie = movie.replace(" ", "-")
	connection = urllib.urlopen(url)
	dom =  lxml.html.fromstring(connection.read())
	for link in dom.xpath('//a/@href'):
		links.append(link)
	for link in links:
		if movie in link:
			fetch_songs(link)

def fetch_songs(link):
	songs = []
	text = urllib2.urlopen("http://www.songsmp3.com" + link).read();
	soup = BeautifulSoup(text);
	data = soup.findAll('object',attrs={'type':'application/x-shockwave-flash'})
	for div in data:
		links = div.findAll('param',attrs={'name':'FlashVars'})
		for a in links:
			songs.append(a['value'])
	i = 1
	for sname in songs:
		name1 = sname.split('/')
		name2 = name1[-1].split('.')
		print str(i) + " " + name2[0].capitalize()
		i = i + 1
	
	dn = raw_input("Enter song number to download : ")
	dn = int(dn)
	if dn > 0 and dn < i:
		j = dn - 1
		dn_song = songs[j]
		#download_url(dn_song)
		first = dn_song.split('&')
		second = first[0]
		final = second[4:]
		dn_url = "http://www.songsmp3.com" + final
		download_url(dn_url)
	else:
		print "Song not found. Enter number in range 1 to %i" % i
		sys.exit()
	
def download_url(file):
	print "File Size: " + file_size(file)
	user_input = raw_input("Do you want to download?(y/n)")
	if user_input == 'y':
		download_file(file)
	else:
		sys.exit()
	
	
def file_size(file):
	bytes = float(requests.head(file).headers.get('content-length', None))
	mb = bytes/1024/1024
	mb = float("{0:.2f}".format(mb))
	return str(mb) + " MB\n"
	
def download_file(file):
	r = requests.get(file, stream=True)
	filename = movie_name + str(randint(100,999999)) + '.mp3'
	with open(filename, 'wb') as f:
		total_length = int(r.headers.get('content-length'))
		for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
			if chunk:
				f.write(chunk)
				f.flush()
	print "Download Complete"
	
make_url(movie_name)
