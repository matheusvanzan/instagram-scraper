from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from argparse import ArgumentParser
from time import sleep

from models import Profile, Post


# parse args
parser = ArgumentParser()
parser.add_argument('-u', '--username', dest='username', help='Profile username')
parser.add_argument('-d', '--debug', dest='debug', default=False, required=False, help='If True it shows debug output')
args = parser.parse_args()

# chrome config
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')
driver = '/usr/bin/chromedriver'

chrome = Chrome(
    chrome_options=options, 
    executable_path=driver
)

chrome.get('https://www.instagram.com/' + args.username)
if args.debug: print('Chrome running at ', chrome.current_url)

selectors = {
    'name': 'header h1',
    'num_posts': 'header ul li:nth-child(1) span',
    'num_followers': 'header ul li:nth-child(2) span',
    'num_following': 'header ul li:nth-child(3) span',
    
    'posts': 'main article a',
    'desc': 'article ul li[role=menuitem] span',
    'img': 'main article > div img',
    'local': 'header a',
    'lat': 'meta[property="place:location:latitude"]',
    'lng': 'meta[property="place:location:longitude"]',
}


# Create Profile instance and get info
profile = Profile(args.username)

name_el = chrome.find_element_by_css_selector(selectors['name'])
profile.name = name_el.text

num_posts_el = chrome.find_element_by_css_selector(selectors['num_posts'])
profile.num_posts = int(num_posts_el.text.replace(',', ''))

num_followers_el = chrome.find_element_by_css_selector(selectors['num_followers'])
profile.num_followers = int(num_followers_el.text.replace(',', '').replace('mil', '').replace('milhões', ''))

num_following_el = chrome.find_element_by_css_selector(selectors['num_following'])
profile.num_following = int(num_following_el.text.replace(',', ''))

if args.debug: print('Saved', profile)
profile.save()
    

# Scroll untill all pictures are visible
urls = set()
while len(urls) < profile.num_posts:
    
    if args.debug: print('Scroll down... ', end='')
    chrome.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    sleep(1)
    
    for a in chrome.find_elements_by_css_selector( selectors['posts'] ):
        urls.add(a.get_attribute('href'))
    
    if args.debug: print('found', len(urls), 'of', profile.num_posts)


for i, url in enumerate(urls):
    
    # Create new Post object
    post = Post(profile)
    post.id_ = i
    post.url = url
    
    # Navigate to post url
    chrome.get(url)
    chrome.get_screenshot_as_file('post.png')
    
    # get description (first comment)
    desc_el = chrome.find_elements_by_css_selector(selectors['desc'])
    if len(desc_el) > 1:
        post.desc = desc_el[0].text.replace('\n', '').encode('utf-8').decode('latin-1')
        # TODO: explain https://github.com/gevent/gevent/issues/614
        #       replace \n by space
        
    # get image
    img_el = chrome.find_element_by_css_selector(selectors['img'])
    post.download_img(img_el.get_attribute('src'))
    
    # get locations
    local_el = chrome.find_elements_by_css_selector(selectors['local'])
    if len(local_el) > 0:
        href = local_el[-1].get_attribute('href')
    
        if 'locations' in href:
            chrome.get(href)
            
            lat_metas = chrome.find_elements_by_css_selector(selectors['lat'])
            if len(lat_metas) > 0:
                lat = lat_metas[0].get_attribute('content')
            
            lng_metas = chrome.find_elements_by_css_selector(selectors['lng'])
            if len(lng_metas) > 0:
                lng = lng_metas[0].get_attribute('content')
    
    if args.debug: print('Saved', post)
    post.save()

chrome.quit()