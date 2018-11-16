import subprocess
import pathlib

ffmpegPath = r"c:\tools\Player\ffmpeg-20180802-c9118d4-win64-static\bin\ffmpeg.exe"

folderPath = [
"e:\minieye\",
"e:\minieye\"
]

def ffmpegConvert(inputPath,outputPath):
    p = subprocess.Popen([ffmpegPath,"-i",inputPath,"-codec","copy",outputPath],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        outs, errs = p.communicate(timeout=120)
    except TimeoutExpired:
        p.kill()
        outs, errs = p.communicate()

#TODO convert a floders--allsubfolders flv
#TODO skip exist

















