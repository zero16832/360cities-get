#!/usr/bin/env python

import os
from os import makedirs
from os.path import basename, exists, join
from urlparse import urlparse, urljoin
from urllib import urlopen, urlretrieve
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from Queue import Queue, Empty
from threading import Thread, active_count, current_thread


fetch_queue = Queue()

def fetch_worker():
	try:
		while True:
			url, filename = fetch_queue.get_nowait()
			urlretrieve(url, filename=filename)
			print 'got', filename, current_thread().ident
			fetch_queue.task_done()
	except Empty:
		return


def fetch(urls, pool_size=4):
	''' downloads the listed urls in parallel. '''

	for data in urls:
		fetch_queue.put_nowait(data)

	old_pool_size = active_count()
	for i in range(pool_size - old_pool_size):
		thread = Thread(target=fetch_worker)
		thread.start()

	fetch_queue.join()






def try_makedirs(path):
	if not exists(path):
		makedirs(path)


def get_info(url):
	''' returns the metadata url for this panorama '''

	page = BeautifulSoup(''.join(urlopen(url)))
	link = page.find('link', {'rel':'video_src'})
	query = urlparse(link['href']).query
	params = dict([p.split('=') for p in query.split('&')])
	return params['pano']



def tiles(url, target=None):
	''' yields pairs (url, filename) of tiles to download '''

	# one dir per pano
	if not target:
		target = basename(urlparse(url).path)
	try_makedirs(target)

	# save original url
	with open(join(target, 'original.url'), 'w') as f:
		print >>f, url

	# get info
	info_file = join(target, 'info.xml')
	if not exists(info_file):
		print 'Retrieving info...'
		info_url = urljoin(url, get_info(url))
		urlretrieve(info_url, filename=info_file)

	info = BeautifulStoneSoup(''.join(open(info_file)))
	image = info.find('krpano').find('image')
	tilesize = int(image['tilesize'])
	base_idx = int(image['baseindex'])

	# go through levels
	for level in image.findAll('level'):
		width = int(level['tiledimagewidth'])
		height = int(level['tiledimageheight'])
		row_count = width / tilesize
		col_count = height / tilesize

		tile_path = join(target, '%05dx%05d' % (width, height))
		try_makedirs(tile_path)

		# find tiles
		queue = []
		for side in ['left', 'right', 'front', 'back', 'up', 'down']:
			pat = level.find(side)['url']
			for row in range(base_idx, row_count + base_idx):
				for col in range(base_idx, col_count + base_idx):
					tile_name = join(tile_path, '%s-%d-%d.jpg' % (side, row, col))
					if not exists(tile_name):
						tile_url = pat.replace('%r', str(row)).replace('%c', str(col))
						yield tile_url, tile_name



if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1:
		# urls on command line
		for url in sys.argv[1:]:
			print 'Downloading', url
			fetch(tiles(url))
	
	else:
		print 'Reading whitespace seperated URLs from stdin'
		for line in sys.stdin:
			for url in line.split():
				print 'Downloading', url
				fetch(tiles(url))
