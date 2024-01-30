#!/usr/bin/env python

import os
from os import makedirs, remove
from os.path import basename, exists, join
from urlparse import urlparse, urljoin
from urllib import urlopen, urlretrieve
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from Queue import Queue, Empty
from threading import Thread, active_count, current_thread
from thread import interrupt_main

fetch_queue = Queue()

def fetch_worker():
	try:
		while True:
			try:
				url, filename = fetch_queue.get_nowait()
			except Empty:
				return
			try:
				urlretrieve(url, filename=filename)
				#print 'got', filename, current_thread().ident
			except:
				print 'Download of', url, 'failed'
			finally:
				fetch_queue.task_done()
	except KeyboardInterrupt:
		interrupt_main()


def fetch(urls, pool_size=4, **kwargs):
	''' downloads the listed urls in parallel. '''

	for data in urls:
		fetch_queue.put_nowait(data)

	old_pool_size = active_count()
	for i in range(pool_size - old_pool_size):
		thread = Thread(target=fetch_worker)
		thread.daemon = True
		thread.start()



def try_makedirs(path):
	if not exists(path):
		makedirs(path)


def get_info(url):
	''' returns the metadata url for this panorama '''

	
	try:
		source = list(urlopen(url))
		page = BeautifulSoup(''.join(source))
		if page.find('krpano'):
			return source
		link = page.find('link', {'rel':'video_src'})
		query = urlparse(link['href']).query
		params = dict([p.split('=') for p in query.split('&')])
		return params['pano']
	except:
		return None

class NotFound(Exception):
	pass


def filter_levels(levels, size):
	if not size:
		for x in levels:
			yield x
	elif size == 'largest':
		yield max(levels, key = lambda x: int(x['tiledimagewidth']))
	else:
		for x in levels:
			w = int(x['tiledimagewidth'])
			if w in size:
				yield x


def tiles(url, target=None, size=[], **kwargs):
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
		info = get_info(url)
		if not info:
			raise NotFound()
		elif type(info) == unicode:
			info_url = urljoin(url, info)
			if not info_url:
				raise NotFound()
			msg = urlopen(info_url)
			if msg.getcode() not in [200]:
				raise NotFound()
		else:
			msg = info
		with open(info_file, 'w') as f:
			for line in msg:
				print >>f, line,

	info = BeautifulStoneSoup(''.join(open(info_file)))
	pano = info.find('krpano')
	if not pano:
		remove(info_file)
		raise NotFound()
	image = info.find('krpano').find('image')
	image_type = image['type'].strip().lower()
	tilesize = int(image['tilesize'])
	try:
		base_idx = int(image['baseindex'])
	except:
		base_idx = 1

	# go through levels
	count = 0
	for level in filter_levels(image.findAll('level'), size):
		print repr(level)
		width = int(level['tiledimagewidth'])
		height = int(level['tiledimageheight'])
		row_count = width / tilesize
		col_count = height / tilesize

		tile_path = join(target, '%05dx%05d' % (width, height))
		try_makedirs(tile_path)

		# find tiles
		if image_type == 'sphere':
			pat = level.find('sphere')['url']
			for row in range(base_idx, row_count + base_idx):
				for col in range(base_idx, col_count + base_idx):
					tile_name = join(tile_path, '%d-%d.jpg' % (row, col))
					if not exists(tile_name):
						tile_url = pat.replace('%0v', '%02d' % row).replace('%0h', '%02d' % col)
						count += 1
						yield tile_url, tile_name
		elif image_type == 'cube':
			for side in ['left', 'right', 'front', 'back', 'up', 'down']:
				pat = level.find(side)['url']
				for row in range(base_idx, row_count + base_idx):
					for col in range(base_idx, col_count + base_idx):
						tile_name = join(tile_path, '%s-%d-%d.jpg' % (side, row, col))
						if not exists(tile_name):
							tile_url = pat.replace('%r', str(row)).replace('%c', str(col))
							count += 1
							yield tile_url, tile_name
		else:
			raise Exception, 'Unsupported image type %r' % image_type

	print count, 'tiles to download'


def fetch_all(urls, **kwargs):
	for url in urls:
		print 'Downloading', url
		try:
			fetch(tiles(url, **kwargs))
		except NotFound:
			print 'No panorama'
		except Exception, e:
			import traceback
			traceback.print_exc()
			print 'Error while trying to download', url


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(
		description='Download 360cities.net panorama tiles',
		fromfile_prefix_chars='@')
	parser.add_argument('-l', '--largest', default=False, action='store_true',
		help='Download only the largest version')
	parser.add_argument('-s', '--size', type=int, default=[], nargs='+', metavar='W',
		help='Download a set of specific widths')
	parser.add_argument('-t', '--threads', type=int, default=3,
		help='Number of parallel worker threads')
	parser.add_argument('url', default=[], nargs='*',
		help='The URL of a panorama page or its XML description')
	args = parser.parse_args()

	kwargs = {}

	if args.size and args.largest:
		parser.error(message='Specify either --largest OR --size')
	kwargs['size'] = 'largest' if args.largest else args.size

	if args.threads < 0 or args.threads > 20:
		parser.error()
	kwargs['pool_size'] = args.threads

	if args.url:
		# urls on command line
		fetch_all(args.url, **kwargs)
	
	else:
		print 'Reading whitespace seperated URLs from stdin'
		for line in sys.stdin:
			fetch_all(line.split(), **kwargs)

	import time, sys
	try:
		while not fetch_queue.empty():
			sys.stdout.write('\r%d to go     ' % fetch_queue.qsize())
			sys.stdout.flush()
			time.sleep(1)
	except KeyboardInterrupt:
		parser.exit()
