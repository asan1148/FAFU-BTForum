import threading
import requests
import tkinter
import json
import time
import datetime
from tkinter import ttk
from tkinter import scrolledtext


class Downloader:
    def __init__(self):
        self.mission_total = 0
        self.mission_finished = 0
        # window define
        window = tkinter.Tk()
        window.title("FAFU国贸UN-Comtrade数据采集工具")
        screen_x = window.winfo_screenwidth()
        screen_y = window.winfo_screenheight()
        position_x = (screen_x - 900) / 2
        position_y = (screen_y - 700) / 2
        window.geometry("900x700+%d+%d" % (position_x, position_y))

        # part define
        banner = tkinter.Label(window, text="UN-Comtrade数据下载工具(突破数量限制)", font="微软雅黑 12 bold")
        banner.place(x=250, y=10, anchor="nw")
        comment = tkinter.Label(window, text="Develope by FAFU-BTForum", font="微软雅黑 10")
        comment.place(x=450, y=40, anchor="nw")

        type_label = tkinter.Label(window, text="1.Type of product", font="微软雅黑 11")
        type_label.place(x=10, y=70, anchor="nw")
        self.type_combobox = ttk.Combobox(window, width=25, height=3)
        self.type_combobox.place(x=160, y=72, anchor="nw")
        self.type_combobox["values"] = ["请选择:C=商品贸易/S=服务贸易", "C", "S"]
        self.type_combobox.current(0)

        frequency_label = tkinter.Label(window, text="2.Frequency", font="微软雅黑 11")
        frequency_label.place(x=10, y=100, anchor="nw")
        self.frequency_combobox = ttk.Combobox(window, width=25, height=2)
        self.frequency_combobox.place(x=160, y=102, anchor="nw")
        self.frequency_combobox["values"] = ["请选择:A=按年查询/M=按月查询", "A", "M"]
        self.frequency_combobox.current(0)

        classification_label = tkinter.Label(window, text="3.Classification", font="微软雅黑 11")
        classification_label.place(x=10, y=130, anchor="nw")
        self.classification_combobox = ttk.Combobox(window, width=25, height=10)
        self.classification_combobox.place(x=160, y=132, anchor="nw")
        self.classification_combobox["values"] = ["请选择:认证体系",
                                                  "+-------------HS区-------------+",
                                                  " | HS=默认值As reported,H0/ |",
                                                  " | 1/2/3/4/5分别为92/96/02/0 |",
                                                  " | 7/12/17                             |",
                                                  "+-------------------------------+",
                                                  "HS", "H0", "H1", "H2", "H3", "H4", "H5",
                                                  "+------------SITC区-----------+",
                                                  " | ST=默认值As reported,S1/ |",
                                                  " | 2/3/4分别为Rev.1/2/3/4      |",
                                                  "+-------------------------------+",
                                                  "ST", "S1", "S2", "S3", "S4",
                                                  "+-------------BEC区-----------+",
                                                  "BEC"]
        self.classification_combobox.current(0)

        periods_label = tkinter.Label(window, text="4.Periods(year)", font="微软雅黑 11")
        periods_label.place(x=10, y=160, anchor="nw")
        periods_require = tkinter.Label(window, justify=tkinter.LEFT,
                                        text="请写入起始年份(上面选按年查询,例如2010,2020或2010,2010)或\n月(上面选按月查询,例如202001,202003),以英文逗号\",\"分隔", font="微软雅黑 10")
        periods_require.place(x=10, y=183, anchor="nw")
        self.periods_entry = tkinter.Entry(window, font="微软雅黑 10")
        self.periods_entry.place(x=10, y=225, anchor="nw", width=380)

        reporters_label = tkinter.Label(window, text="5.Reporters", font="微软雅黑 11")
        reporters_label.place(x=10, y=250, anchor="nw")
        reporters_require = tkinter.Label(window, justify=tkinter.LEFT, text="请写入地区/国家ID,若有多个,以英文逗号\",\"分隔,可在右边查询", font="微软雅黑 10")
        reporters_require.place(x=10, y=273, anchor="nw")
        self.reporters_entry = tkinter.Entry(window, font="微软雅黑 10")
        self.reporters_entry.place(x=10, y=295, width=380)

        partners_label = tkinter.Label(window, text="6.Partners", font="微软雅黑 11")
        partners_label.place(x=10, y=320, anchor="nw")
        partners_require = tkinter.Label(window, justify=tkinter.LEFT, text="请写入地区/国家ID,若有多个,以英文逗号\",\"分隔,可在右边查询",
                                         font="微软雅黑 10")
        partners_require.place(x=10, y=343, anchor="nw")
        self.partners_entry = tkinter.Entry(window, font="微软雅黑 10")
        self.partners_entry.place(x=10, y=365, width=380)

        flows_label = tkinter.Label(window, text="7.Trade Flows", font="微软雅黑 11")
        flows_label.place(x=10, y=390, anchor="nw")
        flows_require = tkinter.Label(window, justify=tkinter.LEFT,
                                      text="请写入进出口类型(all就是all,1=Import,2=Export,3=re-Export,\n4=re-Import),若有多个,以英文逗号\",\"分隔,全部小写",
                                      font="微软雅黑 10")
        flows_require.place(x=10, y=413, anchor="nw")
        self.flows_entry = tkinter.Entry(window, font="微软雅黑 10")
        self.flows_entry.place(x=10, y=455, width=380)

        codes_label = tkinter.Label(window, text="8.Commodity Codes", font="微软雅黑 11")
        codes_label.place(x=10, y=480, anchor="nw")
        codes_require = tkinter.Label(window, text="请写入商品ID,若有多个,以英文逗号\",\"分隔,可超过20个,可在右边查询")
        codes_require.place(x=10, y=503, anchor="nw")
        self.codes_entry = tkinter.Entry(window, font="微软雅黑 10")
        self.codes_entry.place(x=10, y=525, width=380, anchor="nw")

        download_button = tkinter.Button(window, text="开始下载数据", font="微软雅黑 11", bitmap="gray25", compound=tkinter.RIGHT,
                                         width=120, height=25, command=self.threading_start)
        download_button.place(x=140, y=560, anchor="nw")
        file_save_tip = tkinter.Label(window, text="文件保存在本工具同目录下", font="微软雅黑 11 bold")
        file_save_tip.place(x=110, y=600, anchor="nw")
        log_label = tkinter.Label(window, text="运行日志", font="微软雅黑 11 bold")
        log_label.place(x=410, y=70, anchor="nw")
        self.log_area = scrolledtext.ScrolledText(window, width=57, height=10, font="微软雅黑 10")
        self.log_area.place(x=410, y=100, anchor="nw")
        self.logging("程序开始运行!\n")

        reporter_search_label = tkinter.Label(window, text="Reporters ID查询", font="微软雅黑 11 bold")
        reporter_search_label.place(x=410, y=295, anchor="nw")
        reporter_search_input_label = tkinter.Label(window, text="请输入国家/区域名称", font="微软雅黑 10 ")
        reporter_search_input_label.place(x=410, y=320, anchor="nw")
        reporter_search_result_label = tkinter.Label(window, text="结果", font="微软雅黑 10 ")
        reporter_search_result_label.place(x=600, y=320, anchor="nw")
        self.reporter_search_entry = tkinter.Entry(window, font="微软雅黑 9")
        self.reporter_search_entry.place(x=410, y=345, width=170, anchor="nw")
        self.reporter_result_text = scrolledtext.ScrolledText(window, width=45, height=6, font="微软雅黑 8")
        self.reporter_result_text.place(x=600, y=345)
        self.reporter_search_entry.bind("<Button-1>", lambda m=self, thread=self.reporter_search: threading_search(thread))
        self.reporter_result_text.insert(tkinter.END, "由于语言问题(如Reunion为法语的\"留尼汪岛\"),"
                                                      "若无结果请打开本工具目录下area_codes文件夹内的Reporters_code.json文件自行查找\n")

        partner_search_label = tkinter.Label(window, text="Partners ID查询", font="微软雅黑 11 bold")
        partner_search_label.place(x=410, y=420, anchor="nw")
        partner_search_input_label = tkinter.Label(window, text="请输入国家/区域名称", font="微软雅黑 10 ")
        partner_search_input_label.place(x=410, y=445, anchor="nw")
        partner_search_result_label = tkinter.Label(window, text="结果", font="微软雅黑 10 ")
        partner_search_result_label.place(x=600, y=445, anchor="nw")
        self.partner_search_entry = tkinter.Entry(window, font="微软雅黑 9")
        self.partner_search_entry.place(x=410, y=470, width=170, anchor="nw")
        self.partner_result_text = scrolledtext.ScrolledText(window, width=45, height=6, font="微软雅黑 8")
        self.partner_result_text.place(x=600, y=470)
        self.partner_search_entry.bind("<Button-1>", lambda m=self, thread=self.partner_search: threading_search(thread))
        self.partner_result_text.insert(tkinter.END, "由于语言问题(如Reunion为法语的\"留尼汪岛\"),"
                                        "若无结果请打开本工具目录下area_codes文件夹内的Partners_code.json文件自行查找\n")

        commodity_search_label = tkinter.Label(window, text="Commodity Codes查询", font="微软雅黑 11 bold")
        commodity_search_label.place(x=410, y=545, anchor="nw")
        commodity_search_input_label = tkinter.Label(window, text="请输入商品名称或ID", font="微软雅黑 10 ")
        commodity_search_input_label.place(x=410, y=570, anchor="nw")
        commodity_search_result_label = tkinter.Label(window, text="结果", font="微软雅黑 10 ")
        commodity_search_result_label.place(x=600, y=570, anchor="nw")
        self.commodity_search_entry = tkinter.Entry(window, font="微软雅黑 9")
        self.commodity_search_entry.place(x=410, y=595, width=170, anchor="nw")
        self.commodity_result_text = scrolledtext.ScrolledText(window, width=45, height=6, font="微软雅黑 8")
        self.commodity_result_text.place(x=600, y=595)
        self.commodity_search_entry.bind("<Button-1>", lambda m=self, thread=self.commodity_search: threading_search(thread))
        self.commodity_result_text.insert(tkinter.END, "由于语言问题(如Reunion为法语的\"留尼汪岛\"),"
                                          "若无结果请打开本工具目录下commodity_codes文件夹内的相应文件自行查找\n")

        window.mainloop()

    def threading_start(self):
        for i in range(50):
            thread = threading.Thread(target=self.encode)
            thread.start()

    # print log on log_area
    def logging(self, info):
        self.log_area.insert(tkinter.END, "<" + str(datetime.datetime.now().strftime("%X")) + "> " + info)
        self.log_area.see(tkinter.END)

    # return "type" to someone needs it
    def process_type(self):
        if "请选择:C=商品贸易/S=服务贸易" in self.type_combobox.get():
            self.logging("Type of Product为空!\n")
            return False
        else:
            return self.type_combobox.get()

    # return "frequency" to someone needs it
    def process_frequency(self):
        if "请选择:A=按年查询/M=按月查询" in self.frequency_combobox.get():
            self.logging("Frequency为空!\n")
            return False
        else:
            return self.frequency_combobox.get()

    # return "classification" to someone needs it
    def process_classification(self):
        if (self.classification_combobox.get() != "HS") \
                and (self.classification_combobox.get() != "H0") \
                and (self.classification_combobox.get() != "H1") \
                and (self.classification_combobox.get() != "H2") \
                and (self.classification_combobox.get() != "H3") \
                and (self.classification_combobox.get() != "H4") \
                and (self.classification_combobox.get() != "H5") \
                and (self.classification_combobox.get() != "ST") \
                and (self.classification_combobox.get() != "S1") \
                and (self.classification_combobox.get() != "S2") \
                and (self.classification_combobox.get() != "S3") \
                and (self.classification_combobox.get() != "S4") \
                and (self.classification_combobox.get() != "S5") \
                and (self.classification_combobox.get() != "BEC"):
            self.logging("Classification不正确!\n")
            return False
        else:
            return self.classification_combobox.get()

    # split "periods" every 5 item ,then append to "period_list" and return
    def process_period(self):
        if len(self.periods_entry.get()) == 0:
            self.logging("Periods为空!\n")
            return False
        # split periods&reporters&partners&codes
        periods_list = self.periods_entry.get().split(",")
        time_block_list = []
        # ----process and split periods
        # ----estimate the validity of periods_list
        if len(periods_list) != 2:
            self.logging("时间格式错误! 例子: \n单年份 : 2020,2020\n多年份 : 2020,2030\n单月份 : 202001,202001\n多月份 : 202001,202002\n")
        elif len(periods_list[0]) != len(periods_list[1]):
            self.logging("时间格式不一致! 例子: \n单年份 : 2020,2020\n多年份 : 2020,2030\n单月份 : 202001,202001\n多月份 : 202001,202002\n")
        elif int(periods_list[0]) > int(periods_list[1]):
            self.logging("起始时间大于结束时间!\n")

        # ----differ period_list's type
        else:
            start_time = int(periods_list[0])
            end_time = int(periods_list[1])

            # ----Year format
            if (len(periods_list[0]) == 4) and (len(periods_list[1]) == 4):

                # ----calculate time gap and cut it every 5 years
                if end_time - start_time != 0:
                    for i in range(start_time, end_time + 1, 5):
                        temp = []
                        for x in range(i, i + 5):
                            if x <= end_time:
                                temp.append(x)
                        time_block_list.append(temp)
                else:
                    time_block_list.append(start_time)

            # ------------Year + Month format
            elif (len(periods_list[0]) == 6) and (len(periods_list[1]) == 6):
                if (int(periods_list[0]) % 100 == 0) or (int(periods_list[1]) % 100 == 0):
                    self.logging("没有0月份!\n")
                    return
                elif (int(periods_list[0]) % 100 > 12) or (int(periods_list[1]) % 100 > 12):
                    self.logging("月份大于12月!\n")
                    return
                if end_time - start_time != 0:
                    for i in range(start_time, end_time + 1, 5):
                        month = i % 100
                        temp = []
                        if month <= 12:
                            for x in range(i, i + 5):
                                if (x % 100 <= 12) and x <= end_time:
                                    temp.append(x)
                            time_block_list.append(temp)
                else:
                    time_block_list.append(start_time)
            # ------------unknown format
            else:
                self.logging("未知时间格式!\n")
        return time_block_list

    # same as periods
    def process_reporters(self):
        if len(self.reporters_entry.get()) == 0:
            self.logging("Reporter为空!\n")
            return False
        reporter_split = self.reporters_entry.get().split(",")
        reproter_list = []
        for i in range(0, len(reporter_split), 5):
            temp = []
            for x in range(i, i + 5):
                if x < len(reporter_split):
                    temp.append(reporter_split[x])
            reproter_list.append(temp)
        return reproter_list

    # same as periods
    def process_partners(self):
        if len(self.partners_entry.get()) == 0:
            self.logging("Partners为空!\n")
            return False
        partner_split = self.partners_entry.get().split(",")
        partner_list = []
        for i in range(0, len(partner_split), 5):
            temp = []
            for x in range(i, i + 5):
                if x < len(partner_split):
                    temp.append(partner_split[x])
            partner_list.append(temp)
        return partner_list

    # just turn flows from "str" to "list"
    def process_flows(self):
        if len(self.flows_entry.get()) == 0:
            self.logging("Trade Flows为空!\n")
            return False
        flow_list = self.flows_entry.get().split(",")
        return flow_list

    # same as periods  but every 20 items
    def process_codes(self):
        if (len(self.codes_entry.get())) == 0:
            self.logging("HS Commodity Codes为空!\n")
            return False
        code_split = self.codes_entry.get().split(",")
        code_list = []
        for i in range(0, len(code_split), 20):
            temp = []
            for x in range(i, i + 20):
                if x < len(code_split):
                    temp.append(code_split[x])
            code_list.append(temp)
        return code_list

    # search
    def reporter_search(self):
        # event=None is must included! i haven't figure it out, more in http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
        # bind(event[or you can call it a key is pressed] , handler[or you can call it a callback function])
        # it seems that handler is called with an object(some codes) describing the event.
        # but in this function we don't need to describe the event so event=None .
        file = open("area_codes/Reporters_code.json", "r")
        dict_list = json.load(file)["results"]
        finish_flag = 0
        last_input = self.reporter_search_entry.get()
        while True:
            if finish_flag < 10:
                now_input = self.reporter_search_entry.get()
                if (len(now_input) == 0) or (len(now_input) < 3):
                    self.reporter_result_text.insert(tkinter.END, "长度过短!\n")
                    self.reporter_result_text.see(tkinter.END)
                    time.sleep(0.5)
                    continue
                # in case of unlimited loop,add a 2.5s period to judge whether user finish inputting
                if len(now_input) == len(last_input):
                    finish_flag = finish_flag + 1
                    time.sleep(0.5)
                elif len(now_input) != len(last_input):
                    last_input = now_input
                    finish_flag = 0
                    found_flag = 0
                    for item in dict_list:
                        if now_input.upper() in item["text"].upper():
                            found_flag = found_flag + 1
                            self.reporter_result_text.insert(tkinter.END, "_______________________________\n")
                            self.reporter_result_text.insert(tkinter.END,
                                                             "名称 : " + item["text"] + "\nID     : " + item["id"] + "\n")
                            self.reporter_result_text.see(tkinter.END)
                    if found_flag == 0:
                        self.reporter_result_text.insert(tkinter.END, "无匹配结果,请重试!\n")
                        self.reporter_result_text.see(tkinter.END)
                    time.sleep(0.5)
            else:
                self.reporter_result_text.insert(tkinter.END, "长时间未操作,请点击输入框重试\n")
                self.reporter_result_text.see(tkinter.END)
                break

    def partner_search(self):
        file = open("area_codes/Partners_code.json", "r")
        dict_list = json.load(file)["results"]
        finish_flag = 0
        last_input = self.partner_search_entry.get()
        while True:
            if finish_flag < 10:
                now_input = self.partner_search_entry.get()
                if (len(now_input) == 0) or (len(now_input) < 3):
                    self.partner_result_text.insert(tkinter.END, "长度过短!\n")
                    self.partner_result_text.see(tkinter.END)
                    time.sleep(0.5)
                    continue
                # in case of unlimited loop,add a 2.5s period to judge whether user finish inputting
                if len(now_input) == len(last_input):
                    finish_flag = finish_flag + 1
                    time.sleep(0.5)
                elif len(now_input) != len(last_input):
                    last_input = now_input
                    finish_flag = 0
                    found_flag = 0
                    for item in dict_list:
                        if now_input.upper() in item["text"].upper():
                            found_flag = 1
                            self.partner_result_text.insert(tkinter.END, "_______________________________\n")
                            self.partner_result_text.insert(tkinter.END,
                                                            "名称 : " + item["text"] + "\nID     : " + item["id"] + "\n")
                            self.partner_result_text.see(tkinter.END)
                    if found_flag == 0:
                        self.partner_result_text.insert(tkinter.END, "无匹配结果,请重试!\n")
                        self.partner_result_text.see(tkinter.END)
                    time.sleep(0.5)
            else:
                self.partner_result_text.insert(tkinter.END, "长时间未操作,请点击输入框重试\n")
                self.partner_result_text.see(tkinter.END)
                break

    def commodity_search(self):
        scheme = self.classification_combobox.get()
        if scheme == "HS":
            file = open("commodity_codes/HS_code.json", "r")
        elif scheme == "H0":
            file = open("commodity_codes/H0_code.json", "r")
        elif scheme == "H1":
            file = open("commodity_codes/H1_code.json", "r")
        elif scheme == "H2":
            file = open("commodity_codes/H2_code.json", "r")
        elif scheme == "H3":
            file = open("commodity_codes/H3_code.json", "r")
        elif scheme == "H4":
            file = open("commodity_codes/H4_code.json", "r")
        elif scheme == "H5":
            file = open("commodity_codes/H5_code.json", "r")
        elif scheme == "ST":
            file = open("commodity_codes/ST_code.json", "r")
        elif scheme == "S1":
            file = open("commodity_codes/S1_code.json", "r")
        elif scheme == "S2":
            file = open("commodity_codes/S2_code.json", "r")
        elif scheme == "S3":
            file = open("commodity_codes/S3_code.json", "r")
        elif scheme == "S4":
            file = open("commodity_codes/S4_code.json", "r")
        elif scheme == "BEC":
            file = open("commodity_codes/BEC_code.json", "r")
        else:
            self.commodity_result_text.insert(tkinter.END, "请选择正确的认证体系(Classification)\n")
            self.commodity_result_text.see(tkinter.END)
            return
        dict_list = json.load(file)["results"]
        finish_flag = 0
        last_input = self.commodity_search_entry.get()
        while True:
            if finish_flag < 10:
                now_input = self.commodity_search_entry.get()
                if (len(now_input) == 0) or (len(now_input) <= 3):
                    self.commodity_result_text.insert(tkinter.END, "长度过短!\n")
                    self.commodity_result_text.see(tkinter.END)
                    time.sleep(0.5)
                    continue

                # in case of unlimited loop,add a 2.5s period to judge whether user finish inputting
                if len(now_input) == len(last_input):
                    finish_flag = finish_flag + 1
                    time.sleep(0.5)
                elif len(now_input) != len(last_input):
                    last_input = now_input
                    finish_flag = 0
                    found_flag = 0
                    search_dict = dict_list
                    temp = []
                    for item in search_dict:
                        if now_input.upper() in item["text"].upper():
                            found_flag = 1
                            temp.append(item)
                            self.commodity_result_text.insert(tkinter.END, "_______________________________\n")
                            self.commodity_result_text.insert(tkinter.END,
                                                              "名称 : " + item["text"] + "\nID     : " + item["id"] + "\n")
                            self.commodity_result_text.see(tkinter.END)
                    if found_flag == 0:
                        self.commodity_result_text.insert(tkinter.END, "无匹配结果,请重试!\n")
                        self.commodity_result_text.see(tkinter.END)
                    search_dict = temp
                    time.sleep(0.5)
            else:
                self.commodity_result_text.insert(tkinter.END, "长时间未操作,请点击输入框重试\n")
                self.commodity_result_text.see(tkinter.END)
                break

    # encode every variable to URL Format("%2C" means "&") and start download
    # but api use both of these , "%2C" used inside a kind of variable , "&" used to connect variables
    def encode(self):
        self.mission_total = 0
        self.mission_finished = 0
        try:
            r_periods = self.process_period()
            r_reporters = self.process_reporters()
            r_partners = self.process_partners()
            r_flows = self.process_flows()
            r_codes = self.process_codes()
            url_type = self.process_type()
            url_freq = self.process_frequency()
            url_classification = self.process_classification()
            url_periods = []
            for each_period in r_periods:
                url = ""
                for year in each_period:
                    url = url + str(year) + "%2C"
                url = url[:-3]  # 2020%2C2021%2C2022
                url_periods.append(url)
            url_reporters = []
            for each_reporter in r_reporters:
                url = ""
                for reporter in each_reporter:
                    url = url + str(reporter) + "%2C"
                url = url[:-3]
                url_reporters.append(url)
            url_partners = []
            for each_partner in r_partners:
                url = ""
                for partner in each_partner:
                    url = url + str(partner) + "%2C"
                url = url[:-3]
                url_partners.append(url)
            url_flows = ""
            for flow in r_flows:
                url_flows = url_flows + str(flow) + "%2C"
            url_flows = url_flows[:-3]
            url_codes = []
            for each_code in r_codes:
                url = ""
                for code in each_code:
                    url = url + str(code) + "%2C"
                url = url[:-3]
                url_codes.append(url)
            # ----start downloading
            for each_period in url_periods:
                for each_reporter in url_reporters:
                    for each_partner in url_partners:
                        for each_code in url_codes:
                            self.mission_total = self.mission_total + 1
                            self.logging("\n_______________________________\n" +
                                         "正在下载 : " +
                                         "\nType of Product : " + url_type +
                                         " , Frequency : " + url_freq +
                                         " , Classification : " + url_classification +
                                         "\nPeriod : " + str(each_period).replace("%2C", "+") +
                                         "\nReporter : " + str(each_reporter).replace("%2C", "+") +
                                         "\nPartner : " + str(each_partner).replace("%2C", "+") +
                                         "\nTrade Flow :" + str(url_flows).replace("%2C", "+") +
                                         "\nCommodity Code : " + str(each_code).replace("%2C", "+") +
                                         "\n")
                            threading.Thread(target=self.download, args=(url_type, url_freq, url_classification, each_period, each_reporter,
                                             each_partner, url_flows, each_code)).start()
                            time.sleep(1)
            threading.Thread(target=self.check_finish).start()
        except Exception:
            self.logging("输入有误,请检查!\n")
            return

    # download csv
    def download(self, data_type, freq, classification, period, reporter, partner, flow, code):
        error_flag = 0
        api_url = "https://comtrade.un.org/api/get?" \
                  "r=" + reporter + \
                  "&px=" + classification + \
                  "&ps=" + period + \
                  "&p=" + partner + \
                  "&rg=" + flow + \
                  "&cc=" + code + \
                  "&max=100000" \
                  "&fmt=csv" \
                  "&type=" + data_type + \
                  "&freq=" + freq
        while error_flag <= 5:
            try:
                csv_data = requests.get(api_url).content
                file = open(
                    period.split("%2C")[0] + "-" + period.split("%2C")[-1] +
                    "年的Reporter为" +
                    reporter.split("%2C")[0] + "-" + reporter.split("%2C")[-1] + ",Partner为" +
                    partner.split("%2C")[0] + "-" + partner.split("%2C")[-1] + ",商品为" +
                    code.split("%2C")[0] + "-" + code.split("%2C")[-1] + ".csv", "wb")
                file.write(csv_data)
                self.mission_finished = self.mission_finished + 1
                break
            except Exception as e:
                self.logging(period.split("%2C")[0] + "-" + period.split("%2C")[-1] +
                             "年的Reporter为" +
                             reporter.split("%2C")[0] + "-" + reporter.split("%2C")[-1] + ",Partner为" +
                             partner.split("%2C")[0] + "-" + partner.split("%2C")[-1] + ",商品为" +
                             code.split("%2C")[0] + "-" + code.split("%2C")[-1] + ".csv文件下载出错,三秒后重试\n")
                time.sleep(3)
                error_flag = error_flag + 1
        if error_flag >= 5:
            self.logging("出错次数过多,已停止" + period.split("%2C")[0] + "-" + period.split("%2C")[-1] +
                         "年的Reporter为" +
                         reporter.split("%2C")[0] + "-" + reporter.split("%2C")[-1] + ",Partner为" +
                         partner.split("%2C")[0] + "-" + partner.split("%2C")[-1] + ",商品为" +
                         code.split("%2C")[0] + "-" + code.split("%2C")[-1] + ".csv文件下载,请检查网络连通性并自行重试\n")

    def check_finish(self):
        while True:
            if self.mission_finished == self.mission_total:
                self.logging("已全部下载完成!,文件保存在本工具同目录下\n")
                break
            else:
                time.sleep(0.5)
                continue


def threading_search(thread):
    threading.Thread(target=thread).start()


if __name__ == '__main__':
    download = Downloader()
