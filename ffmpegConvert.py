import subprocess
from pathlib import Path
import sys

ffmpegPath = r"c:\tools\Player\ffmpeg-20180802-c9118d4-win64-static\bin\ffmpeg.exe"

params = {
    "input":r"\\SWUFE\asset\assetAV\纪录片库\bilibili未整理\\",
    "output":r"\\SWUFE\asset\assetAV\纪录片库\bilibili\\"
}

def ffmpegConvert(inputPath, outputPath):
    p = subprocess.Popen([ffmpegPath, "-i", str(inputPath), "-codec", "copy", str(outputPath)], shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        outs, errs = p.communicate(timeout=600)
    except TimeoutExpired:
        p.kill()
        outs, errs = p.communicate()


def listFlv(inputPath):
    p = Path(inputPath)
    if (p.exists() and p.is_dir()):
        return p.glob('**/*.flv')


def checkConverted(inputPathObj,outputPath):
    return p.with_suffix("mp4").is_file()


def convert(inputPath, outputPath):

    #list files
    flvlst = listFlv(inputPath)

    #mk output dir
    output = Path(outputPath)
    if (output.is_dir() is not True):
        output.mkdir(parents=True, exist_ok=True)

    #loop
    ti =0
    for i in flvlst:
        ti+=1
        print(f"Transcoding:{i}, Progress:{ti}")

        r = i.relative_to(inputPath)
        o = output / r
        o = o.with_name(i.name).with_suffix(".mp4")
        print(f"To:{o}")

        if (o.is_file()):
            print(f"Dump file:{o} will not converted")
            continue

        ffmpegConvert(i,o)
        print("Done!")

convert(params["input"],params["output"])

# ffmpegConvert(
#     r"c:\tools\Player\ffmpeg-20180802-c9118d4-win64-static\bin\0094.哔哩哔哩-神奇的大脑：第1集 [超清版].flv",
#     r"c:\tools\Player\ffmpeg-20180802-c9118d4-win64-static\bin\0094.哔哩哔哩-神奇的大脑：第1集 [超清版].mp4"
#              )

import yiiUtils