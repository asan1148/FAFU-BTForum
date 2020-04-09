import requests
import colored
import datetime
import json
url = "API_URL"


def get_info():
    html = requests.get(url).text
    json_dict = json.loads(html)
    return json_dict


if __name__ == '__main__':
    base_info = get_info()
    print("Total : " + "{}%s{}".format(colored.fg(11), colored.attr(0)) % str(len(base_info)) + " records, sorted by upload time")
    download_list = []
    seq = 0
    write_file = open("%s Past Stream URL.txt" % (datetime.datetime.now().strftime("%F")), "w")
    for item in base_info:
        contentId = item['contentId']
        title = item['title']
        title = title.replace("/", "-")
        title = title.replace("\\", "-")
        title = title.replace(":", "-")
        title = title.replace("*", "-")
        title = title.replace("?", "-")
        title = title.replace("\"", "-")
        title = title.replace("<", "-")
        title = title.replace(">", "-")
        title = title.replace("|", "-")
        duration = round(item['durationInSeconds'] / 60, 2)
        download_link = item['contentLocators'][1]['uri']
        upload_time = item['uploadDate']
        upload_time = upload_time.split(".")[0]
        upload_time = upload_time.replace("T", " ")
        upload_time = upload_time.replace("Z", " ")
        upload_time = upload_time.replace(":", ".")
        file_info = (contentId, title, upload_time, duration, download_link)
        download_list.append(file_info)
        print("+----------------------------------------------------------------------+")
        print("Seq : " + str(seq))
        seq += 1
        print("{}Title : {}".format(colored.fg(1), colored.attr(0)) + title)
        print("{}Upload Time : {}".format(colored.fg(11), colored.attr(0)) + upload_time)
        print("{}Download Link : {}".format(colored.fg(5), colored.attr(0)) + download_link)
        print("File name : " + title + upload_time)
        write_file.write("+----------------------------------------------------------------------+")
        write_file.write(str(seq) + "\n")
        write_file.write(str(title) + "\n")
        write_file.write(str(upload_time) + "\n")
        write_file.write(str(download_link) + "\n")
    write_file.close()
    input("\n\nFinished . The URLs are output to txt , press ENTER to exit")


