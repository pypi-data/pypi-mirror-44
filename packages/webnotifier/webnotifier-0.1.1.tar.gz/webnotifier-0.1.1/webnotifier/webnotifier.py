from time import sleep
from random import randint
from requests import get
from lxml import html
from hashlib import md5
from lxml.html.clean import Cleaner

class WebNotifier:
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0']
    
    def __init__(self, urls, onNewChange, onError, interval = 3600):
        super().__init__()
        self.urls = urls
        self.onNewChange = onNewChange
        self.onError = onError
        self.interval = interval
        self.urls_data = {}
        self.html_cleaner = Cleaner(page_structure=False,style=True,inline_style=True,javascript=True,scripts=True)
        self.user_agent = self.user_agents[randint(0,len(self.user_agents)-1)]

    def _makeGETRequest(self,url):
        headers = {'User-Agent':self.user_agent}
        page = get(url,headers=headers)
        return page

    def _getURLHash(self,request_object):
        clean_content = self.html_cleaner.clean_html(request_object.content)
        content = html.fromstring(clean_content)
        body = content.xpath('/html/body')
        if(len(body)):
            body_text = body[0].text_content()
            web_hash = md5(body_text.encode()).hexdigest()
            return web_hash
        else:
            raise Exception('Body content not found')

    def _getURLETag(self,request_object):
        return request_object.headers['Etag']

    def _check_urls(self):
        """
        Checks if the hash has changed. It also makes the init process
        """
        for url in self.urls:
            try:
                get_request = self._makeGETRequest(url['href'])
                if url['href'] not in self.urls_data:
                    # Determine the type of checking new changes
                    self.urls_data[url['href']] = {}
                    response_headers = get_request.headers
                    if ('ETag' in response_headers) and (not response_headers['Etag'].startswith('W/')):
                        self.urls_data[url['href']]['type'] = 'etag'
                        self.urls_data[url['href']]['etag'] = self._getURLETag(get_request)
                    else:
                        self.urls_data[url['href']]['type'] = 'body'
                        self.urls_data[url['href']]['hash'] = self._getURLHash(get_request)
                else:
                    if self.urls_data[url['href']]['type'] == 'etag':
                        new_etag = self._getURLETag(get_request)
                        old_etag = self.urls_data[url['href']]['etag']
                        if(new_etag != old_etag):
                            self.urls_data[url['href']]['etag'] = new_etag
                            self.onNewChange(url['href'],url['name'])
                    elif self.urls_data[url['href']]['type'] == 'body':
                        new_hash = self._getURLHash(get_request)
                        old_hash = self.urls_data[url['href']]['hash']
                        if(new_hash != old_hash):
                            self.urls_data[url['href']]['hash'] = new_hash
                            self.onNewChange(url['href'],url['name'])
            except Exception as err:
                err.name = url['name']
                err.url = url['href']
                self.onError(err)

    def start(self):
        while(True):
            self._check_urls()
            sleep(self.interval)