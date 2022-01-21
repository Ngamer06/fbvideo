# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# Parse posts from Facebook and download file from post
#
# (C) 2022 Cherenkov Denis, Chelyabinsk, Russia
# -----------------------------------------------------------
import requests
from bs4 import BeautifulSoup
from configparser import ConfigParser
import logging

configParser = ConfigParser()
configParser.read('config.cfg')

PROXY_USER = configParser.get('proxy', 'user')
PROXY_PASS = configParser.get('proxy', 'password')
PROXY_HOST = configParser.get('proxy', 'host')
PROXY_PORT = configParser.get('proxy', 'port')

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 OPR/72.0.3815.320"
}

PROXY = {'https': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'}

LOGIN_URL = 'https://www.facebook.com/login'
EMAIL = 'ankhdenov@gmail.com'
PASSWORD = '7hMkFne4'

payload = {'email': EMAIL,
            'pass': PASSWORD}
with requests.Session() as session:
    post = session.post(LOGIN_URL, data=payload, headers = HEADERS, proxies = PROXY)

logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s \
                     [%(asctime)s]  %(message)s', level = logging.INFO)

def parse_video(link_post):
    '''The function parses the link to the video from the post and downloads this video'''
    page = session.get(link_post)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find('meta', property = 'og:description')['content']
    block = soup.find('div', class_ = 'bz')
    url = requests.utils.unquote(block.find('a')['href'])
    filename = title[:45].replace('\n', ' ').strip()
    with open(filename, "wb") as file:
        logging.info("Download started!")
        response = requests.get(url[21:])
        soup = BeautifulSoup(response.content, "html.parser")
        file.write(response.content)
        logging.info("Download success!")
        file.close


if __name__ == "__main__":
    logging.info("Parser started!")
    link_post = 'https://mbasic.facebook.com/groups/122547678361237/posts/995844574364872/?refsrc=deprecated&ref=104&_rdr'
    parse_video(link_post)
