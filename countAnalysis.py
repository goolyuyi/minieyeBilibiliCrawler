from bs4 import BeautifulSoup
import re
import csv
from pathlib import Path
from pathlib import PurePath

# CAParam = {
#     "pagePath":r"d:\managed\MiniEyes\_video\raw\i_纪录\i_纪录的个人空间 - 哔哩哔哩 ( ゜- ゜)つロ 乾杯_ Bilibili (2018-08-11 下午10_56_31).html",
#     "writeCSV":True,
#     "CSVPath":"i_纪录_analysis.csv"
# }

CAParam = {
    "pagePath":r"d:\managed\MiniEyes\_video\raw\i_纪录\纪录片之家字幕组的个人空间 - 哔哩哔哩 ( ゜- ゜)つロ 乾杯_ Bilibili.html",
    "writeCSV":True,
    "CSVPath":"纪录片之家_analysis.csv"
}
#print(CAParam["pagePath"])

def parseViewCount(viewCount):
    mul = 1
    if (viewCount.endswith("万")):
        viewCount = viewCount.replace("万","")
        mul = 10000

    return int(float(viewCount)*mul)

soup = BeautifulSoup(open(CAParam["pagePath"],encoding="utf-8"),"html.parser")

pc = soup.find_all("div",class_= "post-content")

items = []
for item in pc:
    title_str=""
    title = item.find("div",class_= "title")
    if (title is None):
        continue
    title_str = title.string


    #link
    href = item.a.get('href')
    href_str =  href

    #view count
    vcn =0
    vc = item.find("span",class_= "view")
    if (vc is not None):
        vcn = parseViewCount(vc.string)

    items.append(
        {
        "title":title_str,
            "url":href,
            "vcn":vcn
    }
    )

print ("#items",len(items))

items.sort(key=lambda item:item["vcn"],reverse=True)

if (CAParam["writeCSV"]):
    output = Path(CAParam["CSVPath"])

    with output.open("w",newline='',encoding="utf_8_sig") as csvfile:
        fieldnames = ['title','url', 'vcn']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in items:
            writer.writerow(i)

for i in items:
    print(i)




