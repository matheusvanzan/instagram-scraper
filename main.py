from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import urllib.request 
import os

from time import sleep

user = 'matheusvanzan'
# user = 'camoa.telecom'
# user = 'gizbranco.plataforma'

url = 'https://www.instagram.com/' + user
directory = 'data/' + user

if not os.path.exists(directory):
    os.makedirs(directory)


options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')
driver = '/usr/bin/chromedriver'

chrome = Chrome(
    chrome_options=options, 
    executable_path=driver
)


chrome.get(url)

print('Chrome running at ', chrome.current_url)


chrome.get_screenshot_as_file('screen.png')


selectors = {
    'nome': 'header h1',
    'foto_perfil': 'header img',
    'num_posts': 'header ul li:nth-child(1) span',
    'num_seguidores': 'header ul li:nth-child(2) span',
    'num_seguindo': 'header ul li:nth-child(3) span',
    
    'fotos': {
        'a': 'main article a',
        'img': 'main article a img'
    }
}

values = {}

with open('{}/data.csv'.format(directory), 'w+') as f:
    for key in selectors:
        if isinstance(selectors[key], str):
            value = chrome.find_element_by_css_selector(selectors[key])
            values.update({ key: value.text })
            f.write('"{}"; "{}"\n'.format(key, value.text))


# Scroll ate que todas as fotos estejam visiveis
urls = set()
srcs = set()
    
while int(values['num_posts']) > len(urls):
    chrome.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    print('Scroll down... ', end='')
    
    chrome.get_screenshot_as_file('scroll.png')
    
    urls_list = [a.get_attribute('href') for a in chrome.find_elements_by_css_selector( selectors['fotos']['a'] )]
    srcs_list = [img.get_attribute('src') for img in chrome.find_elements_by_css_selector( selectors['fotos']['img'] )]
    
    [urls.add(url) for url in urls_list]
    [srcs.add(src) for src in srcs_list]
    
    print('Found', len(urls), 'of', values['num_posts'])


# Descricao da foto
with open('{}/posts.csv'.format(directory), 'w+') as f:
    for i, url in enumerate(urls):
        lat, lng, desc = 0, 0, ''
        
        chrome.get(url)
        chrome.get_screenshot_as_file('post.png')
        
        desc_span = chrome.find_elements_by_css_selector('article ul li[role=menuitem] span')
        
        if len(desc_span) > 1:
            desc = desc_span[1].text.encode('utf-8').decode('latin-1') 
            # TODO: explain https://github.com/gevent/gevent/issues/614
            #       replace \n by space
        
        local = chrome.find_elements_by_css_selector('header a')
        if len(local) > 0:
            href = local[-1].get_attribute('href')
        
            if 'locations' in href:
                chrome.get(href)
                
                lat_metas = chrome.find_elements_by_css_selector('meta[property="place:location:latitude"]')
                if len(lat_metas) > 0:
                    lat = lat_metas[0].get_attribute('content')
                
                lng_metas = chrome.find_elements_by_css_selector('meta[property="place:location:longitude"]')
                if len(lng_metas) > 0:
                    lng = lng_metas[0].get_attribute('content')
        
        line = '"{}"; "{}"; "{}"; "{}"\n'.format(i, lat, lng, desc)
        print(line)
        f.write(line)
    

# Download das fotos
for i, src in enumerate(srcs):
    filename = '{}/{}.png'.format(directory, i)
    urllib.request.urlretrieve(src, filename)




chrome.quit()