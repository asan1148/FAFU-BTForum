# Intro

This tool is used to burn the subtitle into a MKV container.

Due to my laptop issue and it needs to be return to the manufacturer to repaire it ,this tool is write in a rush ,there are plenty of codes that can/need to be optimize ,but as for me this is only a simple tool ,so i wont do it myself ,you can custom it anyway you want.

The most ridiculous thing is that ,i use a good amount of repeated variable ,and it certainly needs to be a list or a dict ... Stupid me

# How to use

**There is two way to use it : Download the exe file or complie by yourself**
* 1.Download the exe file and run it
  * 1.1 extract the compressed file (already included ffmpeg/ffprobe/ffplay and mkvtoolnix)
  * 1.2 run the MovieSubtitler.exe 

* 2.Complie by yourself and run it
  * 2.1 download the source code named MovieSubtitler.py ,and edit it on your python ide
  * 2.2 after you finish your editing ,compile it and it will work fine

# Warning
* 1.This tool will no replace/overwrite your source video file ,but for subtitle file , it will . So make sure you got your subs backup
* 2.This tool can't deal with MKV container  with muti stream channel ,so you need to use **mkvtoolnix** to remove those unnecessary stream. *e.g cover image (mjpeg) with video stream and no duration.
* 3.This tool will reformat your subtitle file from any encoding to UTF-8
* 4.This tool includes many crap code so maybe you need to optimize it for your own useage.
