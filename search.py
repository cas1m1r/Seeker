from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
import urllib.request
import random
import json
import time
import sys
import os
import re


def search_ddg(browser, search_term):
	root = 'https://duckduckgo.com'
	q = f'{root}/?t=ffab&q={search_term.replace(" ","+")}&ia=web'
	browser.get(q)
	random_sleep(3)
	print(f'[+] Searching Duck Duck Go for: {search_term}')
	# TODO: scroll to get more pages of results 
	random_sleep(3)
	urls = []
	new_finds = 1
	seeking = True
	dy = 0
	iteration = 1
	depth_limit = 33
	browser.set_window_size(800,900)
	while seeking and (new_finds>0 and iteration < depth_limit):
		try:
			N  = len(urls)
			for link in pull_links(browser.page_source, 'href="'):
				if link not in urls and link.find('http://')==0 and link.find('duckduckgo.com')<0:
					urls.append(link)
				elif link not in urls and link.find('https://')==0 and link.find('duckduckgo.com')<0:
					urls.append(link)
			new_finds = len(urls) - N
			print(f'\tFound {new_finds} more links')
			browser.execute_script(f'javascript:window.scrollBy(0,{800*iteration});')
			browser.find_element(By.ID, 'more-results').click()
			random_sleep(3)
			iteration += 1
		except KeyboardInterrupt:
			print('[!] Killing Search')
			seeking = False
			pass
		except urllib3.exceptions.NewConnectionError:
			seeking = False
			pass
		except urllib3.exceptions.MaxRetryError:
			seeking = False
			pass

	print(f'[X] Finished. {len(urls)} URLs found in total:')
	browser.close()
	return urls


def get_browser():
	options = Options()
	profile = FirefoxProfile()
	profile.set_preference("javascript.enabled", True)
	options.profile = profile 
	return Firefox(options)


def pull_links(html, delim):
	links = []
	for i in re.finditer(delim, html):
		ind = i.start()
		link = html[ind+len(delim):].split('"')[0]
		links.append(link)
	return links


def random_sleep(maxdt):
	delay = random.randint(1, maxdt)
	time.sleep(delay)
	return




def usage():
	print(f'Usage: python3 {sys.argv[0]} [search term]')
	exit(0)

def main():
	if len(sys.argv) < 2:
		usage()

	foxy = get_browser()
	search_term = ' '.join(sys.argv[1:])

	urls = search_ddg(foxy, search_term)
	fout = f'{search_term.replace(" ","_")}.json'
	with open(fout, 'w') as f:
		f.write(json.dumps(urls,indent=2))
	f.close()

if __name__ == '__main__':
	main()

