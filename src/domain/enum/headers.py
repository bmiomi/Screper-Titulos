from enum import Enum

class Headers(Enum):
    ACCEPT = 'Accept'
    ACCEPT_ENCODING = 'Accept-Encoding'
    ACCEPT_LANGUAGE = 'Accept-Language'
    CACHE_CONTROL = 'Cache-Control'
    CONNECTION = 'Connection'
    COOKIE = 'Cookie'
    HOST = 'Host'
    ORIGIN = 'Origin'
    REFERER = 'Referer'
    SEC_FETCH_DEST = 'Sec-Fetch-Dest'
    SEC_FETCH_MODE = 'Sec-Fetch-Mode'
    SEC_FETCH_SITE = 'Sec-Fetch-Site'
    USER_AGENT = 'User-Agent'

    @classmethod
    def get_headers(cls, cookies, url):
        return {
            cls.ACCEPT.value: 'image/avif,image/webp,*/*',
            cls.ACCEPT_ENCODING.value: 'gzip, deflate, br',
            cls.ACCEPT_LANGUAGE.value: 'es-ES,es;q=0.8',
            cls.CACHE_CONTROL.value: 'no-cache',
            cls.CONNECTION.value: 'keep-alive',
            cls.COOKIE.value: f"JSESSIONID={cookies.get('JSESSIONID')}",
            cls.HOST.value: 'www.senescyt.gob.ec',
            cls.ORIGIN.value: 'https://www.senescyt.gob.ec',
            cls.REFERER.value: url,
            cls.SEC_FETCH_DEST.value: 'image',
            cls.SEC_FETCH_MODE.value: 'no-cors',
            cls.SEC_FETCH_SITE.value: 'same-origin',
            cls.USER_AGENT.value: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        }