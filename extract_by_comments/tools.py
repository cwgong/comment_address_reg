#!/usr/bin/env python3
#coding=utf-8

import openpyxl
import re
from pymongo import MongoClient
import io
# from LAC import LAC

def remove_company(company_list,sen):
    sen = sen.lower()
    for company_item in company_list:
        if len(sen.split(company_item)) > 1:
            sen = sen.replace(company_item,"")
    return sen

def read_company(company_file):
    company_list = []
    with io.open(company_file, "r", encoding="utf-8") as f1:
        for line in f1:
            company_list.append(line.strip().lower())
    return company_list


def loading_data_baidu(input_file):
    complain_data_list = []
    with io.open(input_file, "r", encoding="utf-8") as f1:
        for line in f1:
            tmp_dict = {}
            if line == "": continue
            line_list = line.split("\t")
            print(len(line))
            if len(line_list) != 8: continue
            complain_id = line_list[0].strip()
            complain_company = line_list[2].strip()
            complain_data = line_list[3].strip()
            if len(complain_id) > 0:
                tmp_dict["complain_id"] = complain_id
                tmp_dict["complain_data"] = complain_data
                tmp_dict["complain_company"] = complain_company
                complain_data_list.append(tmp_dict)
    return complain_data_list


def loading_data_ext(input_file):
    complain_data_list = []
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            tmp_dict = {}
            if line == "":continue
            line_list = line.split("\t")
            if len(line_list) != 4:continue
            complain_id = line_list[0].strip()
            complain_data = line_list[1].strip()
            complain_problem = line_list[2].strip()
            complain_company = line_list[2].strip()
            if len(complain_id) > 0:
                tmp_dict["complain_id"] = complain_id
                tmp_dict["complain_data"] = complain_data
                tmp_dict["complain_problem"] = complain_problem
                tmp_dict["complain_company"] = complain_company
                complain_data_list.append(tmp_dict)
    return complain_data_list

def get_company(complain_data_list):
    company_dict = {}
    for complain_data in complain_data_list:
        complain_company = complain_data['complain_company']
        complain_company_list = complain_company.split(",")
        for complain_company_item in complain_company_list:
            complain_company_item = complain_company_item.strip()
            if complain_company_item not in company_dict:
                company_dict[complain_company_item] = 1
            else:
                company_dict[complain_company_item] = company_dict[complain_company_item] + 1
    company_list = list(company_dict.keys())
    with io.open("./data/company_data.txt","w",encoding="utf-8") as f1:
        f1.write("\n".join(company_list))
        f1.flush()


def loading_education_data(input_file):
    complain_data_list = []
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            tmp_dict = {}
            if line == "":continue
            line_list = line.strip().split("\t")
            if len(line_list) != 8:continue
            complain_id = line_list[0].strip()
            complain_company = line_list[2].strip()
            complain_data = line_list[3].strip()
            complain_problem_ori = line_list[4].strip()
            complain_problem = line_list[6].strip()
            if len(complain_id) > 0 :
                tmp_dict['complain_id'] = complain_id
                tmp_dict['complain_company'] = complain_company
                tmp_dict['complain_data'] = complain_data
                tmp_dict['complain_problem_ori'] = complain_problem_ori
                tmp_dict['complain_problem'] = complain_problem
                complain_data_list.append(tmp_dict)
    return complain_data_list


def removePunctuation(text):
    punctuation = '\！\，\；\：\？\。!,;:?".'
    text = re.sub(r'[{}]+'.format(punctuation), '。', text)
    return text.strip().lower()
"""
mongo -> fw_spider -> tousu_sina_msg_list
mongo -> fw_spider -> tousu_sina_msg_info
"""

def text_clean(text):
    text = text.strip()
    text = text.replace("\t", " ") \
            .replace("\n", " ") \
            .replace("\r;", "") \


    text = re.sub(r"[\s]+", " ", text)

    return text

def loading_data_by_mongo():
    client = MongoClient(host='mongodb://spider:spidermining@172.20.207.10:27051,172.20.207.12:27051,172.20.207.13:27051/admin',document_class=dict, tz_aware=True)
    db = client.fw_spider
    results = db['tousu_sina_msg_info'].find({})
    idx = 0

    r_lst = ["id\task\ttitle\trequire"]

    for j_data in results:
        idx += 1
        print(j_data)
        if idx % 1000 == 0: print("idx: %s" % idx)
        if "_id" not in j_data: continue
        _id = j_data["_id"]
        c = ""
        if "ask" in j_data:
            c = text_clean(j_data["ask"])
        else:
            print("ask is empty!")
        t = ""
        if "title" in j_data:
            t = text_clean(j_data["title"])
        else:
            print("title is empty!")
        r = ""
        if "require" in j_data:
            r =  text_clean(j_data["require"])


        #r_lst.append("%s\001%s\001%s" %(_id, c, t))
        r_lst.append("%s\t%s\t%s\t%s" % (_id, c, t, r))
        print(r_lst)



    with open("./data/tousu_info.txt", "w",encoding="utf-8") as f2:
        f2.write("\n".join(r_lst))
        f2.flush()


# def complain_data_seg(complain_data_list):
#     lac = LAC(mode="seg")
#     words_dict = {}
#     words_list = []
#     for complain_data in complain_data_list:
#         seg_result = lac.run(complain_data['complain_data'])
#         for seg_word in seg_result:
#             if seg_word not in words_dict:
#                 words_dict[seg_word] = 1
#             else:
#                 words_dict[seg_word] = words_dict[seg_word] + 1
#     if words_dict != {}:
#         words_list = [(k,v) for k,v in words_dict.items()]
#     words_list = sorted(words_list,key=lambda x:x[1],reverse=True)
#     return words_list


def struct_complain_data_baidu(input_file_ext,company_list):
    sen_dict = {}
    ori_data_list = []
    sen_list = []

    for complain_data_ext in input_file_ext:
        complain_sen_ext = complain_data_ext['complain_data']
        complain_sen_ext = remove_company(company_list,complain_sen_ext)
        complain_sen_ext = "。".join([complain_sen_ext])
        complain_sen_ext_ = removePunctuation(complain_sen_ext)
        complain_sen_ext_list = complain_sen_ext_.split("。")
        ori_data_list = ori_data_list + complain_sen_ext_list

    # with io.open("./data/test_data.txt","w",encoding="utf-8") as f2:
    #     f2.write("。".join(ori_data_list))

    for item_sen in ori_data_list:
        if len(item_sen) <= 10:
            if item_sen not in sen_dict:
                sen_dict[item_sen] = 1
            else:
                sen_dict[item_sen] = sen_dict[item_sen] + 1
    if sen_dict != {}:
        sen_list = [(k,v) for k,v in sen_dict.items()]
    sen_list = sorted(sen_list,key=lambda x:x[1],reverse=True)
    return sen_list


if __name__ == "__main__":
    # loading_data_by_mongo()
    input_file = "./data/baidu.txt"
    company_file = "./data/company_data.txt"
    # complain_data_list = loading_education_data(input_file)
    # get_company(complain_data_list)
    data_list = loading_data_baidu(input_file)
    # word_list = complain_data_seg(data_list)
    company_list = read_company(company_file)
    sen_list = struct_complain_data_baidu(data_list,company_list)
    with io.open("./data/sen_baidu_data_problem.txt", "w", encoding="utf-8") as f1:
        for seg_word in sen_list:
            f1.write(str(seg_word) + "\n")