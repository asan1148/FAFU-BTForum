import threading
import os


def combined(v, a, o):
    os.system("chcp 65001")
    os.system("ffmpeg -i \"%s\" -i \"%s\" -c copy -map 0:v:0 -map 1:a:0 \"%s\"" % (v, a, o))


path = os.getcwd()
temp_list = os.listdir(path)
file_list = []
for file in temp_list:
    file_name = file.split(".")[0:-1]
    temp = ""
    for i in range(len(file_name)):
        if i != len(file_name) - 1:
            temp = temp + file_name[i] + "."
        else:
            temp = temp + file_name[i]
    file_name = temp
    if file_name != "combine_list" and \
            file_name != "ffmpeg" and \
            file_name != "Mixer_Past_Stream" and \
            file_name != "Sub_Restructure" and \
            file_name != "VA_Mixer" and \
            file_name != "Youtube_List_Download" and \
            file_name != "youtube-dl" and \
            file_name != "edit" and \
            file_name != "combine":
        if file_name in file_list:
            continue
        else:
            file_list.append(file_name)
for name in file_list:
    if len(name) == 0:
        continue
    video = name + ".mp4"
    audio = name + ".m4a"
    output = name + "_combined.mp4"
    threading.Thread(target=combined, args=(video, audio, output)).start()
