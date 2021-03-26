# -!- coding: utf-8 -!-

import io
import json
import struct_address
import time
import multiprocessing
import temp

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



def duplicate_data(data_list):
    tmp_dict = {}
    for item in data_list:
        tmp_dict[item['danhao']] = item
    data_list_duplicate = list(tmp_dict.values())
    return data_list_duplicate


def add_addr_data(data_list,addr_list_province, addr_list_city, addr_list_district):
    flag = 0
    for item_data in data_list:
        flag += 1
        addr_data_list = item_data['data']
        for addr_data in addr_data_list:
            addr_loc = ""
            if "location" in addr_data:
                addr_loc = addr_data['location']
            addr_context = addr_data['context']     #取到那一句数据
            province_list = []
            city_list = []
            district_list = []
            tmp_dict = {}
            # for addr_province in addr_list_province:
            #     if type(addr_loc) != "str":
            #         break
            #     if addr_province['addr_name'].replace("省","") in addr_loc.replace("省",""):
            #         province_list.append(addr_province['addr_name'])
            #     else:
            #         continue
            # if len(province_list) == 0:
            #     for addr_province in addr_list_province:    #遍历省的那一个list
            #         if addr_province['addr_name'].replace("省","") in addr_context.replace("省",""):       #判断那个省是否在context当中
            #             province_list.append(addr_province['addr_name']) #如果在的话加入这个context的省list当中
            #         else:
            #             continue
            # tmp_dict['province'] = province_list

            # for addr_city in addr_list_city:
            #     if type(addr_loc) != "str":
            #         break
            #     if addr_city['addr_name'].replace("市","") in addr_loc.replace("市",""):
            #         city_list.append(addr_city['addr_name'])
            #     else:
            #         continue
            if len(city_list) == 0:
                for addr_city in addr_list_city:
                    if addr_city['addr_name'].replace("市","") in addr_context.replace("市","").replace("（广东广州号）",""):
                        city_list.append(addr_city['addr_name'])
                    else:
                        continue
            tmp_dict['city'] = city_list

            # for addr_district in addr_list_district:
            #     if type(addr_loc) != "str":
            #         break
            #     if addr_district['addr_name'].replace("县","").replace("区","").replace("市","") in addr_loc.replace("县","").replace("区","").replace("市",""):
            #         district_list.append(addr_district['addr_name'])
            #     else:
            #         continue
            if len(district_list) == 0:
                for addr_district in addr_list_district:
                    if addr_district['addr_name'].replace("县","").replace("区","").replace("市","") in addr_context.replace("县","").replace("区","").replace("市",""):
                        district_list.append(addr_district['addr_name'])
                    else:
                        continue
            tmp_dict['district'] = district_list
            addr_data["address"] = tmp_dict
            if flag < 5:
                print(addr_data)
        if flag%500 == 0:
            print(flag)
    return data_list

def rank_words(s_list,s):
    tmp_list = []
    ss_list = []
    for item in s_list:
        item = item.replace("市","").replace("县","").replace("省","").replace("区","")
        tmp_index = s.find(item)
        tmp_list.append(tmp_index)
    s_dict = {}
    for i in range(len(s_list)):
        s_dict[s_list[i]] = tmp_list[i]
    s_dict_ = sorted(s_dict.items(), key=lambda item:item[1],reverse=False)
    # print(s_dict_)
    for item in s_dict_:
        ss_list.append(item[0])
    return ss_list

def rank_words_reverse(s_list,s):
    tmp_list = []
    ss_list = []
    for item in s_list:
        item = item.replace("市", "").replace("县", "").replace("省", "").replace("区", "")
        tmp_index = s.find(item)
        tmp_list.append(tmp_index)
    s_dict = {}
    for i in range(len(s_list)):
        s_dict[s_list[i]] = tmp_list[i]
    s_dict_ = sorted(s_dict.items(), key=lambda item:item[1],reverse=True)
    # print(s_dict_)
    for item in s_dict_:
        ss_list.append(item[0])
    return ss_list


def match_addr_district(update_file,addr_list_city_nest,addr_list_province_nest):
    flag_ = 0
    flag = 0
    flag_1 = 0
    flag_2 = 0
    flag_3 = 0
    flag_4 = 0
    simple_result_list = []
    with io.open(update_file,"r",encoding="utf-8") as f:
        data_list_update = json.load(f)
    f1 = io.open("./data/tmp_result_district.txt", "w", encoding="utf-8")
    f2 = io.open("./data/result_district_11.txt", "w", encoding="utf-8")
    f3 = io.open("./data/result_district_22.txt", "w", encoding="utf-8")
    f4 = io.open("./data/result_district_33.txt", "w", encoding="utf-8")
    for item_dict in data_list_update:
        flag += 1
        item_data = item_dict['data']
        idx_to = 0
        idx = 0
        city_name_to = ""
        province_name_to = ""
        district_name_to = ""
        city_name = ""
        province_name = ""
        district_name = ""
        tmp_dict = {}
        start_string = ""
        end_string = ""
        tmp_dict['status'] = -1
        tmp_dict['length'] = len(item_data)
        tmp_dict['company'] = item_dict['name_str']
        tmp_dict['start_time'] = ""
        tmp_dict['end_time'] = ""
        #找到收件地址
        for data_info in item_data:
            idx_to = idx_to + 1
            # if len(data_info["address"]["district"]) == 0:
            #     continue
            # print(data_info["address"]["district"])
            # for district_item in data_info["address"]["district"]:
            #     tmp_district = district_item.replace("县", "").replace("区", "")
            #     if len(tmp_district) < 2:
            #         data_info["address"]["district"].remove(district_item)
            for i in range(len(data_info["address"]["district"]) - 1, -1, -1):
                tmp_district = data_info["address"]["district"][i].replace("县", "").replace("区", "").replace("市","")
                if len(tmp_district) < 2:
                    data_info["address"]["district"].remove(data_info["address"]["district"][i])
            # print(data_info["address"]["district"])
            if len(data_info["address"]["district"]) > 0:
                data_info["address"]["district"] = rank_words_reverse(data_info["address"]["district"],data_info['context'])
                for district in data_info["address"]["district"]:
                    for city_nest in addr_list_city_nest:
                        for district_item in city_nest["district_item"]:
                            if district == district_item['addr_name']:
                                district_name_to = district
                                city_name_to = city_nest['district']
                                tmp_dict['end_time'] = data_info['time']
                                end_string = data_info['context']
                                break
                        if city_name_to != "":
                            break
                    for province_nest in addr_list_province_nest:
                        for city_item in province_nest['city_item']:
                            if city_name_to == city_item['addr_name']:
                                province_name_to = province_nest['city']
                                break
                        if province_name_to != "":
                            break
                    if city_name_to != '' and province_name_to != '':
                        break
                if city_name_to != '' and province_name_to != '':
                    break
            else:
                data_info["address"]["city"] = rank_words_reverse(data_info["address"]["city"], data_info['context'])
                for city in data_info["address"]["city"]:
                    for province_nest in addr_list_province_nest:
                        for city_item in province_nest["city_item"]:
                            if city == city_item['addr_name']:
                                city_name_to = city
                                province_name_to = province_nest['city']
                                tmp_dict['end_time'] = data_info['time']
                                end_string = data_info['context']
                                break
                        if province_name_to != "":
                            break
                    if province_name_to != '':
                        break
                if province_name_to != '':
                    break

        #找寄件地址
        for data_info in reversed(item_data):
            idx = idx + 1
            if idx + idx_to >= len(item_data):
                break
            # if len(data_info["address"]["district"]) == 0:
            #     continue
            # for district_item in data_info["address"]["district"]:
            #     tmp_district = district_item.replace("县", "").replace("区", "")
            #     if len(tmp_district) < 2:
            #         data_info["address"]["district"].remove(district_item)
            for i in range(len(data_info["address"]["district"]) - 1, -1, -1):
                tmp_district = data_info["address"]["district"][i].replace("县", "").replace("区", "").replace("市","")
                if len(tmp_district) < 2:
                    data_info["address"]["district"].remove(data_info["address"]["district"][i])
            if len(data_info["address"]["district"]) > 0:
                print(data_info["address"]["district"])
                data_info["address"]["district"] = rank_words(data_info["address"]["district"], data_info['context'])
                print(data_info["address"]["district"])
                for district in data_info["address"]["district"]:
                    for city_nest in addr_list_city_nest:
                        for district_item in city_nest["district_item"]:
                            if district == district_item['addr_name']:
                                district_name = district
                                city_name = city_nest['district']
                                tmp_dict['start_time'] = data_info['time']
                                start_string = data_info['context']
                                break
                        if city_name != "":
                            break
                    for province_nest in addr_list_province_nest:
                        for city_item in province_nest['city_item']:
                            if city_name == city_item['addr_name']:
                                province_name = province_nest['city']
                                break
                        if province_name != "":
                            break
                    if city_name != '' and province_name != '':
                        break
                if city_name != '' and province_name != '':
                    break
            else:
                print(data_info['context'])
                print(data_info["address"]["city"])
                data_info["address"]["city"] = rank_words(data_info["address"]["city"], data_info['context'])
                print(data_info["address"]["city"])
                for city in data_info["address"]["city"]:
                    for province_nest in addr_list_province_nest:
                        for city_item in province_nest["city_item"]:
                            if city == city_item['addr_name']:
                                city_name = city
                                province_name = province_nest['city']
                                tmp_dict['start_time'] = data_info['time']
                                start_string = data_info['context']
                                break
                        if province_name != "":
                            break
                    if province_name != '':
                        break
                if province_name != '':
                    break

        if city_name != "" and province_name != "" and city_name_to != "" and province_name_to != "":
            tmp_dict['status'] = 1
        elif city_name == "" and province_name == "" and city_name_to != "" and province_name_to != "":
            tmp_dict['status'] = 2
        elif city_name != "" and province_name != "" and city_name_to == "" and province_name_to == "":
            tmp_dict['status'] = 3
        else:
            tmp_dict['status'] = 4

        tmp_dict["danhao"] = item_dict['danhao']
        tmp_dict['start_loc'] = len(item_data) - idx + 1
        tmp_dict['end_loc'] = idx_to
        tmp_dict['start_addr'] = [province_name,city_name,district_name]
        tmp_dict['end_addr'] = [province_name_to, city_name_to, district_name_to]
        tmp_dict['start_string'] = start_string
        tmp_dict['end_string'] = end_string
        item_dict['struct_addr'] = tmp_dict
        simple_result_list.append(tmp_dict)
        # if start_string != "" or end_string != "":
        #     flag_ += 1
        #     tmp_str = json.dumps(tmp_dict,ensure_ascii=False)
        #     f1.write(tmp_str+"\n")
        if tmp_dict['status'] == 1:
            flag_1 += 1
            tmp_str = json.dumps(tmp_dict, ensure_ascii=False)
            f2.write(tmp_str + "\n")

        if tmp_dict['status'] == 2:
            flag_2 += 1
            tmp_str = json.dumps(tmp_dict, ensure_ascii=False)
            f3.write(tmp_str + "\n")

        if tmp_dict['status'] == 4:
            flag_3 += 1
            tmp_str = json.dumps(tmp_dict, ensure_ascii=False)
            f4.write(tmp_str + "\n")

    f2.close()
    f3.close()
    f4.close()
    print(flag_1)
    print(flag_2)
    print(flag_3)
    return data_list_update, simple_result_list


def match_addr_city(update_file,addr_list_province_nest):
    flag = 0
    flag_1 = 0
    flag_2 = 0
    flag_3 = 0
    flag_4 = 0
    simple_result_list = []
    with io.open(update_file,"r",encoding="utf-8") as f:
        data_list_update = json.load(f)
    f1 = io.open("./data/tmp_result_city.txt","w",encoding="utf-8")
    f2 = io.open("./data/result_city_11.txt","w",encoding="utf-8")
    f3 = io.open("./data/result_city_22.txt","w",encoding="utf-8")
    f4 = io.open("./data/result_city_33.txt","w",encoding="utf-8")
    for item_dict in data_list_update:
        flag += 1
        item_data = item_dict['data']
        idx_to = 0
        idx = 0
        city_name_to = ""
        province_name_to = ""
        district_name_to = ""
        city_name = ""
        province_name = ""
        district_name = ""
        tmp_dict = {}
        start_string = ""
        end_string = ""
        tmp_dict['status'] = -1
        tmp_dict['length'] = len(item_data)
        tmp_dict['company'] = item_dict['name_str']
        tmp_dict['start_time'] = ""
        tmp_dict['end_time'] = ""
        #找到收件地址
        for data_info in item_data:
            idx_to = idx_to + 1
            if len(data_info["address"]["city"]) == 0:
                continue
            for city in data_info["address"]["city"]:
                for province_nest in addr_list_province_nest:
                    for city_item in province_nest["city_item"]:
                        if city == city_item['addr_name']:
                            city_name_to = city
                            province_name_to = province_nest['city']
                            tmp_dict['end_time'] = data_info['time']
                            end_string = data_info['context']
                            break
                    if province_name_to != "":
                        break
                if province_name_to != '':
                    break
            if province_name_to != '':
                break

        #找寄件地址
        for data_info in reversed(item_data):
            idx = idx + 1
            if idx + idx_to >= len(item_data):
                break
            if len(data_info["address"]["city"]) == 0:
                continue
            for city in data_info["address"]["city"]:
                for province_nest in addr_list_province_nest:
                    for city_item in province_nest["city_item"]:
                        if city == city_item['addr_name']:
                            city_name = city
                            province_name = province_nest['city']
                            tmp_dict['start_time'] = data_info['time']
                            start_string = data_info['context']
                            break
                    if province_name != "":
                        break
                if province_name != '':
                    break
            if province_name != '':
                break

        if province_name != "" and province_name_to != "":
            tmp_dict['status'] = 1
        elif province_name == "" and province_name_to != "":
            tmp_dict['status'] = 2
        elif province_name != "" and province_name_to == "":
            tmp_dict['status'] = 3
        else:
            tmp_dict['status'] = 4

        tmp_dict["danhao"] = item_dict['danhao']
        tmp_dict['start_loc'] = len(item_data) - idx + 1
        tmp_dict['end_loc'] = idx_to
        tmp_dict['start_addr'] = [province_name,city_name]
        tmp_dict['end_addr'] = [province_name_to, city_name_to]
        tmp_dict['start_string'] = start_string
        tmp_dict['end_string'] = end_string
        item_dict['struct_addr'] = tmp_dict
        simple_result_list.append(tmp_dict)
        # if start_string != "" or end_string != "":
        #     flag_ += 1
        #     tmp_str = json.dumps(tmp_dict,ensure_ascii=False)
        #     f1.write(tmp_str+"\n")
        if tmp_dict['status'] == 1:
            flag_1 += 1
            tmp_str = json.dumps(tmp_dict,ensure_ascii=False)
            f2.write(tmp_str+"\n")

        if tmp_dict['status'] == 2:
            flag_2 += 1
            tmp_str = json.dumps(tmp_dict,ensure_ascii=False)
            f3.write(tmp_str+"\n")

        if tmp_dict['status'] == 4:
            flag_3 += 1
            tmp_str = json.dumps(tmp_dict,ensure_ascii=False)
            f4.write(tmp_str+"\n")

    f2.close()
    f3.close()
    f4.close()
    print(flag_1)
    print(flag_2)
    print(flag_3)
    return data_list_update,simple_result_list

def stat_length(dict_list):
    idx = 0
    idx_ = 0
    flag = 0
    for dict_item in dict_list:
        flag += 1
        if len(dict_item['data']) <= 2:
            idx += 1
        if len(dict_item['data']) < 2:
            idx_ += 1
    print(idx)
    print(idx_)
    print(flag)


def filter_data(update_data_file):
    with io.open(update_data_file,"r",encoding="utf-8") as f1:
        dict_list = json.load(f1)
    result_data = []
    for dict_item in dict_list:
        flag = 0
        if len(dict_item['data']) >= 2:
            for data_item in dict_item['data']:
                if len(data_item['address']['city']) != 0:
                    flag = 1
            if flag == 0:
                result_data.append(dict_item)
    f = io.open("./data/filter_data.txt","w",encoding="utf-8")
    for item in result_data:
        item_ = json.dumps(item,ensure_ascii=False)
        f.write(item_ + "\n")


def generate_result(simple_result,output_file):
    f = io.open(output_file,"w",encoding="utf-8")
    for result_item in simple_result:
        danhao = result_item['danhao']
        company = result_item['company']
        length = result_item['length']
        start_addr = result_item['start_addr'][0] + result_item['start_addr'][1] + result_item['start_addr'][2]
        start_addr = start_addr.replace("京南转运", "北京市")
        # print(result_item)
        start_time = result_item['start_time']
        end_addr = result_item['end_addr'][0] + result_item['end_addr'][1] + result_item['end_addr'][2]
        end_addr = end_addr.replace("京南转运", "北京市")
        end_time = result_item['end_time']
        start_string = result_item['start_string']
        end_string = result_item['end_string']
        line = danhao + "\t"+company+"\t"+str(length)+"\t"+start_addr+"\t"+start_time+"\t"+end_addr+"\t" \
               +end_time+"\t"+start_string+"\t"+end_string+"\n"
        f.write(line)
    f.close()


if __name__ == "__main__":
    ori_data_file = "./data/Skn_spider_express_Update.json"
    addr_data = "./data/addr_dict.txt"
    output_file = "./data/to_excel_district_2.txt"
    # update_data = "./data/update_data.json"
    # duplicate_data(ori_data_file)
    # dict_list = get_standard_data(ori_data_file)
    # dict_list = temp.get_temp_data()

    # data_list_duplicate = duplicate_data(dict_list)
    addr_list_province, addr_list_city, addr_list_district, addr_list_province_nest, addr_list_city_nest = struct_address.struct_addr_dict(addr_data)
    # stat_length(dict_list)
    # print(len(addr_list_district))
    # data_list_update = add_addr_data(dict_list,addr_list_province, addr_list_city, addr_list_district)
    # print(len(data_list_update))
    # print(data_list_update[0])
    # print(data_list_update[1])
    # print(time.time())
    # with io.open("./data/update_data_2.json","w",encoding="utf-8") as f1:
    #     json.dump(data_list_update,f1,ensure_ascii=False)
    data_list_update_,simple_result_list = match_addr_district("./data/update_data_2.json",addr_list_city_nest,addr_list_province_nest)
    # # data_list_update_,simple_result_list = match_addr_city("./data/update_data_1.json",addr_list_province_nest)
    # print(data_list_update_)
    with io.open("./data/update_result_2.json", "w", encoding="utf-8") as f2:
        json.dump(data_list_update_, f2, ensure_ascii=False)
    generate_result(simple_result_list,output_file)

    # filter_data(update_data)

