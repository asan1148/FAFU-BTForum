import json
import colored
import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


def check_mixer():
    print("正在检测主播是否有在直播")
    while True:
        command = os.popen("get_stream_url.bat")
        result = command.read()
        command.close()
        if "No playable streams found on this URL" in result:
            print("并未直播,10秒后重试")
            stream_url = ""
            streaming_flag = 0
            time.sleep(10)
            continue
        else:
            print("正在直播,准备转播")
            stream_url = result.split("\n")[-2]
            streaming_flag = 1
            break
    return streaming_flag, stream_url


def re_cast(browser, stream_url):
    print("正在开启直播间并获取rtmp推流地址")
    room_setting_url = "https://link.bilibili.com/p/center/index#/my-room/start-live"
    browser.get(room_setting_url)
    time.sleep(3)
    select_class = browser.find_element_by_xpath(
        "/html/body/div[1]/main/div/div[1]/div[2]/div/div[1]/section/div/div[1]/div[1]/a")
    select_class.click()
    time.sleep(1)
    single_player = browser.find_element_by_xpath(
        "/html/body/div[1]/main/div/div[1]/div[2]/div/div[1]/section/div/div[1]/div[2]/div[2]/div/ul/li[3]/a")
    single_player.click()
    time.sleep(1)
    search_input = browser.find_element_by_xpath(
        "/html/body/div[1]/main/div/div[1]/div[2]/div/div[1]/section/div/div[1]/div[2]/div[2]/div/input")
    search_input.send_keys("其他单机")
    time.sleep(1)
    other_single_game = browser.find_element_by_xpath(
        "/html/body/div[1]/main/div/div[1]/div[2]/div/div[1]/section/div/div[1]/div[2]/div[2]/div/div/div[1]/div/a")
    browser.execute_script("arguments[0].click();", other_single_game)
    time.sleep(1)
    start_stream = browser.find_element_by_xpath(
        "/html/body/div[1]/main/div/div[1]/div[2]/div/div[1]/section/div/div[4]/button")
    start_stream.click()
    time.sleep(1)
    rtmp_address = browser.find_element_by_xpath(
        "/html/body/div[1]/main/div/div[1]/div[2]/div/div[1]/section/div/div[3]/div[1]/div[1]/button").get_attribute(
        "data-clipboard-text")
    rtmp_code = browser.find_element_by_xpath(
        "/html/body/div[1]/main/div/div[1]/div[2]/div/div[1]/section/div/div[3]/div[1]/div[2]/button").get_attribute(
        "data-clipboard-text")
    rtmp_url = rtmp_address + rtmp_code
    time.sleep(1)
    print("已获取RTMP推流地址,正在开始推流")
    print(stream_url)
    print(rtmp_url)
    file = open("ffmpeg_setting.bat", "w")
    file.write("set http_proxy=http://127.0.0.1:1099\n"
               "ffmpeg -http_proxy %http_proxy% -i \"" + stream_url + "\" -c copy -f flv \"" + rtmp_url + "\"\n"
                                                                                                              "echo 已转播结束,可以关闭本程序\npause")
    file.close()
    offline_flag = 0
    while True:
        if offline_flag == 1:
            break
        start_cast_cmd = os.popen("ffmpeg_setting.bat")
        cast_result = start_cast_cmd.read()
        if "Error" in cast_result:
            print("网络卡了或主播已下播,请自行检查,若已下播,请手动关闭本程序")
            offline_flag = 1
            print("正在重启转播")
            time.sleep(2)
            continue


def auto_login():
    print("正在自动登陆中...")
    old_cookies_file = open("cookies.json", "r")
    json_cookie = json.loads(old_cookies_file.read())
    old_cookies_file.close()
    home_page_url = "https://bilibili.com"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(home_page_url)
    for cookie in json_cookie:
        if "expiry" in cookie:
            cookie["expiry"] = int(cookie["expiry"])
        browser.add_cookie(cookie)
    browser.get(home_page_url)
    new_cookies = browser.get_cookies()
    json_cookies = json.dumps(new_cookies)
    new_cookies_file = open("cookies.json", "w")
    new_cookies_file.write(json_cookies)
    new_cookies_file.close()
    try:
        if_sucess = browser.find_element_by_xpath(
            "/html/body/div[2]/div/div[1]/div[1]/div/div[3]/div[2]/div[3]/div/div[1]/a/span")
        print("登陆成功!")
    except NoSuchElementException:
        print("{}登录失败,正在重试中,若失败多次请删除本工具目录下cookies.json文件{}".format(colored.fg(1), colored.attr(0)))
        check_cookie()
    flag, url = check_mixer()
    if flag == 1:
        re_cast(browser, url)


def manually_login():
    login_url = "https://passport.bilibili.com/login"
    input("{}请按回车键开始手动登录,并在登录成功后返回本程序,按照提示进行下一步操作{}".format(colored.fg(5), colored.attr(0)))
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(login_url)
    input("{}若已完成手动登录,并已自动跳转到B站首页,请按回车键进行下一步{}".format(colored.fg(5), colored.attr(0)))
    cookies = browser.get_cookies()
    json_cookies = json.dumps(cookies)
    cookie_file = open("cookies.json", "w")
    cookie_file.write(json_cookies)
    cookie_file.close()
    browser.close()
    check_cookie()


def check_cookie():
    try:
        open("cookies.json", "r")
        auto_login()
    except FileNotFoundError:
        print("{}缺少登录必要文件,请按照接下来的提示手动登录一次{}".format(colored.fg(1), colored.attr(0)))
        manually_login()


if __name__ == '__main__':
    print("{}欢迎使用工具man转播工具!{}".format(colored.fg(11), colored.attr(0)))
    check_cookie()
    input("转播已停止,如有需要请再次打开程序")