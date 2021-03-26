import io
import json


# a_dict = {1:'0001', 2: '002',3:'0.002'}
# print(list(a_dict.keys())) # key 列表
# print([list(a_dict.values()).index('002')]) # 对应的索引值
# print(list(a_dict.keys())[list(a_dict.values()).index('002')])
# print(len("0"))
# 结果
#[ 1, 2]
# [1]
# 2
# print(type("women"))

def get_standard_data(ori_data_file):
    dict_str = ""
    dict_list = []
    with io.open(ori_data_file,"r",encoding="utf-8") as f:
        for line in f:
            if "ObjectId" in line:
                line = line.replace("ObjectId","")
                line = line.replace("(","")
                line = line.replace(")", "")
            if "NumberInt(2020)" in line:
                line = line.replace("NumberInt(2020)","2020")
            dict_str = dict_str + line.strip()
            if len(line) < 4 and line.strip() == "}":
                dict_item = json.loads(dict_str)
                dict_list.append(dict_item)
                dict_str = ""
    return dict_list

def read_backup(input_file):
    data_list = []
    with io.open(input_file,"r",encoding="utf-8") as f:
        for line in f:
            line_list = line.split("\t")
            danhao = line_list[0]
            data_list.append(danhao)
    print(len(data_list))
    return data_list

def get_ori_data(data_list,dict_list):
    tmp_data_list = []
    for item in data_list:
        for dict_item in dict_list:
            if dict_item["danhao"] == item:
                tmp_data_list.append(dict_item)
                break
    return tmp_data_list

def get_temp_data():
    ori_data_file = "./data/Skn_spider_express_Update.json"
    dict_list = get_standard_data(ori_data_file)
    data_list = read_backup("./data/backup.txt")
    tmp_data_list = get_ori_data(data_list,dict_list)
    return tmp_data_list

def test_1():
    district= ["道县","三区"]
    district_item = district[0]
    tmp_district = district_item.replace("县", "").replace("区", "")
    if len(tmp_district) < 2:
        district.remove(district_item)
    print(district)

def rank_words():
    s_list = ['襄樊', '珠海']
    s = "快件离开 【珠海三部】 已发往 【襄樊中转】"
    s = s.replace("【","").replace("】",'').replace(" ","")
    print(s)
    tmp_list = []
    ss_list = []
    for item in s_list:
        tmp_index = s.find(item)
        tmp_list.append(tmp_index)
    s_dict = {}
    for i in range(len(s_list)):
        s_dict[s_list[i]] = tmp_list[i]
    s_dict_ = sorted(s_dict.items(), key=lambda item:item[1],reverse=True)
    print(s_dict_)
    for item in s_dict_:
        ss_list.append(item[0])
    print(ss_list)


# rank_words()