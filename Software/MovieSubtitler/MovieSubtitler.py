import tkinter as tk
import tkinter.filedialog
import re
import os
import chardet
import ffmpy3
import time
import threading


def rename():
    root_path = file_path
    if len(root_path) == 0:
        file_name.set("尚未选择文件夹！")
        return
    need_2_del = reduce_word.get()
    for home, dirs, files in os.walk(root_path):
        for filename in files:
            old_fullname = os.path.join(home, filename)
            new_fullname = old_fullname.replace(need_2_del, "")
            os.rename(old_fullname, os.path.join(root_path, new_fullname))


def refresh_filename():
    path = file_path
    if len(path) == 0:
        file_name.set("尚未选择文件夹！")
        return
    root = path.split("\\")[-1]
    final_name = ""
    for home, dirs, files in os.walk(path):
        for filename in files:
            fullname = os.path.join(home, filename)
            final_name = final_name + root + str(fullname.split(root)[1]) + "\n"
    file_name.set(final_name)


def choose_file(return_position, real_position):
    file = tkinter.filedialog.askopenfilename()
    file = file.replace("/", "\\")
    real_position.set(file)
    split = str(file).split("\\")
    final_file = split[0] + "\\"
    for item in split[1:-1]:
        regex_it = re.sub(r".*", ".", string=item)
        final_file = final_file + regex_it + "\\"
    final_file = final_file + split[-1]
    return_position.set(final_file)


def choose_dir(return_position):
    dir_choose = tkinter.filedialog.askdirectory()
    dir_choose = dir_choose.replace("/", "\\")
    global file_path
    file_path = str(dir_choose)
    split = str(dir_choose).split("\\")
    final_path = split[0] + "\\"
    for item in split[1:-1]:
        final_path = final_path + re.sub(r".*", ".", string=item) + "\\"
    final_path = final_path + split[-1]
    root = split[-1]
    final_name = ""
    for home, dirs, files in os.walk(dir_choose):
        for filename in files:
            fullname = os.path.join(home, filename)
            final_name = final_name + root + str(fullname.split(root)[1]) + "\n"
    file_name.set(final_name)
    return_position.set(final_path)


def start_coding():
    video_list = []
    subtitle_list = []
    if len(video1_real_path.get()) != 0:
        video_list.append(video1_real_path.get())

    if len(video2_real_path.get()) != 0:
        video_list.append(video2_real_path.get())

    if len(video3_real_path.get()) != 0:
        video_list.append(video3_real_path.get())

    if len(video4_real_path.get()) != 0:
        video_list.append(video4_real_path.get())

    if len(video5_real_path.get()) != 0:
        video_list.append(video5_real_path.get())

    if len(subtitle1_real_path.get()) != 0:
        subtitle_list.append(subtitle1_real_path.get())

    if len(subtitle2_real_path.get()) != 0:
        subtitle_list.append(subtitle2_real_path.get())

    if len(subtitle3_real_path.get()) != 0:
        subtitle_list.append(subtitle3_real_path.get())

    if len(subtitle4_real_path.get()) != 0:
        subtitle_list.append(subtitle4_real_path.get())

    if len(subtitle5_real_path.get()) != 0:
        subtitle_list.append(subtitle5_real_path.get())
    if len(video_list) != len(subtitle_list):
        coding_status.set("视频与字幕数量不符!")
        return
    if len(video_list) == 0 or len(subtitle_list) == 0:
        coding_status.set("缺少必要文件！")
        return
    global mission_count
    mission_count = len(video_list)
    for item in subtitle_list:
        trans_code_utf8(item)
    thread_list = []
    threading.Thread(target=bar_status).start()
    for (video, subtitle) in zip(video_list, subtitle_list):
        thread_list.append(threading.Thread(target=ffmpeg, args=(video, subtitle)))
    for thread in range(len(thread_list)):
        thread_list[thread].start()


def trans_code_utf8(file):
    coding_status.set("字幕文件转码...")
    with open(file, "rb") as binary_file:
        charset = chardet.detect(binary_file.read())
        binary_file.close()
    with open(file, "rb") as read_file:
        cache_data = read_file.read()
        read_file.close()
    binary = cache_data
    decoded_str = binary.decode(charset["encoding"], "ignore")
    with open(file, "w", encoding="utf-8", buffering=1) as write_file:
        write_file.write(decoded_str)
        write_file.close()


def ffmpeg(video, subtitle):
    print("Video is : " + str(video))
    print("Subtitle is : " + str(subtitle))
    coding_status.set("烧录字幕中...")
    start_button['state'] = tk.DISABLED
    start_button['text'] = "正在烧录字幕"
    video_fullname = str(video).split("\\")[-1]
    video_suffix = video_fullname.split(".")[-1]
    video_name = video_fullname.split(".")
    new_name = ""
    for item in video_name[0:-1]:
        new_name = new_name + item
    new_name = new_name + "_chs&eng." + video_suffix
    ff = ffmpy3.FFmpeg(
        inputs={video: None, subtitle: None},
        outputs={new_name: "-map 0:v -map 0:a -map 1:s -c copy -y"}
    )
    ff.run()
    global status_flag
    status_flag = status_flag + 1


def bar_status():
    clean_line = status_bar_canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
    status_bar_canvas.coords(clean_line, (0, 0, 325, 20))
    window.update()
    fill_line = status_bar_canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
    window.update()
    global mission_count
    each_width = 325 / mission_count
    now_location = 0
    global status_flag
    last_flag = status_flag
    while True:
        if last_flag == status_flag:
            if last_flag == mission_count:
                status_flag = 0
                start_button['state'] = tk.NORMAL
                start_button['text'] = "开始烧录字幕"
                break
            time.sleep(1)
            continue
        else:
            last_flag = status_flag
            now_location = now_location + each_width
            status_bar_canvas.coords(fill_line, (0, 0, now_location, 20))
            window.update()
            continue


if __name__ == '__main__':
    window = tk.Tk()
    window.title("FAFU-BTForum 字幕添加器V1.0")
    window.geometry("950x600")

    video_label = tk.Label(window, text="1.选择视频文件", font="微软雅黑 15 bold").place(x=10, y=15, anchor="nw")
    video_warning = tk.Label(window, text="请先使用改名区精简文件名，且视频文件顺序与字幕文件顺序必须一致！",
                             font="微软雅黑 10 bold").place(x=10, y=45, anchor="nw")

    video1_real_path = tk.StringVar()
    video1_path = tk.StringVar()
    video1_choose_label = tk.Label(window, text="视频1", font="微软雅黑 12").place(x=10, y=70, anchor="nw")
    video1_choose_entry = tk.Entry(window, show=None, font="微软雅黑 10", textvariable=video1_path).place(x=110, y=70,
                                                                                                      anchor="nw")
    video1_choose_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                     compound=tkinter.RIGHT, width=45, height=18,
                                     command=lambda: choose_file(video1_path, video1_real_path)).place(x=290, y=67.5,
                                                                                                       anchor="nw")
    video2_real_path = tk.StringVar()
    video2_path = tk.StringVar()
    video2_choose_label = tk.Label(window, text="视频2(可选)", font="微软雅黑 12").place(x=10, y=95, anchor="nw")
    video2_choose_entry = tk.Entry(window, show=None, font="微软雅黑 10", textvariable=video2_path).place(x=110, y=95,
                                                                                                      anchor="nw")
    video2_choose_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                     compound=tkinter.RIGHT, width=45, height=18,
                                     command=lambda: choose_file(video2_path, video2_real_path)).place(x=290, y=94,
                                                                                                       anchor="nw")

    video3_real_path = tk.StringVar()
    video3_path = tk.StringVar()
    video3_choose_label = tk.Label(window, text="视频3(可选)", font="微软雅黑 12").place(x=10, y=120, anchor="nw")
    video3_choose_entry = tk.Entry(window, show=None, font="微软雅黑 10", textvariable=video3_path).place(x=110, y=120,
                                                                                                      anchor="nw")
    video3_choose_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                     compound=tkinter.RIGHT, width=45, height=18,
                                     command=lambda: choose_file(video3_path, video3_real_path)).place(x=290, y=119,
                                                                                                       anchor="nw")

    video4_real_path = tk.StringVar()
    video4_path = tk.StringVar()
    video4_choose_label = tk.Label(window, text="视频4(可选)", font="微软雅黑 12").place(x=10, y=145, anchor="nw")
    video4_choose_entry = tk.Entry(window, show=None, font="微软雅黑 10", textvariable=video4_path).place(x=110, y=145,
                                                                                                      anchor="nw")
    video4_choose_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                     compound=tkinter.RIGHT, width=45, height=18,
                                     command=lambda: choose_file(video4_path, video4_real_path)).place(x=290, y=144,
                                                                                                       anchor="nw")

    video5_real_path = tk.StringVar()
    video5_path = tk.StringVar()
    video5_choose_label = tk.Label(window, text="视频5(可选)", font="微软雅黑 12").place(x=10, y=170, anchor="nw")
    video5_choose_entry = tk.Entry(window, show=None, font="微软雅黑 10", textvariable=video5_path).place(x=110, y=170,
                                                                                                      anchor="nw")
    video5_choose_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                     compound=tkinter.RIGHT, width=45, height=18,
                                     command=lambda: choose_file(video5_path, video5_real_path)).place(x=290, y=169,
                                                                                                       anchor="nw")

    subtitle_label = tk.Label(window, text="2.选择字幕文件", font="微软雅黑 15 bold").place(x=10, y=195, anchor="nw")

    subtitle1_real_path = tk.StringVar()
    subtitle1_path = tk.StringVar()
    subtitle1_choose_label = tk.Label(window, text="字幕1", font="微软雅黑 12").place(x=10, y=225, anchor="nw")
    subtitle1_choose_entry = tk.Entry(window, show=None, font="微软雅黑 10", textvariable=subtitle1_path).place(x=110,
                                                                                                            y=225,
                                                                                                            anchor="nw")
    subtitle1_choose_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                        compound=tkinter.RIGHT, width=45, height=18,
                                        command=lambda: choose_file(subtitle1_path, subtitle1_real_path)).place(x=290,
                                                                                                                y=224,
                                                                                                                anchor="nw")

    subtitle2_real_path = tk.StringVar()
    subtitle2_path = tk.StringVar()
    subtitle2_choose_label = tk.Label(window, text="字幕2(可选)", font="微软雅黑 12").place(x=10, y=250, anchor="nw")
    subtitle2_choose_entry = tk.Entry(window, show=None, font="微软雅黑 10", textvariable=subtitle2_path).place(x=110,
                                                                                                            y=250,
                                                                                                            anchor="nw")
    subtitle2_choose_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                        compound=tkinter.RIGHT, width=45, height=18,
                                        command=lambda: choose_file(subtitle2_path, subtitle2_real_path)).place(x=290,
                                                                                                                y=249,
                                                                                                                anchor="nw")

    subtitle3_real_path = tk.StringVar()
    subtitle3_path = tk.StringVar()
    subtitle3_choose_label = tk.Label(window, text="字幕3(可选)", font="微软雅黑 12").place(x=10, y=275, anchor="nw")
    subtitle3_choose_entry = tk.Entry(window, show=None, font="微软雅黑 10", textvariable=subtitle3_path).place(x=110,
                                                                                                            y=275,
                                                                                                            anchor="nw")
    subtitle3_choose_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                        compound=tkinter.RIGHT, width=45, height=18,
                                        command=lambda: choose_file(subtitle3_path, subtitle3_real_path)).place(x=290,
                                                                                                                y=274,
                                                                                                                anchor="nw")

    subtitle4_real_path = tk.StringVar()
    subtitle4_path = tk.StringVar()
    subtitle4_choose_label = tk.Label(window, text="字幕4(可选)", font="微软雅黑 12").place(x=10, y=300, anchor="nw")
    subtitle4_choose_entry = tk.Entry(window, show=None, font="微软雅黑 10", textvariable=subtitle4_path).place(x=110,
                                                                                                            y=300,
                                                                                                            anchor="nw")
    subtitle4_choose_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                        compound=tkinter.RIGHT, width=45, height=18,
                                        command=lambda: choose_file(subtitle4_path, subtitle4_real_path)).place(x=290,
                                                                                                                y=299,
                                                                                                                anchor="nw")

    subtitle5_real_path = tk.StringVar()
    subtitle5_path = tk.StringVar()
    subtitle5_choose_label = tk.Label(window, text="字幕5(可选)", font="微软雅黑 12").place(x=10, y=325, anchor="nw")
    subtitle5_choose_entry = tk.Entry(window, show=None, font="微软雅黑 10", textvariable=subtitle5_path).place(x=110,
                                                                                                            y=325,
                                                                                                            anchor="nw")
    subtitle5_choose_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                        compound=tkinter.RIGHT, width=45, height=18,
                                        command=lambda: choose_file(subtitle5_path, subtitle5_real_path)).place(x=290,
                                                                                                                y=324,
                                                                                                                anchor="nw")

    rename_label = tk.Label(window, text="改名区", font="微软雅黑 15 bold").place(x=460, y=15, anchor="nw")
    rename_warning = tk.Label(window, text="单个文件请自行改名，本工具只适用于具有相同特征的多个文件（例如一次\n性下好的美剧）",
                              font="微软雅黑 10 bold").place(x=460, y=45, anchor="nw")

    file_dir = tk.StringVar()
    file_dir_label = tk.Label(window, text="文件夹", font="微软雅黑 12").place(x=460, y=100, anchor="nw")
    file_dir_entry = tk.Entry(window, show=None, width=55, font="微软雅黑 10", textvariable=file_dir).place(x=462, y=130,
                                                                                                        anchor="nw")
    file_dir_button = tk.Button(window, text="浏览", font="微软雅黑 10", bitmap="gray25",
                                compound=tkinter.RIGHT, width=45, height=18,
                                command=lambda: choose_dir(file_dir)).place(x=520, y=100, anchor="nw")

    reduce_word = tk.StringVar()
    reduce_label = tk.Label(window, text="删除的文字(包括符号)", font="微软雅黑 12").place(x=460, y=155, anchor="nw")
    reduce_entry = tk.Entry(window, textvariable=reduce_word, show=None, width=55, font="微软雅黑 10").place(x=462, y=185,
                                                                                                         anchor="nw")

    file_path = ""
    file_name = tk.StringVar()
    show_file_name_label = tk.Label(window, text="当前目录下文件名称", font="微软雅黑 12").place(x=460, y=215, anchor="nw")
    file_name_Label = tk.Label(window, justify=tk.LEFT, textvariable=file_name, border=None, font="微软雅黑 8").place(x=460,
                                                                                                                  y=240,
                                                                                                                  anchor="nw")
    rename_button = tk.Button(window, text="改名", font="微软雅黑 10", bitmap="gray25",
                              compound=tkinter.RIGHT, width=45, height=18,
                              command=rename).place(x=620, y=214, anchor="nw")

    refresh_button = tk.Button(window, text="刷新", font="微软雅黑 10", bitmap="gray25",
                               compound=tkinter.RIGHT, width=45, height=18,
                               command=refresh_filename).place(x=680, y=214, anchor="nw")

    start_button = tk.Button(window, text="开始烧录字幕", font="微软雅黑 12", bitmap="gray25",
                             compound=tkinter.RIGHT, width=120, height=20,
                             command=start_coding)
    start_button.place(x=130, y=360, anchor="nw")
    coding_status = tk.StringVar()
    mission_count = 0
    status_flag = 0
    coding_status_label = tk.Label(window, text="正在进行：", font="微软雅黑 12").place(x=10, y=390, anchor="nw")
    coding_status_entry = tk.Entry(window, textvariable=coding_status, show=None, width=40, font="微软雅黑 10").place(x=100, y=395, anchor="nw")
    status_bar_label = tk.Label(window, text="烧录进度：", font="微软雅黑 12").place(x=10, y=415, anchor="nw")
    status_bar_canvas = tk.Canvas(window, width=325, height=20, bg="white")
    status_bar_canvas.place(x=98, y=420, anchor="nw")

    window.mainloop()
