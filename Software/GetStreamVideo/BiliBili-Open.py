import json
import requests
import tkinter
from tkinter import ttk
from tkinter import scrolledtext
import datetime
import threading
import time
import os


class Window:

    def __init__(self):
        # 窗口定义
        self.window = tkinter.Tk()
        self.window.title("BiliBili直播下载工具")
        self.window.geometry("400x500")
        self.finish_flag = 0

        # 组件定义
        banner = tkinter.Label(self.window, text="欢迎使用本工具,请您在发布视频时注明工具作者", font="微软雅黑 12 bold")
        banner.place(x=15, y=15, anchor="nw")

        self.room_id = tkinter.StringVar()
        room_id_label = tkinter.Label(self.window, text="房间号", font="微软雅黑 11")
        room_id_label.place(x=15, y=47, anchor="nw")
        room_id_entry = tkinter.Entry(self.window, show=None, font="微软雅黑 11", textvariable=self.room_id)
        room_id_entry.place(x=70, y=49, anchor="nw")
        room_check_button = tkinter.Button(self.window, text="获取直播间信息", font="微软雅黑 10", bitmap="gray25",
                                           compound=tkinter.RIGHT, width=130, height=18, command=self.check)
        room_check_button.place(x=260, y=47, anchor="nw")

        self.quality_list = tkinter.StringVar()
        quality_label = tkinter.Label(self.window, text="画质", font="微软雅黑 11")
        quality_label.place(x=15, y=90, anchor="nw")
        self.quality_combobox = ttk.Combobox(self.window, textvariable=self.quality_list)
        self.quality_combobox.place(x=70, y=90, anchor="nw")
        self.quality_combobox["values"] = ["请选择", "无数据"]
        self.quality_combobox.current(0)

        self.start_button = tkinter.Button(self.window, text="开始", font="微软雅黑 11", bitmap="gray25",
                                           compound=tkinter.RIGHT,
                                           width=50, height=20, command=self.threading_start)
        self.start_button.place(x=175, y=130, anchor="nw")

        log_label = tkinter.Label(self.window, text="运行日志", font="微软雅黑 11")
        log_label.place(x=15, y=160, anchor="nw")
        self.log_area = scrolledtext.ScrolledText(self.window, width=44, height=15, font="微软雅黑 10")
        self.log_area.place(x=15, y=190, anchor="nw")
        self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 程序开始运行!\n")

        self.window.mainloop()

    def check(self):
        if len(self.room_id.get()) == 0:
            self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 尚未输入房间号!\n")
            self.window.update()
            return
        room_info_api = "****"
        room_info = json.loads(requests.get(room_info_api).text)
        if room_info["****"] == "获取房间基础信息失败":
            self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 房间不存在!\n")
            self.start_button["state"] = tkinter.DISABLED
            self.window.update()
        elif room_info["*****"] == 0:
            self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 尚未开播!\n")
            self.start_button["state"] = tkinter.DISABLED
            self.window.update()
        elif room_info["*****"] == 1:
            self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 正在直播!\n")
            self.start_button["state"] = tkinter.NORMAL
            self.get_quality()
        elif room_info["*****"] == 2:
            self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 正在轮播!\n")
            self.start_button["state"] = tkinter.NORMAL
            self.get_quality()

    def get_quality(self):
        if len(self.room_id.get()) == 0:
            self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 尚未输入房间号!\n")
            self.window.update()
            return
        quality_api = "****"
        quality_info = json.loads(requests.get(quality_api).text)["****"]
        quality_list = []
        self.log_area.insert(tkinter.END, "当前直播间提供以下画质,请选择 : \n")
        for item in quality_info:
            self.log_area.insert(tkinter.END, "___" + item["****"])
            quality_list.append(item["****"])
        self.log_area.insert(tkinter.END, "\n")
        self.quality_combobox.config(values=quality_list)
        self.window.update()

    def threading_start(self):
        self.finish_flag = 0
        report_thread = threading.Thread(target=self.report_status)
        start_thread = threading.Thread(target=self.start)
        report_thread.start()
        start_thread.start()

    def report_status(self):
        while self.finish_flag == 0:
            file_list = os.listdir()
            file_list.sort(key=lambda filename: os.path.getmtime(filename))
            newest_file = file_list[-1]
            time.sleep(3)
            size = os.path.getsize(newest_file)
            if size < 1024:
                self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 已下载 : " + str(
                    round(size, 2)) + "B\n")
            elif 1024 <= size < 1048576:
                size = size / 1024
                self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 已下载 : " + str(
                    round(size, 2)) + "KB\n")
            elif 1048576 <= size < 1073741824:
                size = size / 1048576
                self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 已下载 : " + str(
                    round(size, 2)) + "MB\n")
            elif 1073741824 <= size:
                size = size / 1048576
                self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 已下载 : " + str(
                    round(size, 2)) + "MB\n")
            

    def start(self):
        if len(self.room_id.get()) == 0:
            self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 尚未输入房间号!\n")
            self.window.update()
            return
        quality_choosen = self.quality_combobox.get()
        self.log_area.insert(tkinter.END, "<" + str(
            datetime.datetime.now().strftime(
                "%X")) + "> 当前所选画质 : " + quality_choosen + " , 正在开始下载,有时可能会突然报下载完成,重新获取信息再开始即可...\n")
        bitrate = 0
        quality_api = "****"
        quality_info = json.loads(requests.get(quality_api).text)["****"]
        for item in quality_info:
            if item["****"] == quality_choosen:
                bitrate = item["****"]
                break
        stream_links = json.loads(requests.get(url="****").text)["*****"]
        for item in stream_links:
            link = item["****"]
            response_code = requests.head(link).status_code
            if response_code != 200:
                continue
            else:
                stream_data = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                        "Chrome/80.0.3987.122 Safari/537.36"},
                                           stream=True)
                save_file = open(str(self.room_id.get()) + "房间的" + datetime.datetime.now().strftime("%F") + "号录播.flv",
                                 "wb")
                for chunk in stream_data.iter_content(chunk_size=128):
                    if chunk:
                        save_file.write(chunk)
                save_file.close()
                break
        self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> 下载完成或直播已经结束!!\n")
        self.finish_flag = 1


if __name__ == '__main__':
    start_window = Window()
