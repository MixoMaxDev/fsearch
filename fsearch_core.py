"""
fsearch_core.py
This file contains the core functions for the fsearch API.
All functions are imported into main.py.
The search providers are defined in this file.
"""

import requests
import bs4
import random

class SearchResult:
    title: str
    url: str
    description: str
    image_url: str
    provider: str
    provider_url: str
    is_nsfw: bool = False
    
    def __init__(self, title, url, description, image_url, provider, provider_url, is_nsfw = False):
        self.title = title
        self.url = url
        self.description = description
        self.image_url = image_url
        self.provider = provider
        self.provider_url = provider_url
        self.is_nsfw = is_nsfw
    
    def to_json(self):
        data = {
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "image_url": self.image_url,
            "provider": self.provider,
            "provider_url": self.provider_url,
            "is_nsfw": self.is_nsfw
        }
        return data


def calculate_filesize(size_in_B: int) -> str:
    """
    Convert a size in bytes to a human-readable string.
    """
    
    if size_in_B < 1024:
        return f"{size_in_B} B"
    elif size_in_B < 1024**2:
        return f"{round(size_in_B/1024, 2)} KB"
    elif size_in_B < 1024**3:
        return f"{round(size_in_B/1024**2, 2)} MB"
    elif size_in_B < 1024**4:
        return f"{round(size_in_B/1024**3, 2)} GB"
    elif size_in_B < 1024**5:
        return f"{round(size_in_B/1024**4, 2)} TB"
    else:
        return f"{round(size_in_B/1024**5, 2)} PB"



def get_random_header():
    headers = [
        { #make a somewhat realistic user agent
            "Connection": "keep-alive", #means: keep the connection open
            "Cache-Control": "max-age=0", #means: don't cache
            "sec-ch-ua": f'"Chromium";v="{random.randint(90, 95)}", "Google Chrome";v="{random.randint(90, 95)}", ";Not A Brand";v="99"', #means: I'm using Chrome 94
            "sec-ch-ua-mobile": "?0", #means: I'm not using a mobile device
            "sec-ch-ua-platform": f'"{random.choice(["macOS", "Windows", "Linux", "iPhone", "iPad", "Android"])}"', #means: I'm using macOS
            "Upgrade-Insecure-Requests": "1", #means: I want to be redirected to https if possible
            "User-Agent": f"Mozilla/5.0 ({random.choice(['Macintosh', 'Windows', 'Linux', 'iPhone', 'iPad', 'Android'])}; Intel Mac OS X 10_{random.randint(10, 15)}_{random.randint(1, 9)}) AppleWebKit/{random.randint(500, 599)}.36 (KHTML, like Gecko)", #means: I'm using macOS and Chrome 94
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8", #means: I accept all kinds of files
            "Sec-Fetch-Site": "none", #means: I'm not on a different site
            "Sec-Fetch-Mode": "navigate", #means: I'm navigating to a different site
            "Sec-Fetch-User": "?1", #means: I'm not using a mobile device
            "Sec-Fetch-Dest": "document", #means: I'm navigating to a document
            "Accept-Encoding": "gzip, deflate, br", #means: I accept all kinds of encodings
            "Accept-Language": "en-US, ar, zh-CN, fr, de, it, ja, ko, ru, es", #means: I accept all kinds of languages
        },
        {#make a firefox/windows user agent
            "Connection": "keep-alive", #means: keep the connection open
            "Cache-Control": "max-age=0", #means: don't cache
            "sec-ch-ua": f'"Mozilla";v="{random.randint(80, 89)}.0", "Firefox";v="{random.randint(80, 89)}.0"', #means: I'm using Firefox
            "sec-ch-ua-mobile": "?0", #means: I'm not using a mobile device
            "sec-ch-ua-platform": f'"{random.choice(["Windows", "Linux", "Macintosh"])}"', #means: I'm using Windows
            "Upgrade-Insecure-Requests": "1", #means: I want to be redirected to https if possible
            "User-Agent": f"Mozilla/5.0 ({random.choice(['Windows NT 10.0; Win64; x64', 'Windows NT 10.0; Win64; x64; rv:89.0', 'Windows NT 6.1; Win64; x64', 'Windows NT 6.1; Win64; x64; rv:89.0', 'Windows NT 6.3; Win64; x64', 'Windows NT 6.3; Win64; x64; rv:89.0'])}) Gecko/20100101 Firefox/{random.randint(80, 89)}.0", #means: I'm using Windows and Firefox
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", #means: I accept all kinds of files
            "Sec-Fetch-Site": "none", #means: I'm not on a different site
            "Sec-Fetch-Mode": "navigate", #means: I'm navigating to a different site
            "Sec-Fetch-User": "?1", #means: I'm not using a mobile device
            "Sec-Fetch-Dest": "document", #means: I'm navigating to a document
            "Accept-Encoding": "gzip, deflate, br", #means: I accept all kinds of encodings
            "Accept-Language": "en-US, ar, zh-CN, fr, de, it, ja, ko, ru, es", #means: I accept all kinds of languages
        },
        {#make a edge/windows user agent
            "Connection": "keep-alive", #means: keep the connection open
            "Cache-Control": "max-age=0", #means: don't cache
            "sec-ch-ua": f'"Microsoft Edge";v="{random.randint(80, 89)}", "Edg";v="{random.randint(80, 89)}"', #means: I'm using Edge
            "sec-ch-ua-mobile": "?0", #means: I'm not using a mobile device
            "sec-ch-ua-platform": f'"{random.choice(["Windows", "Linux", "Macintosh"])}"', #means: I'm using Windows
            "Upgrade-Insecure-Requests": "1", #means: I want to be redirected to https if possible
            "User-Agent": f"Mozilla/5.0 ({random.choice(['Windows NT 10.0; Win64; x64', 'Windows NT 10.0; Win64; x64; rv:89.0', 'Windows NT 6.1; Win64; x64', 'Windows NT 6.1; Win64; x64; rv:89.0', 'Windows NT 6.3; Win64; x64', 'Windows NT 6.3; Win64; x64; rv:89.0'])}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 95)}.0.0.0 Safari/537.36 Edg/{random.randint(80, 89)}.0.{random.randint(1000, 9999)}.0", #means: I'm using Windows and Edge
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", #means: I accept all kinds of files
            "Sec-Fetch-Site": "none", #means: I'm not on a different site
            "Sec-Fetch-Mode": "navigate", #means: I'm navigating to a different site
            "Sec-Fetch-User": "?1", #means: I'm not using a mobile device
            "Sec-Fetch-Dest": "document", #means: I'm navigating to a document
            "Accept-Encoding": "gzip, deflate, br", #means: I accept all kinds of encodings
            "Accept-Language": "en-US, ar, zh-CN, fr, de, it, ja, ko, ru, es", #means: I accept all kinds of languages
        },
        {#make a chromium/Ubuntu user agent
            "Connection": "keep-alive", #means: keep the connection open
            "Cache-Control": "max-age=0", #means: don't cache
            "sec-ch-ua": f'"Chromium";v="{random.randint(90, 95)}", "Google Chrome";v="{random.randint(90, 95)}", ";Not A Brand";v="99"', #means: I'm using Chrome 94
            "sec-ch-ua-mobile": "?0", #means: I'm not using a mobile device
            "sec-ch-ua-platform": f'"{random.choice(["Ubuntu", "Linux", "Macintosh"])}"', #means: I'm using Ubuntu
            "Upgrade-Insecure-Requests": "1", #means: I want to be redirected to https if possible
            "User-Agent": f"Mozilla/5.0 ({random.choice(['X11; Ubuntu Linux x86_64', 'X11; Linux x86_64', 'Macintosh; Intel Mac OS X 10_15_7'])}) AppleWebKit/{random.randint(500, 599)}.36 (KHTML, like Gecko) Chrome/{random.randint(90, 95)}.0.0.0 Safari/{random.randint(500, 599)}.36", #means: I'm using Ubuntu and Chrome
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", #means: I accept all kinds of files
            "Sec-Fetch-Site": "none", #means: I'm not on a different site
            "Sec-Fetch-Mode": "navigate", #means: I'm navigating to a different site
            "Sec-Fetch-User": "?1", #means: I'm not using a mobile device
            "Sec-Fetch-Dest": "document", #means: I'm navigating to a document
            "Accept-Encoding": "gzip, deflate, br", #means: I accept all kinds of encodings
            "Accept-Language": "en-US, ar, zh-CN, fr, de, it, ja, ko, ru, es", #means: I accept all kinds of languages
        },
        {#make a chromebook user agent
            "Connection": "keep-alive", #means: keep the connection open
            "Cache-Control": "max-age=0", #means: don't cache
            "sec-ch-ua": f'"Chromium";v="{random.randint(90, 95)}", "Google Chrome";v="{random.randint(90, 95)}", ";Not A Brand";v="99"', #means: I'm using Chrome 94
            "sec-ch-ua-mobile": "?1", #means: I'm using a mobile device
            "sec-ch-ua-platform": f'"CrOS";v="{random.randint(10000, 99999)}.{random.randint(0, 9)}.{random.randint(0, 9999)}.{random.randint(0, 999)}"', #means: I'm using a Chromebook
            "Upgrade-Insecure-Requests": "1", #means: I want to be redirected to https if possible
            "User-Agent": f"Mozilla/5.0 ({random.choice(['X11; CrOS x86_64', 'X11; CrOS armv7l', 'X11; CrOS aarch64'])}) AppleWebKit/{random.randint(500, 599)}.36 (KHTML, like Gecko) Chrome/{random.randint(90, 95)}.0.0.0 Safari/{random.randint(500, 599)}.36", #means: I'm using a Chromebook and Chrome
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", #means: I accept all kinds of files
            "Sec-Fetch-Site": "none", #means: I'm not on a different site
            "Sec-Fetch-Mode": "navigate", #means: I'm navigating to a different site
            "Sec-Fetch-User": "?1", #means: I'm using a mobile device
            "Sec-Fetch-Dest": "document", #means: I'm navigating to a document
            "Accept-Encoding": "gzip, deflate, br", #means: I accept all kinds of encodings
            "Accept-Language": "en-US, ar, zh-CN, fr, de, it, ja, ko, ru, es", #means: I accept all kinds of languages
        },
        {#make a chrome/windows 10 user agent
            "Connection": "keep-alive", #means: keep the connection open
            "Cache-Control": "max-age=0", #means: don't cache
            "sec-ch-ua": f'"Chromium";v="{random.randint(90, 95)}", "Google Chrome";v="{random.randint(90, 95)}", ";Not A Brand";v="99"', #means: I'm using Chrome 94
            "sec-ch-ua-mobile": "?0", #means: I'm not using a mobile device
            "sec-ch-ua-platform": f'"Windows";v="{random.choice(["10.0", "8.1", "8", "7", "Vista", "XP"])}"', #means: I'm using Windows 10
            "Upgrade-Insecure-Requests": "1", #means: I want to be redirected to https if possible
            "User-Agent": f"Mozilla/5.0 (Windows NT {random.choice(['10.0', '6.1', '6.3'])}; Win64; x64) AppleWebKit/{random.randint(500, 599)}.36 (KHTML, like Gecko) Chrome/{random.randint(90, 95)}.0.0.0 Safari/{random.randint(500, 599)}.36", #means: I'm using Windows 10 and Chrome
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", #means: I accept all kinds of files
            "Sec-Fetch-Site": "none", #means: I'm not on a different site
            "Sec-Fetch-Mode": "navigate", #means: I'm navigating to a different site
            "Sec-Fetch-User": "?1", #means: I'm not using a mobile device
            "Sec-Fetch-Dest": "document", #means: I'm navigating to a document
            "Accept-Encoding": "gzip, deflate, br", #means: I accept all kinds of encodings
            "Accept-Language": "en-US, ar, zh-CN, fr, de, it, ja, ko, ru, es", #means: I accept all kinds of languages
        },
    ]
    h = random.choice(headers)
    
    #append "charset=utf-8" to the "Content-Type" header
    h["Content-Type"] = "text/html; charset=utf-8"
    return h




def search_google(q: str) -> list[SearchResult]:
    # search google
    
    cookie_data = {
    "CAPTCHA_SOLVER_ACTIVE": "false",
    "GOOGLE_OGPC_COOKIE": "",
    "GOOGLE_NID_COOKIE": "",
    "GOOGLE_AEC_COOKIE": "",
    "GOOGLE_1P_JAR_COOKIE": "",
    "GOOGLE_ABUSE_COOKIE": ""
    }
    
    cookies = {
        "OGPC": cookie_data["GOOGLE_OGPC_COOKIE"],
        "NID": cookie_data["GOOGLE_NID_COOKIE"],
        "AEC": cookie_data["GOOGLE_AEC_COOKIE"],
        "1P_JAR": cookie_data["GOOGLE_1P_JAR_COOKIE"],
        "GOOGLE_ABUSE_EXEMPTION": cookie_data["GOOGLE_ABUSE_COOKIE"]
    }
    
    headers = get_random_header()
    
    r = requests.get(f"https://www.google.com/search?q={q}", headers=headers, cookies=cookies)
    
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    
    # get search results
    results = []
    for i in soup.find_all("div", class_="g"):
        try:
            # needed info:
            # title
            # url
            # description
            # image url
            # provider (google)
            # provider url (google.com)
            # is_nsfw (bool)
            
            title = i.find("h3").text
            link = i.find("a")["href"]
            
            try:
                description = i.find("span", class_="aCOpRe").text
            except:
                description = ""
                
            image = i.find("img")["src"]
            provider = "Google"
            provider_url = "https://www.google.com"
            is_nsfw = False
            
            results.append(SearchResult(title, link, description, image, provider, provider_url, is_nsfw))
        
        except Exception as e:
            print(e)
    
    return results
    

def search_tpb(q: str) -> list[SearchResult]:
    """
    Search The Pirate Bay for the query q.
    Returns a list of SearchResult objects.
    """
    
    url = f"https://apibay.org/q.php?q={q}"
    
    r = requests.get(url)
    
    data = r.json()
    
    results = []
    
    for item in data:
        #{
        # "id": str(int),
        # "name": str,
        # "info_hash": str,
        # "leechers": str(int),
        # "seeders": str(int),
        # "num_files": str(int),
        # "size": str(int),
        # "username": str,
        # "added": str(int),
        # "status": str,
        # "category": str(int),
        # "imdb": str
        #}
        
        title = item["name"]
        url = f"https://thepiratebay.org/description.php?id={item['id']}"
        description = f"Seeders: {item['seeders']} | Leechers: {item['leechers']} | Size: {calculate_filesize(int(item['size']))}"
        image_url = ""
        provider = "The Pirate Bay"
        provider_url = "https://thepiratebay.org/"
        
        nsfw_categories = [502, 505, 506]
        is_nsfw = (int(item["category"]) in nsfw_categories)
        
        if is_nsfw:
            description += " | NSFW"
        
        res = SearchResult(title, url, description, image_url, provider, provider_url, is_nsfw)
        results.append(res)
    
    return results
    
