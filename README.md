# Instagram Scraper

Download instagram profile info and posts with Selenium

## Install

1. google chrome

```bash
sudo apt-get install google-chrome-stable=80.0.3987.149-1
```

2. chromedriver

```bash
wget https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo cp chromedriver /usr/bin/  
sudo chown user:user /usr/bin/chromedriver 
```

3. virtualenv

```bash
virtualenv --python=/usr/bin/python3 env
source env/bin/activaate
pip install -r requirements.txt
```

### Usage

```bash
python main.py --username=profile_username_here --debug=True
```