import colored
import os
import requests
import threading
from bs4 import BeautifulSoup as bs

play_list_url = "https://www.youtube.com/user/TheViperAOC/playlists"


def get_list():
    list_page = requests.get(play_list_url).text
    list_page_soup = bs(list_page, "lxml")
    play_list = list_page_soup.find_all("h3", {"class": "yt-lockup-title"})
    number = 0
    info_list = []
    print("All play list is : ")
    for item in play_list:
        list_title = item.a.get_text()
        list_url = "https://www.youtube.com" + item.a["href"]
        print("+------------------------------------------------------------------------+")
        print("{}Number : {}".format(colored.fg(5), colored.attr(0)) + str(number))
        print("{}List Title : {}".format(colored.fg(11), colored.attr(0)) + list_title)
        print("{}List URL : {}".format(colored.fg(1), colored.attr(0)) + list_url)
        list_info = (number, list_title, list_url)
        number += 1
        info_list.append(list_info)
    return info_list


def get_video(selected_info):
    list_page_url = selected_info[2]
    list_page = requests.get(list_page_url).text
    list_soup = bs(list_page, "lxml")
    video_list = list_soup.find_all("tr")
    number = 0
    info_list = []
    for item in video_list:
        info = item.find("a", {"class": "pl-video-title-link yt-uix-tile-link yt-uix-sessionlink spf-link"})
        video_url = "https://www.youtube.com" + info["href"]
        video_name = info.get_text()
        video_name = video_name.replace("\n", "")
        video_name = video_name.replace(" ", "")
        list_info = (number, video_name, video_url)
        number += 1
        info_list.append(list_info)
    return info_list


def download_subtitle(url):
    os.system("youtube-dl.exe --no-playlist --proxy \"http://127.0.0.1:1099\" --write-auto-sub --skip-download \"%s\"" % url)


def download_video(url):
    os.system("youtube-dl.exe --no-playlist --proxy \"http://127.0.0.1:1099\" -f \"(mp4)[width>=1920][height>=1080][fps>=60]\" \"%s\"" % url)


def download_audio(url):
    os.system("youtube-dl.exe --no-playlist --proxy \"http://127.0.0.1:1099\" -f \"(m4a)[asr=44100][abr<=320]\" \"%s\"" % url)


def threading_download(info):
    while True:
        if_only_sub_select = input("Would you like to Download Video+Audio+Subtitle or just Subtitle ? VAS/S").upper()
        if if_only_sub_select == "VAS":
            print("Downloading Video+Audio+Subtitle")
            for video in info:
                url = str(video[2])
                threading.Thread(target=download_audio, args=(url,)).start()
                threading.Thread(target=download_video, args=(url,)).start()
                threading.Thread(target=download_subtitle, args=(url,)).start()
            break
        elif if_only_sub_select == "S":
            print("Downloading only the Subtitle")
            for video in info:
                url = str(video[2])
                threading.Thread(target=download_subtitle, args=(url,)).start()
            break
        else:
            print("Please enter 'VAS'(for Video+Audio+Subtitle) or 'S'(only Subtitle)")
            continue


if __name__ == '__main__':
    print("Launching, please wait...")
    play_list_info_list = get_list()
    selected_list = None
    while True:
        try:
            list_selection = int(input("Which one would you like to use ? "))
        except TypeError:
            print("Wrong Input, Try again!")
            continue
        if list_selection > len(play_list_info_list):
            print("Too large number, Try again!")
            continue
        else:
            print("\nYour selection is :")
            print("+------------------------------------------------------------------------+")
            print("{}Number : {}".format(colored.fg(5), colored.attr(0)) + str(play_list_info_list[list_selection][0]))
            print("{}List Title : {}".format(colored.fg(11), colored.attr(0)) + play_list_info_list[list_selection][1])
            print("{}List URL : {}".format(colored.fg(1), colored.attr(0)) + play_list_info_list[list_selection][2])
            while True:
                try:
                    list_confirm = input("Is that correct ? Y/N").upper()
                except TypeError:
                    print("Please input 'Y' or 'N', Try again!")
                    continue
                if list_confirm == "Y":
                    print("Processing...")
                    selected_list = play_list_info_list[list_selection]
                    break
                elif list_confirm == "N":
                    print("Please try again...")
                    continue
                else:
                    print("Wrong input, please try again!")
                    continue
            break
    print("Entering List...")
    video_list_info = get_video(selected_list)
    threading_download(video_list_info)
