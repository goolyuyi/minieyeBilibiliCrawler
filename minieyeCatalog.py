import videoInfo
from pathlib import Path
from pathlib import PurePath

from urllib.parse import urlparse
import requests
import re
import csv
import json

################Params##################
minieyeParam = {
    "inputFile":"minieye2018-8-14",

    "writeJSON":False,
    "fromJSON":False,
    "JSONFile":"minieye.json",

    "genMeta":True,
    "metaOutputPath":"meta2018-8-14",
    "imgExistSkip":True,

    "genDownloadList":True,
    "downloadListFile":"downlist2018-8-14.txt",
    "downloadListSize":-1,
    "multiEpisodeIncludeFirst":True,

    "genCSV":True,
    "csvPath":"meta2018-8-14.csv"
}


# minieyeParam = {
#     "inputFile":"minieye2",
#
#     "writeJSON":False,
#     "fromJSON":False,
#     "JSONFile":"minieye.json",
#
#     "genMeta":False,
#     "metaOutputPath":"meta",
#     "imgExistSkip":True,
#
#     "genDownloadList":True,
#     "downloadListFile":"downlist.txt",
#     "downloadListSize":-1,
#     "multiEpisodeIncludeFirst":True,
#
#     "genCSV":False,
#     "csvPath":"meta.csv"
# }


###############Funcs####################

titleRegex = re.compile(r'^(.+?)_')

def doTitle(title):
    m = re.match(titleRegex, title)
    if (m is not None):
         return re.sub(r'[^\w]', '_', m.group(1))
    else:
        return re.sub(r'[^\w]', '_', title)

GRUBER_URLINTEXT_PAT = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

def doURL(text):
    res = GRUBER_URLINTEXT_PAT.search(text)
    if (res is not None):
        return res.group(0)
    return None



def genBilibiliInfos(inputFile):
    inputPath = Path(inputFile)
    res = []

    with inputPath.open(mode='r',encoding="utf8") as f:
        linenum=0

        for line in f:
            linenum+=1

            if (not line.strip()):
                continue
            line = line.replace("\r","")
            line = line.replace("\n","")

            if (line.startswith('#')):
                continue

            line = doURL(line)
            if (line is None):
                continue

            p = urlparse(line)
            if ("bilibili" not in p.netloc):
                continue

            print("[%d]getting:"%linenum+p.geturl())

            vi = videoInfo.parseBilibiliVideoPage(p.geturl())

            print(vi)
            res.append(vi)

    return res

def genMeta(infos,outputPath,imgSkip):

    print("genMeta")

    outputPath = Path(outputPath)

    for vi in infos:

        dirname = vi['title']

        t = doTitle(dirname)
        dirPath = Path(outputPath,t)
        dirPath.mkdir(parents=True, exist_ok=True)

        img_url = urlparse(vi["img_url"])
        if (not img_url.scheme.strip()):
            continue

        img_ext = PurePath().suffix
        img_path = Path(dirPath,t+img_ext)

        if (img_path.exists() and imgSkip):
            print("img exist skip:",str(img_path))
            continue
        print("get img:[%s]"%t,vi["img_url"])
        img_req = requests.get(vi["img_url"],stream= True)

        if (img_req.status_code==200):


            with img_path.open("wb") as img_f:
                for chunk in img_req:
                    img_f.write(chunk)

        with open(Path(dirPath,"desc.txt"),'w',encoding="utf8") as desc_f:
            desc_f.write(vi["keywords"]+"\n")
            desc_f.write(vi["desc"])

def genDownloadList(infos,outputFile,downloadListSize,multiEpisodeIncludeFirst):
    print("genDownloadList")

    output = Path(outputFile)

    with output.open("w",encoding="utf8") as f:
        count = downloadListSize
        biggerCount = 1

        for vi in infos:
            lst = vi["epi_urls"] if multiEpisodeIncludeFirst else vi["epi_urls"][1:]
            for url in lst:
                count +=1
                if (downloadListSize>0 and count>=downloadListSize):
                    f.write("\n"+"*"*20+str(biggerCount)+"*"*20+"\n")
                    count =0
                    biggerCount+=1


                f.write(url+"\n")


def genCSV(infos,outputFile):
    print("genCSV")
    output = Path(outputFile)

    with output.open("w",newline='',encoding="utf_8_sig") as csvfile:
        fieldnames = ['title','b_title', 'desc','has multi',"#epis","img_url","epi_urls"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


        writer.writeheader()

        for vi in infos:
            wt = {
                'title': vi["keywords"],
                'b_title': vi["title"],
                'desc':vi["desc"],
                'has multi':vi["has multi"],
                '#epis':len(vi["epi_urls"]),
                'img_url':vi["img_url"],
                'epi_urls':vi["epi_urls"]
                  }
            writer.writerow(wt)


##############Main#####################
if (minieyeParam["writeJSON"] or not minieyeParam["fromJSON"]):
    infos = genBilibiliInfos(minieyeParam["inputFile"])
    if (minieyeParam["writeJSON"]):
        jsonPath = Path(minieyeParam["JSONFile"])
        with jsonPath.open('w') as jf:
            json.dump(infos,jf)
else:

    jsonPath = Path(minieyeParam["JSONFile"])
    with jsonPath.open('r') as jf:
        infos = json.load(jf)

print(len(infos))


if (minieyeParam["genMeta"]):
    genMeta(infos,minieyeParam["metaOutputPath"],minieyeParam["imgExistSkip"])

if (minieyeParam["genDownloadList"]):
    genDownloadList(infos,minieyeParam["downloadListFile"],\
                    minieyeParam["downloadListSize"],\
                    minieyeParam["multiEpisodeIncludeFirst"])

if (minieyeParam["genCSV"]):
    genCSV(infos,minieyeParam["csvPath"])