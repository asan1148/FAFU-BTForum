import os
import colored


def remove_blank(file_name):
    print("{}Removing blank line in case BiliBili can't recognize...{}".format(colored.fg(5), colored.attr(0)))
    raw_sub_file = open(file_name, "r")
    temp_content = ""
    for line in raw_sub_file.readlines():
        if len(line) == 0:
            continue
        elif line == "\n":
            continue
        elif line == " \n":
            continue
        else:
            temp_content = temp_content + line
    raw_sub_file.close()
    write_sub_file = open(file_name, "w")
    write_sub_file.write(temp_content)
    write_sub_file.close()


def add_zero(var):
    if len(var) == 1:
        var = "0" + var
    return var


def remove_unnecessary_part(file_name):
    while True:
        if_remove = input("Would you like to remove some un-necessary parts of subtitle ? Y/N").upper()
        if if_remove == "Y":
            print("Preparing to remove...")
            break
        elif if_remove == "N":
            print("We won't remove anything")
            return
        else:
            print("{}Wrong input , try again{}".format(colored.fg(1), colored.attr(0)))
            continue
    while True:
        start_hour = input("Please input start-time's hour : ")
        start_min = input("Please input start-time's min : ")
        start_sec = input("Please input start-time's sec : ")
        start_million_sec = input("Please input start-time's million sec : ")
        end_hour = input("Please input end-time's hour : ")
        end_min = input("Please input end-time's min : ")
        end_sec = input("Please input end-time's sec : ")
        end_million_sec = input("Please input end-time's million sec : ")
        try:
            int(start_hour)
            int(start_min)
            int(start_sec)
            int(start_million_sec)
            int(end_hour)
            int(end_min)
            int(end_sec)
            int(end_million_sec)
            break
        except ValueError:
            start_hour = None
            start_min = None
            start_sec = None
            start_million_sec = None
            end_hour = None
            end_min = None
            end_sec = None
            end_million_sec = None
            print("{}Wrong input, try again!{}".format(colored.fg(1), colored.attr(0)))
            continue
    print("{}Removing unnecessary part...{}".format(colored.fg(5), colored.attr(0)))
    start_hour = add_zero(start_hour)
    start_min = add_zero(start_min)
    start_sec = add_zero(start_sec)
    start_million_sec = add_zero(start_million_sec)
    end_hour = add_zero(end_hour)
    end_min = add_zero(end_min)
    end_sec = add_zero(end_sec)
    end_million_sec = add_zero(end_million_sec)
    start_time = "%s:%s:%s,%s" % (str(start_hour), str(start_min), str(start_sec), str(start_million_sec))
    end_time = "%s:%s:%s,%s" % (str(end_hour), str(end_min), str(end_sec), str(end_million_sec))
    raw_sub_file = open(file_name, "r")
    raw_content = raw_sub_file.read()
    raw_sub_file.close()
    split_list = raw_content.split("\n")
    start_index = 0
    end_index = 0
    # get start index
    for index in range(len(split_list)):
        if start_time in split_list[index]:
            time_axis = split_list[index]
            start_axis = time_axis.split(" --> ")[0]
            end_axis = time_axis.split(" --> ")[1]
            if start_axis == start_time:
                start_index = index - 1
            elif end_axis == start_time:
                continue
            else:
                continue
            break
        else:
            continue
    # get basic end index
    for index in range(len(split_list)):
        if end_time in split_list[index]:
            time_axis = split_list[index]
            start_axis = time_axis.split(" --> ")[0]
            end_axis = time_axis.split(" --> ")[1]
            if start_axis == end_time:
                end_index = index - 1
            elif end_axis == end_time:
                continue
            else:
                continue
            break
        else:
            continue
    # get final end index
    for index in range(end_index, len(split_list)):
        if index == end_index:
            continue
        else:
            try:
                int(split_list[index])
                end_index = index - 1
                break
            except ValueError:
                continue
    head_content = ""
    for sentence in split_list[0:start_index]:
        head_content = head_content + sentence + "\n"
    tail_content = ""
    for sentence in split_list[end_index + 1:]:
        tail_content = tail_content + sentence + "\n"
    cut_content = head_content + tail_content
    cut_content = cut_content.strip()
    open(file_name, "w").write(cut_content)


def translate_sub(file_name, content):
    while True:
        if_translate = input("Would you like to translate the subtitle right now ? Y/N").upper()
        if if_translate == "Y":
            print("{}Perparing to translate...{}".format(colored.fg(5), colored.attr(0)))
            break
        elif if_translate == "N":
            print("Got it , Process is complete , thanks for using this tool...")
            print("Press Enter to exit the program")
            exit(0)
        else:
            print("{}Please input 'Y' or 'N'")
            continue
    raw_content = content
    translated_content = []
    for current_index in range(len(raw_content)):
        row_sentence = ""
        current_time_axis = raw_content[current_index][0]
        print("---------------------------------------------------------------------")
        print("{}Current Time : {}".format(colored.fg(11), colored.attr(0)) + current_time_axis)
        for sentence in raw_content[current_index][1]:
            row_sentence = row_sentence + sentence
        print("{}Raw Sentence : {}".format(colored.fg(6), colored.attr(0)) + row_sentence)
        print("{}Next 5 sentences are : {}".format(colored.fg(12), colored.attr(0)))
        for forward_index in range(5):
            if current_index + forward_index > len(content) - 1:
                print("")
            else:
                for sentence in content[current_index + forward_index][1]:
                    print(sentence)
        print("---------------------------------------------------------------------")

        translation = input("Please enter your translation : ").encode("utf-8")
        if len(translation) == 0:
            translation = row_sentence
        translated_block = [current_time_axis, translation]
        translated_content.append(translated_block)
    write_file = open(file_name, "w", encoding="utf-8")
    block_seq = 1
    for block in translated_content:
        final_time_axis = block[0]
        final_sentence = block[1]
        write_file.write(str(block_seq) + "\n")
        write_file.write(final_time_axis)
        write_file.write(final_sentence.decode("utf-8"))
        block_seq += 1
    write_file.close()


def restructure_sub(file_name):
    print("{}Restructuring subtitle...{}".format(colored.fg(5), colored.attr(0)))
    raw_file = open(file_name, "r")
    raw_content = raw_file.read()
    raw_file.close()
    split_content = raw_content.split("\n")
    un_duplicate_content_list = []
    content_block_list = []
    temp_block = []

    # turn every dialog to a block
    for index in range(len(split_content)):
        try:
            int(split_content[index])
            if len(temp_block) == 0:
                continue
            else:
                content_block_list.append(temp_block)
            temp_block = []
        except ValueError:
            temp_block.append(split_content[index])
    content_block_list.append(temp_block)

    # start check duplication
    # loop to find any duplicated sentence , and try to fix the time axis and the dialog
    finish_flag = 0
    while True:
        if finish_flag == 1:
            break
        duplication_flag = 0
        # get current block's info
        for current_index in range(len(content_block_list)):
            if duplication_flag == 1:
                break
            current_block = content_block_list[current_index]
            current_time_axis = current_block[0]
            current_start_time = current_time_axis.split(" --> ")[0]
            current_sentences = current_block[1:]
            # get next block's info
            for forward_index in range(current_index + 1, len(content_block_list)):
                if forward_index > len(content_block_list) - 1:
                    break
                forward_block = content_block_list[forward_index]
                forward_time_axis = forward_block[0]
                forward_end_time = forward_time_axis.split(" --> ")[1]
                forward_sentences = forward_block[1:]
                # start to compare if there is a duplication
                for current_sentence in current_sentences:
                    # if we found a duplicated block
                    if current_sentence in forward_sentences:
                        # if next block's sentence is single line (means it's a transition dialog)
                        # we need to delete this block
                        if len(forward_sentences) == 1:
                            un_duplicate_time_axis = current_start_time + " --> " + forward_end_time
                            un_duplicate_sentences = current_sentences
                            temp_un_duplicated_block = [un_duplicate_time_axis, un_duplicate_sentences]
                            un_duplicate_content_list.append(temp_un_duplicated_block)
                            duplication_flag = 1
                            del content_block_list[forward_index]
                            break
                        # if next block's sentence is double line (means its a dialog that it's no a transition dialog)
                        # we just need to delete the transition sentence in the double line dialog
                        else:
                            del content_block_list[forward_index][1]
                            duplication_flag = 1
                            break
                    # if we didn't found a duplicated block
                    else:
                        continue
            if current_index == len(content_block_list) - 1:
                finish_flag = 1
                temp_un_duplicated_block = [content_block_list[current_index][0], content_block_list[current_index][1:]]
                un_duplicate_content_list.append(temp_un_duplicated_block)
    write_file = open(file_name, "w")
    block_seq = 1
    for block in un_duplicate_content_list:
        final_time_axis = block[0] + "\n"
        final_sentences = ""
        for sentence in block[1]:
            final_sentences = final_sentences + sentence + "\n"
        write_file.write(str(block_seq) + "\n")
        write_file.write(str(final_time_axis) + "\n")
        write_file.write(str(final_sentences) + "\n")
        block_seq += 1
    write_file.close()
    translate_sub(file_name, un_duplicate_content_list)


def get_all_file():
    print("{}Getting all the vtt files...{}".format(colored.fg(5), colored.attr(0)))
    path = os.getcwd()
    file_list = os.listdir(path)
    vtt_list = []
    for file_name in file_list:
        file_extension = file_name.split(".")[-1]
        if file_extension == "vtt":
            vtt_list.append(file_name)
    return vtt_list


def reformat_sub(file_name):
    print("{}Reformatting file from vtt to srt , please wait...{}".format(colored.fg(5), colored.attr(0)))
    old_file_name = file_name
    new_file_name = file_name.replace("vtt", "srt")
    os.system("ffmpeg -i \"%s\" \"%s\"" % (old_file_name, new_file_name))
    os.system("del \"%s\"" % old_file_name)
    return new_file_name


if __name__ == '__main__':
    print("{}Thanks for using my Youtube auto-generate subtitle restruction tool{}".format(colored.fg(11), colored.attr(0)))
    sub_list = get_all_file()
    file_counter = 0
    for sub in sub_list:
        print("---------------------------------------------------------------------------------")
        print("%d : " % file_counter + sub)
        file_counter += 1
    while True:
        try:
            file_selector = int(input("Please select which subtitle you want to edit : "))
            select_confirm = input(
                "Your selection is : %d : %s\nIs that correct ?  Y/N" % (file_selector, sub_list[file_selector])).upper()
            if select_confirm == "Y":
                print("Processing...")
                break
            elif select_confirm == "N":
                print("Please try again ...")
                continue
            else:
                print("{}Please input 'Y' or 'N' ! ")
                continue
        except ValueError:
            file_selector = 0
            print("{}Please enter a number ! {}".format(colored.fg(11), colored.attr(0)))
            continue
    srt_file_name = reformat_sub(sub_list[file_selector])
    remove_blank(srt_file_name)
    remove_unnecessary_part(srt_file_name)
    restructure_sub(srt_file_name)
