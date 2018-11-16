import requests
from bs4 import BeautifulSoup
import re

def __addNum(matchObj,n=1):
    if (matchObj is not None):
        return "ep"+str(int(matchObj.group(1))+n)
    return '0'

regex=re.compile(r"ep(\d+)/*$")

def createBilibiliEpisodeURL(videoUrl,n):
    return regex.sub(lambda m: __addNum(m, n), videoUrl)


def parseBilibiliVideoPage(video_url):
    #page req
    page = requests.get(video_url)

    if (page.status_code != 200):
        print("[wrong code:%d]"%page.status_code,video_url)
        return None

    v = page.url

    soup = BeautifulSoup(page.content,'html.parser')
    head = soup.head
    body = soup.body

    #title
    title_str = head.title.string

    #desc
    f = head.find("meta",attrs={"name": "description"})
    desc_str = f["content"]

    #keywords
    f = head.find("meta",attrs={"name": "keywords"})
    keywords_str = f["content"]

    #thumb
    f = head.find("meta",attrs={"property": "og:image"})
    img_url = f["content"]

    #episode
    epi_urls = [v]
    has_multiepi=False
    epi = body.find("ul",class_="episode-list")
    if (epi is not None):
        fa = epi.find_all("li",class_ = "episode-item")
        if (fa is not None and len(fa)>1):
            has_multiepi=True
            for i in range(1,len(fa)):
                epi_urls.append(createBilibiliEpisodeURL(v,i))

    return {
               "title":title_str,
                "desc":desc_str,
            "keywords":keywords_str,
                "img_url":img_url,
               "has multi":has_multiepi,
        "epi_urls":epi_urls
    }

#vvvv = "https://www.bilibili.com/bangumi/play/ep216015/"
#print(parseBilibiliVideoPage(vvvv))


#v = "https://www.bilibili.com/bangumi/play/ep120822/"
# up = url.urlparse(v)
# print(up.path)
# upp = pathlib.PurePath(up.path)
# str(upp.as_posix())

    #一根绳子
#v = "https://www.bilibili.com/bangumi/play/ep120822/"

    #涟漪
v = "https://www.bilibili.com/bangumi/play/ep230308/"

print(parseBilibiliVideoPage(v))



