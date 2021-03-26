# from LAC import LAC
import io
import tools
import random

# def complain_data_seg(complain_data_list):
#     lac = LAC(mode="seg")
#     words_dict = {}
#     words_list = []
#     for complain_data in complain_data_list:
#         seg_result = lac.run(complain_data['complain_problem_ori'])
#         for seg_word in seg_result:
#             if seg_word not in words_dict:
#                 words_dict[seg_word] = 1
#             else:
#                 words_dict[seg_word] = words_dict[seg_word] + 1
#     if words_dict != {}:
#         words_list = [(k,v) for k,v in words_dict.items()]
#     words_list = sorted(words_list,key=lambda x:x[1],reverse=True)
#     return words_list

def struct_complain_data(complain_data_list,input_file_ext,company_list):
    sen_dict = {}
    ori_data_list = []
    sen_list = []

    complain_data_ext_list = tools.loading_data_ext(input_file_ext)

    for complain_data_ext in complain_data_ext_list:
        complain_sen_ext = complain_data_ext['complain_data']
        complain_sen_ext = tools.remove_company(company_list,complain_sen_ext)
        complain_problem_ext = complain_data_ext['complain_problem']
        complain_problem_ext = tools.remove_company(company_list, complain_problem_ext)
        complain_sen_ext = "。".join([complain_sen_ext, complain_problem_ext])
        complain_sen_ext_ = tools.removePunctuation(complain_sen_ext)
        complain_sen_ext_list = complain_sen_ext_.split("。")
        ori_data_list = ori_data_list + complain_sen_ext_list

    for complain_data in complain_data_list:
        complain_sen = complain_data['complain_data']
        complain_sen = tools.remove_company(company_list, complain_sen)
        complain_ori_problem_sen = complain_data['complain_problem_ori']
        complain_ori_problem_sen = tools.remove_company(company_list, complain_ori_problem_sen)
        complain_problem_sen = complain_data['complain_problem']
        complain_problem_sen = complain_problem_sen.replace("|","。")
        complain_problem_sen = tools.remove_company(company_list, complain_problem_sen)

        complain_sen = "。".join([complain_sen,complain_ori_problem_sen,complain_problem_sen])
        complain_sen_ = tools.removePunctuation(complain_sen)
        complain_sen_list = complain_sen_.split("。")
        ori_data_list = ori_data_list + complain_sen_list

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



def complain_data_sign(complain_data_list):
    variety_1 = [{"variety_name":"消费体验","variety_list":["退款","物流","价格","消费综合","续费"]},{"variety_name":"服务体验","variety_list":["客服","服务综合","课堂","vip","合同"]},{"variety_name":"产品体验","variety_list":["产品综合","内容"]}]
    variety_2 = [{"variety_name": "退款", "variety_list": ["不予退款", "退款问题", "不退款", "申请退款/提现不到账", "无退款通道", "退款未到账"]},
                 {"variety_name": "价格",
                  "variety_list": ["价格问题", "费用问题", "乱收费", "收费问题", "自动扣费", "私自扣费", "刚刚下单就降价", "刚买完就降价"]}, \
                 {"variety_name": "消费综合",
                  "variety_list": ["诱导消费", "默认购买增值服务", "优惠券问题", "强迫消费", "设置消费黑洞", "欺骗消费", "赔偿不到位", "发票问题"]}, \
                 {"variety_name": "物流", "variety_list": ["逾期未发货", "虚假发货", "不发货", "快件丢失", "商品有损", "出库中但拒绝修改地址"]},
                 {"variety_name": "续费", "variety_list": ["自动续费", "连续包月无法取消"]}, \
                 {"variety_name": "客服",
                  "variety_list": ["客服不处理", "联系不到客服", "客服处理不当", "平台未只会我们", "不处理客户问题", "客服电话打不通", "客服不作为", "客服糊弄人",
                                   "不理睬"]}, \
                 {"variety_name": "服务综合",
                  "variety_list": ["服务不到位", "恶意私自篡改用户权益", "改规则", "服务质量差", "态度恶劣", "侵犯用户权益", "欺骗学生", "电话骚扰", "短信骚扰",
                                   "暴力催收", "推卸责任", "侵犯消费者知情权", "侵犯隐私", "侵害消费者权益", "中奖名单不真实", "虚假活动", "短信电话骚扰",
                                   "侵犯公民个人隐私", "盗取个人信息", "电话不接"]}, \
                 {"variety_name": "课堂",
                  "variety_list": ["只有寥寥数次答疑", "未提供承诺的周测", "不能有任何的互相讨论", "而且没有提供新的老师", "半路换老师", "欺骗学生", "误导学员", "误导学生",
                                   "qq群一直禁言", "没有分班和定期测试", "提问需要点数", "老师更换", "更改课时性质"]}, \
                 {"variety_name": "vip",
                  "variety_list": ["vip问答收费", "vip问题", "vip提问扣费", "vip提问需要点数", "未履行其vip权益", "vip纠纷"]}, \
                 {"variety_name": "合同",
                  "variety_list": ["霸王条款", "未履行合同", "欺诈违约", "单方撕毁合同", "违反购课合同", "单方面违反合同", "要求维持原有合同", "未履行7天无理由退货",
                                   "未履行保价承诺", "伪造合同", "单方违约", "单方面违约"]}, \
                 {"variety_name": "产品综合", "variety_list": ["强行增加有效期", "账号问题", "擅自更改赠品有效期"]}, \
                 {"variety_name": "内容",
                  "variety_list": ["与承诺的相差甚多", "假货", "赠品问题", "实际核心内容涉抄袭", "虚假承诺", "虚假宣传", "误导宣传", "虚假广告", "与宣传不符"]}]

    standard_data_list = []
    with io.open("./data/statistic.txt",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            standard_data_list.append(line.strip())



    for complain_data in complain_data_list:
        complain_sen = complain_data['complain_data']
        complain_ori_problem_sen = complain_data['complain_problem_ori']
        complain_problem_sen = complain_data['complain_problem']
        # complain_problem_sen_ = complain_problem_sen.replace("|", "。")
        # complain_problem_sen_ = complain_problem_sen_.replace("/", "。")
        complain_sen = "。".join([complain_sen, complain_ori_problem_sen, complain_problem_sen])
        # complain_sen_list = complain_sen.split("。")

        tmp_list = []
        # temp_list_1 = []
        # temp_list_2 = []
        for item in standard_data_list:
            tmp_dict = {}
            if item in complain_sen:
                tmp_dict['rgx_str'] = item
                for item_dict in variety_2:
                    if item in item_dict['variety_list']:
                        tmp_dict['variety_2'] = item_dict['variety_name']
                        for y in variety_1:
                            if item_dict['variety_name'] in y["variety_list"]:
                                tmp_dict['variety_1'] = y['variety_name']
                                tmp_list.append(tmp_dict)
            else:
                continue
        complain_data["variety"] = tmp_list
        # complain_data['variety_2'] = temp_list_1
        # complain_data['variety_1'] = temp_list_2

    return complain_data_list
        # for item_dict in variety_2:

def complain_data_sign_(complain_data_list):
    variety_1 = [{"variety_name":"消费体验","variety_list":["退款","物流","价格","消费综合","续费"]},{"variety_name":"服务体验","variety_list":["客服","服务综合","课堂","vip","合同"]},{"variety_name":"产品体验","variety_list":["产品综合","内容"]}]
    variety_2 = [{"variety_name": "退款", "variety_list": ["不予退款", "退款问题", "不退款", "申请退款/提现不到账", "无退款通道", "退款未到账"]},
                 {"variety_name": "价格",
                  "variety_list": ["价格问题", "费用问题", "乱收费", "收费问题", "自动扣费", "私自扣费", "刚刚下单就降价", "刚买完就降价"]}, \
                 {"variety_name": "消费综合",
                  "variety_list": ["诱导消费", "默认购买增值服务", "优惠券问题", "强迫消费", "设置消费黑洞", "欺骗消费", "赔偿不到位", "发票问题"]}, \
                 {"variety_name": "物流", "variety_list": ["逾期未发货", "虚假发货", "不发货", "快件丢失", "商品有损", "出库中但拒绝修改地址"]},
                  {"variety_name": "续费", "variety_list": ["自动续费", "连续包月无法取消"]}, \
                 {"variety_name": "客服",
                  "variety_list": ["客服不处理", "联系不到客服", "客服处理不当", "平台未只会我们", "不处理客户问题", "客服电话打不通", "客服不作为", "客服糊弄人",
                                   "不理睬"]}, \
                 {"variety_name": "服务综合",
                  "variety_list": ["服务不到位", "恶意私自篡改用户权益", "改规则", "服务质量差", "态度恶劣", "侵犯用户权益", "欺骗学生", "电话骚扰", "短信骚扰",
                                   "暴力催收", "推卸责任", "侵犯消费者知情权", "侵犯隐私", "侵害消费者权益", "中奖名单不真实", "虚假活动", "短信电话骚扰",
                                   "侵犯公民个人隐私", "盗取个人信息", "电话不接"]}, \
                 {"variety_name": "课堂",
                  "variety_list": ["只有寥寥数次答疑", "未提供承诺的周测", "不能有任何的互相讨论", "而且没有提供新的老师", "半路换老师", "欺骗学生", "误导学员", "误导学生",
                                   "qq群一直禁言", "没有分班和定期测试", "提问需要点数", "老师更换", "更改课时性质"]}, \
                 {"variety_name": "vip",
                  "variety_list": ["vip问答收费", "vip问题", "vip提问扣费", "vip提问需要点数", "未履行其vip权益", "vip纠纷"]}, \
                 {"variety_name": "合同",
                  "variety_list": ["霸王条款", "未履行合同", "欺诈违约", "单方撕毁合同", "违反购课合同", "单方面违反合同", "要求维持原有合同", "未履行7天无理由退货",
                                   "未履行保价承诺", "伪造合同", "单方违约", "单方面违约"]}, \
                 {"variety_name": "产品综合", "variety_list": ["强行增加有效期", "账号问题", "擅自更改赠品有效期"]}, \
                 {"variety_name": "内容",
                  "variety_list": ["与承诺的相差甚多", "假货", "赠品问题", "实际核心内容涉抄袭", "虚假承诺", "虚假宣传", "误导宣传", "虚假广告", "与宣传不符"]}]

    standard_data_list = []
    with io.open("./data/statistic.txt",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            standard_data_list.append(line.strip())



    for complain_data in complain_data_list:
        complain_sen = complain_data['complain_data']
        complain_ori_problem_sen = complain_data['complain_problem']
        # complain_problem_sen_ = complain_problem_sen.replace("|", "。")
        # complain_problem_sen_ = complain_problem_sen_.replace("/", "。")
        complain_sen = "。".join([complain_sen, complain_ori_problem_sen])
        # complain_sen_list = complain_sen.split("。")

        tmp_list = []
        # temp_list_1 = []
        # temp_list_2 = []
        for item in standard_data_list:
            tmp_dict = {}
            if item in complain_sen:
                tmp_dict['rgx_str'] = item
                for item_dict in variety_2:
                    if item in item_dict['variety_list']:
                        tmp_dict['variety_2'] = item_dict['variety_name']
                        for y in variety_1:
                            if item_dict['variety_name'] in y["variety_list"]:
                                tmp_dict['variety_1'] = y['variety_name']
                                tmp_list.append(tmp_dict)
            else:
                continue
        complain_data["variety"] = tmp_list
        # complain_data['variety_2'] = temp_list_1
        # complain_data['variety_1'] = temp_list_2

    return complain_data_list

def complain_data_sign_baidu(complain_data_list):
    variety_1 = [{"variety_name":"消费体验","variety_list":["退款","物流","价格","消费综合","续费"]},{"variety_name":"服务体验","variety_list":["客服","服务综合","课堂","vip","合同"]},{"variety_name":"产品体验","variety_list":["产品综合","内容"]}]
    variety_2 = [{"variety_name": "退款", "variety_list": ["不予退款", "退款问题", "不退款", "申请退款/提现不到账", "无退款通道", "退款未到账"]},
                 {"variety_name": "价格",
                  "variety_list": ["价格问题", "费用问题", "乱收费", "收费问题", "自动扣费", "私自扣费", "刚刚下单就降价", "刚买完就降价"]}, \
                 {"variety_name": "消费综合",
                  "variety_list": ["诱导消费", "默认购买增值服务", "优惠券问题", "强迫消费", "设置消费黑洞", "欺骗消费", "赔偿不到位", "发票问题"]}, \
                 {"variety_name": "物流", "variety_list": ["逾期未发货", "虚假发货", "不发货", "快件丢失", "商品有损", "出库中但拒绝修改地址"]},
                 {"variety_name": "续费", "variety_list": ["自动续费", "连续包月无法取消"]}, \
                 {"variety_name": "客服",
                  "variety_list": ["客服不处理", "联系不到客服", "客服处理不当", "平台未只会我们", "不处理客户问题", "客服电话打不通", "客服不作为", "客服糊弄人",
                                   "不理睬"]}, \
                 {"variety_name": "服务综合",
                  "variety_list": ["服务不到位", "恶意私自篡改用户权益", "改规则", "服务质量差", "态度恶劣", "侵犯用户权益", "欺骗学生", "电话骚扰", "短信骚扰",
                                   "暴力催收", "推卸责任", "侵犯消费者知情权", "侵犯隐私", "侵害消费者权益", "中奖名单不真实", "虚假活动", "短信电话骚扰",
                                   "侵犯公民个人隐私", "盗取个人信息", "电话不接"]}, \
                 {"variety_name": "课堂",
                  "variety_list": ["只有寥寥数次答疑", "未提供承诺的周测", "不能有任何的互相讨论", "而且没有提供新的老师", "半路换老师", "欺骗学生", "误导学员", "误导学生",
                                   "qq群一直禁言", "没有分班和定期测试", "提问需要点数", "老师更换", "更改课时性质"]}, \
                 {"variety_name": "vip",
                  "variety_list": ["vip问答收费", "vip问题", "vip提问扣费", "vip提问需要点数", "未履行其vip权益", "vip纠纷"]}, \
                 {"variety_name": "合同",
                  "variety_list": ["霸王条款", "未履行合同", "欺诈违约", "单方撕毁合同", "违反购课合同", "单方面违反合同", "要求维持原有合同", "未履行7天无理由退货",
                                   "未履行保价承诺", "伪造合同", "单方违约", "单方面违约"]}, \
                 {"variety_name": "产品综合", "variety_list": ["一点都不好","一点也不好","一点都不好用","一点也不好用","太不好了","非常不好","不好用","垃圾软件","太垃圾了","非常差","很垃圾","不行","没用","绝望","失望","再也不用了","很差","差劲","忍好几次了","炒作",\
                                                           "一颗星都不想给","大家千万不要用","恶心","流氓软件","气死我","烂的","太坑了","烂货","脑残软件","不满意","删掉","不实用"]}, \
                 {"variety_name": "内容",
                  "variety_list": ["广告太多","错误","骗人的","误人子弟","搜不到","广告多","根本就看不懂","很多答案都是错的"]}]

    standard_data_list = []
    with io.open("./data/statistic_baidu.txt",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            standard_data_list.append(line.strip())


    for complain_data in complain_data_list:
        complain_sen = complain_data['complain_data']
        # complain_ori_problem_sen = complain_data['complain_problem']
        # complain_problem_sen_ = complain_problem_sen.replace("|", "。")
        # complain_problem_sen_ = complain_problem_sen_.replace("/", "。")
        # complain_sen = "。".join([complain_sen, complain_ori_problem_sen])
        # complain_sen_list = complain_sen.split("。")

        tmp_list = []
        # temp_list_1 = []
        # temp_list_2 = []
        for item in standard_data_list:
            tmp_dict = {}
            if item in complain_sen:
                tmp_dict['rgx_str'] = item
                for item_dict in variety_2:
                    if item in item_dict['variety_list']:
                        tmp_dict['variety_2'] = item_dict['variety_name']
                        for y in variety_1:
                            if item_dict['variety_name'] in y["variety_list"]:
                                tmp_dict['variety_1'] = y['variety_name']
                                tmp_list.append(tmp_dict)
            else:
                continue
        complain_data["variety"] = tmp_list
        # complain_data['variety_2'] = temp_list_1
        # complain_data['variety_1'] = temp_list_2

    return complain_data_list


if __name__ == "__main__":
    ori_data = "./data/complain_education.txt"
    company_file = "./data/company_data.txt"
    ori_data_ext = "./data/tousu_info.txt"
    # complain_data_list = tools.loading_education_data(ori_data)
    variety_1_ = [{"variety_name": "消费体验", "variety_list": ["退款", "物流", "价格", "消费综合", "续费"]},
                 {"variety_name": "服务体验", "variety_list": ["客服", "服务综合", "课堂", "vip", "合同"]},
                 {"variety_name": "产品体验", "variety_list": ["产品综合", "内容"]}]
    variety_2_ = [{"variety_name": "退款", "variety_list": ["不予退款", "退款问题", "不退款", "申请退款/提现不到账", "无退款通道", "退款未到账"]},
                 {"variety_name": "价格",
                  "variety_list": ["价格问题", "费用问题", "乱收费", "收费问题", "自动扣费", "私自扣费", "刚刚下单就降价", "刚买完就降价"]}, \
                 {"variety_name": "消费综合",
                  "variety_list": ["诱导消费", "默认购买增值服务", "优惠券问题", "强迫消费", "设置消费黑洞", "欺骗消费", "赔偿不到位", "发票问题"]}, \
                 {"variety_name": "物流", "variety_list": ["逾期未发货", "虚假发货", "不发货", "快件丢失", "商品有损", "出库中但拒绝修改地址"]},
                 {"variety_name": "续费", "variety_list": ["自动续费", "连续包月无法取消"]}, \
                 {"variety_name": "客服",
                  "variety_list": ["客服不处理", "联系不到客服", "客服处理不当", "平台未只会我们", "不处理客户问题", "客服电话打不通", "客服不作为", "客服糊弄人",
                                   "不理睬"]}, \
                 {"variety_name": "服务综合",
                  "variety_list": ["服务不到位", "恶意私自篡改用户权益", "改规则", "服务质量差", "态度恶劣", "侵犯用户权益", "欺骗学生", "电话骚扰", "短信骚扰",
                                   "暴力催收", "推卸责任", "侵犯消费者知情权", "侵犯隐私", "侵害消费者权益", "中奖名单不真实", "虚假活动", "短信电话骚扰",
                                   "侵犯公民个人隐私", "盗取个人信息", "电话不接"]}, \
                 {"variety_name": "课堂",
                  "variety_list": ["只有寥寥数次答疑", "未提供承诺的周测", "不能有任何的互相讨论", "而且没有提供新的老师", "半路换老师", "欺骗学生", "误导学员", "误导学生",
                                   "qq群一直禁言", "没有分班和定期测试", "提问需要点数", "老师更换", "更改课时性质"]}, \
                 {"variety_name": "vip",
                  "variety_list": ["vip问答收费", "vip问题", "vip提问扣费", "vip提问需要点数", "未履行其vip权益", "vip纠纷"]}, \
                 {"variety_name": "合同",
                  "variety_list": ["霸王条款", "未履行合同", "欺诈违约", "单方撕毁合同", "违反购课合同", "单方面违反合同", "要求维持原有合同", "未履行7天无理由退货",
                                   "未履行保价承诺", "伪造合同", "单方违约", "单方面违约"]}, \
                 {"variety_name": "产品综合", "variety_list": ["强行增加有效期", "账号问题", "擅自更改赠品有效期"]}, \
                 {"variety_name": "内容",
                  "variety_list": ["与承诺的相差甚多", "假货", "赠品问题", "实际核心内容涉抄袭", "虚假承诺", "虚假宣传", "误导宣传", "虚假广告", "与宣传不符"]}]

    # company_list = tools.read_company(company_file)
    # for complain_data in complain_data_list:
    #     print(complain_data)
    # words_list = complain_data_seg(complain_data_list)
    # with io.open("./data/seg_ori_data_problem.txt","w",encoding="utf-8") as f1:
    #     for seg_word in words_list:
    #         f1.write(str(seg_word) + "\n")
    # sen_list = struct_complain_data(complain_data_list,ori_data_ext,company_list)
    # with io.open("./data/sen_ori_data_all.txt", "w", encoding="utf-8") as f1:
    #     for seg_sen in sen_list:
    #         f1.write(str(seg_sen) + "\n")
    # ___________________________________________
    # write_list = []
    # complain_data_list_ext = tools.loading_data_ext(ori_data_ext)
    # complain_data_list_ext = complain_data_sign(complain_data_list)
    # print(complain_data_list_ext)
    # # with io.open("./data/data_result_update.txt","w",encoding="utf-8") as f1:
    # for complain_data_list in complain_data_list_ext:
    #     complain_id = complain_data_list["complain_id"]
    #     # complain_company = complain_data_list["complain_company"]
    #     complain_data = complain_data_list["complain_data"]
    #     complain_problem_ori = complain_data_list["complain_problem_ori"]
    #     complain_problem = complain_data_list["complain_problem"]
    #     variety = complain_data_list["variety"]
    #     variety_1_list = []
    #     variety_2_list = []
    #     rgx_str_list = []
    #     rgx_result = ""
    #     variety_1_result = ""
    #     variety_2_result = ""
    #
    #     for item_dict in variety:
    #         rgx_str = item_dict['rgx_str']
    #         rgx_str_list.append(rgx_str)
    #     for item_dict in variety:
    #         variety_1 = item_dict['variety_1']
    #         variety_1_list.append(variety_1)
    #     for item_dict in variety:
    #         variety_2 = item_dict['variety_2']
    #         variety_2_list.append(variety_2)
    #     for i in range(len(variety)):
    #         rgx_result = rgx_str_list[i]
    #         variety_1_result =  variety_1_list[i]
    #         variety_2_result = variety_2_list[i]
    #     variety_2_tmp_dict = {}
    #     for item in variety_2_:
    #         # print(variety_2_list)
    #         # print(item)
    #         if item["variety_name"] in set(variety_2_list):
    #             variety_2_tmp_dict[item["variety_name"]] = []
    #             for item_rgx in item["variety_list"]:
    #                 if item_rgx in rgx_str_list:
    #                     variety_2_tmp_dict[item["variety_name"]] = variety_2_tmp_dict[item["variety_name"]] + [item_rgx]
    #     variety_2_tmp_str = ""
    #     print(variety_2_tmp_dict)
    #     variety_mp_str = ""
    #     variety_tmp_dict = {}
    #     for t in range(len(variety)):
    #         if (variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)") in variety_tmp_dict:
    #             variety_tmp_dict[variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)"] = variety_tmp_dict[variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)"] + ","+ rgx_str_list[t]
    #         else:
    #             variety_tmp_dict[variety_1_list[t] + "(一级分类)" + "_" + variety_2_list[t] + "(二级分类)"] = "\n" + variety_1_list[t] + "(一级分类)" + "_" + variety_2_list[t] + "(二级分类)" + ":" + rgx_str_list[t]
    #             # variety_mp_str = variety_mp_str + variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)" +":"+ rgx_str_list[t] + "\n"
    #
    #     variety_tmp_result = ""
    #     for k,v in variety_tmp_dict.items():
    #         variety_tmp_result = variety_tmp_result + v
    #         # variety_2_tmp_str = variety_2_tmp_str + k + ":" + ",".join(v) + "\n"
    #     #
    #
    #     for k,v in variety_2_tmp_dict.items():
    #         variety_2_tmp_str = variety_2_tmp_str + k + ":" + ",".join(v) + "\n"
    #     # variety_2 = ",".join(set(complain_data_list["variety_2"]))
    #     # variety_1 = ",".join(set(complain_data_list["variety_1"]))
    #     # write_list.append("id:" + complain_id + "\n" + "topic:" + complain_data + "\n" + "title:" + complain_problem_ori + \
    #     #                   "\n" + "problemLabelList:" + complain_problem + "\n" + "\n" + "一级分类：" + ",".join(set(variety_1_list)) + "\n" + "二级分类：" + ",".join(set(variety_2_list)) +"\n" +\
    #     #                   variety_2_tmp_str + "\n" + "---------------------" + "\n")
    #     write_list.append(
    #         "id:" + complain_id + "\n" + "topic:" + complain_data + "\n" + "title:" + complain_problem_ori + \
    #         "\n" + "problemLabelList:" + complain_problem + "\n" + "\n" + variety_tmp_result + "\n" + "---------------------" + "\n")
    #     # write_list.append("\n".join([complain_id,complain_company,complain_data,complain_problem_ori,complain_problem,variety_1_result,variety_2_result,rgx_result])+"\n")
    #
    # random.shuffle(write_list)
    #
    # with io.open("./data/data_result_update_1.txt", "w", encoding="utf-8") as f1:
    #     for write_item in write_list:
    #         f1.write(write_item)
    # __________________________________________________
    # for complain_data_list in complain_data_list_ext:
    #     complain_id = complain_data_list["complain_id"]
    #     complain_company = complain_data_list["complain_company"]
    #     complain_data = complain_data_list["complain_data"]
    #     # complain_problem_ori = complain_data_list["complain_problem_ori"]
    #     complain_problem = complain_data_list["complain_problem"]
    #     variety = complain_data_list["variety"]
    #     variety_1_list = []
    #     variety_2_list = []
    #     rgx_str_list = []
    #     rgx_result = ""
    #     variety_1_result = ""
    #     variety_2_result = ""
    #
    #     for item_dict in variety:
    #         rgx_str = item_dict['rgx_str']
    #         rgx_str_list.append(rgx_str)
    #     for item_dict in variety:
    #         variety_1 = item_dict['variety_1']
    #         variety_1_list.append(variety_1)
    #     for item_dict in variety:
    #         variety_2 = item_dict['variety_2']
    #         variety_2_list.append(variety_2)
    #     for i in range(len(variety)):
    #         rgx_result = rgx_str_list[i]
    #         variety_1_result =  variety_1_list[i]
    #         variety_2_result = variety_2_list[i]
    #     variety_2_tmp_dict = {}
    #     for item in variety_2_:
    #         # print(variety_2_list)
    #         # print(item)
    #         if item["variety_name"] in set(variety_2_list):
    #             variety_2_tmp_dict[item["variety_name"]] = []
    #             for item_rgx in item["variety_list"]:
    #                 if item_rgx in rgx_str_list:
    #                     variety_2_tmp_dict[item["variety_name"]] = variety_2_tmp_dict[item["variety_name"]] + [item_rgx]
    #     variety_2_tmp_str = ""
    #     print(variety_2_tmp_dict)
    #     variety_mp_str = ""
    #     variety_tmp_dict = {}
    #     if variety == []:
    #         write_list.append("聚投诉" + "\t" + complain_company + '\t' + complain_data )
    #         continue
    #     for t in range(len(variety)):
    #         if (variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)") in variety_tmp_dict:
    #             variety_tmp_dict[variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)"] = variety_tmp_dict[variety_1_list[t] + \
    #                                             "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)"] + ","+ rgx_str_list[t]
    #         else:
    #             variety_tmp_dict[variety_1_list[t] + "(一级分类)" + "_" + variety_2_list[t] + "(二级分类)"] = variety_1_list[t] + \
    #                                                             "\t" + variety_2_list[t] +  "\t" + rgx_str_list[t]
    #             # variety_mp_str = variety_mp_str + variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)" +":"+ rgx_str_list[t] + "\n"
    #
    #     variety_tmp_list = []
    #     for k, v in variety_tmp_dict.items():
    #         variety_tmp_list.append(v)
    #
    #     # variety_tmp_result = ""
    #     # for k,v in variety_tmp_dict.items():
    #     #     variety_tmp_result = variety_tmp_result + v
    #         # variety_2_tmp_str = variety_2_tmp_str + k + ":" + ",".join(v) + "\n"
    #     #
    #
    #     for k,v in variety_2_tmp_dict.items():
    #         variety_2_tmp_str = variety_2_tmp_str + k + ":" + ",".join(v) + "\n"
    #
    #     for i in range(len(variety_tmp_list)):
    #         if i == 0:
    #             write_list.append("聚投诉" + "\t" + complain_company +'\t'+complain_data + \
    #         "\t" + variety_tmp_list[i])
    #         else:
    #             write_list.append( " " + "\t" + " " + "\t" + " "\
    #         "\t" + variety_tmp_list[i])
    #     # variety_2 = ",".join(set(complain_data_list["variety_2"]))
    #     # variety_1 = ",".join(set(complain_data_list["variety_1"]))
    #     # write_list.append("id:" + complain_id + "\n" + "topic:" + complain_data + "\n" + "title:" + complain_problem_ori + \
    #     #                   "\n" + "problemLabelList:" + complain_problem + "\n" + "\n" + "一级分类：" + ",".join(set(variety_1_list)) + "\n" + "二级分类：" + ",".join(set(variety_2_list)) +"\n" +\
    #     #                   variety_2_tmp_str + "\n" + "---------------------" + "\n")
    #     # write_list.append(
    #     #     "id:" + complain_id + "\n" + "topic:" + complain_data + \
    #     #     "\n" + "ask:" + complain_problem + "\n" + variety_tmp_result + "\n" + "---------------------" + "\n")
    #     # write_list.append("\n".join([complain_id,complain_company,complain_data,complain_problem_ori,complain_problem,variety_1_result,variety_2_result,rgx_result])+"\n")
    #
    # # random.shuffle(write_list)
    #
    # with io.open("./data/data_result_update_3.txt", "w", encoding="utf-8") as f1:
    #     for write_item in write_list:
    #         f1.write(write_item + "\n")
    # ___________________________________________
    write_list = []
    ori_data_ext = "./data/baidu.txt"
    complain_data_list_ext = tools.loading_data_baidu(ori_data_ext)
    complain_data_list_ext = complain_data_sign_baidu(complain_data_list_ext)
    print(complain_data_list_ext)
    # with io.open("./data/data_result_update.txt","w",encoding="utf-8") as f1:
    flag = 0
    for complain_data_list in complain_data_list_ext:
        complain_id = complain_data_list["complain_id"]
        complain_company = complain_data_list["complain_company"]
        complain_data = complain_data_list["complain_data"]
        # complain_problem_ori = complain_data_list["complain_problem_ori"]
        # complain_problem = complain_data_list["complain_problem"]
        variety = complain_data_list["variety"]
        variety_1_list = []
        variety_2_list = []
        rgx_str_list = []
        rgx_result = ""
        variety_1_result = ""
        variety_2_result = ""

        for item_dict in variety:
            rgx_str = item_dict['rgx_str']
            rgx_str_list.append(rgx_str)
        for item_dict in variety:
            variety_1 = item_dict['variety_1']
            variety_1_list.append(variety_1)
        for item_dict in variety:
            variety_2 = item_dict['variety_2']
            variety_2_list.append(variety_2)
        for i in range(len(variety)):
            rgx_result = rgx_str_list[i]
            variety_1_result = variety_1_list[i]
            variety_2_result = variety_2_list[i]
        variety_2_tmp_dict = {}
        for item in variety_2_:
            # print(variety_2_list)
            # print(item)
            if item["variety_name"] in set(variety_2_list):
                variety_2_tmp_dict[item["variety_name"]] = []
                for item_rgx in item["variety_list"]:
                    if item_rgx in rgx_str_list:
                        variety_2_tmp_dict[item["variety_name"]] = variety_2_tmp_dict[item["variety_name"]] + [
                            item_rgx]
        variety_2_tmp_str = ""
        variety_mp_str = ""
        variety_tmp_dict = {}
        if variety == []:
            write_list.append("百度商家口碑" + "\t" + complain_company + '\t' + complain_data )
            continue
        for t in range(len(variety)):
            if (variety_1_list[t] + "(一级分类)" + "_" + variety_2_list[t] + "(二级分类)") in variety_tmp_dict:
                variety_tmp_dict[variety_1_list[t] + "(一级分类)" + "_" + variety_2_list[t] + "(二级分类)"] = \
                variety_tmp_dict[variety_1_list[t] + "(一级分类)" + "_" + variety_2_list[t] + "(二级分类)"] + "," + \
                rgx_str_list[t]
            else:
                variety_tmp_dict[variety_1_list[t] + "(一级分类)" + "_" + variety_2_list[t] + "(二级分类)"] = variety_1_list[
                                                                                                          t] + "\t" + \
                                                                                                      variety_2_list[
                                                                                                          t] + "\t" + \
                                                                                                      rgx_str_list[
                                                                                                          t]
                # variety_mp_str = variety_mp_str + variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)" +":"+ rgx_str_list[t] + "\n"

        variety_tmp_list = []
        for k, v in variety_tmp_dict.items():
            variety_tmp_list.append(v)
            # variety_2_tmp_str = variety_2_tmp_str + k + ":" + ",".join(v) + "\n"
        #
        #
        # for k, v in variety_2_tmp_dict.items():
        #     variety_2_tmp_str = variety_2_tmp_str + k + ":" + ",".join(v) + "\n"
        # variety_2 = ",".join(set(complain_data_list["variety_2"]))
        # variety_1 = ",".join(set(complain_data_list["variety_1"]))
        # write_list.append("id:" + complain_id + "\n" + "topic:" + complain_data + "\n" + "title:" + complain_problem_ori + \
        #                   "\n" + "problemLabelList:" + complain_problem + "\n" + "\n" + "一级分类：" + ",".join(set(variety_1_list)) + "\n" + "二级分类：" + ",".join(set(variety_2_list)) +"\n" +\
        #                   variety_2_tmp_str + "\n" + "---------------------" + "\n")
        for i in range(len(variety_tmp_list)):
            if i == 0:
                write_list.append("百度商家口碑" + "\t" + complain_company + "\t" + complain_data + \
            "\t" + variety_tmp_list[i])
            else:
                write_list.append(" " + "\t" + " " + "\t" + " " + \
            "\t" + variety_tmp_list[i])

        # write_list.append(
        #     "id:" + complain_id + "\n" + "topic:" + complain_data + \
        #     "\n" + variety_tmp_result + "\n" + "---------------------" + "\n")
        # if variety_tmp_result != "":
        #     flag += 1
        # write_list.append("\n".join([complain_id,complain_company,complain_data,complain_problem_ori,complain_problem,variety_1_result,variety_2_result,rgx_result])+"\n")

    # random.shuffle(write_list)

    with io.open("./data/data_result_update_baidu_.txt", "w", encoding="utf-8") as f1:
        for write_item in write_list:
            f1.write(write_item+"\n")
    print(flag)
    #-------------
    # print(complain_data_list_ext)
    # with io.open("./data/data_result_update.txt","w",encoding="utf-8") as f1:
    # for complain_data_list in complain_data_list_ext:
    #     complain_id = complain_data_list["complain_id"]
    #     # complain_company = complain_data_list["complain_company"]
    #     complain_data = complain_data_list["complain_data"]
    #     # complain_problem_ori = complain_data_list["complain_problem_ori"]
    #     complain_problem = complain_data_list["complain_problem"]
    #     variety = complain_data_list["variety"]
    #     variety_1_list = []
    #     variety_2_list = []
    #     rgx_str_list = []
    #     rgx_result = ""
    #     variety_1_result = ""
    #     variety_2_result = ""
    #
    #     for item_dict in variety:
    #         rgx_str = item_dict['rgx_str']
    #         rgx_str_list.append(rgx_str)
    #     for item_dict in variety:
    #         variety_1 = item_dict['variety_1']
    #         variety_1_list.append(variety_1)
    #     for item_dict in variety:
    #         variety_2 = item_dict['variety_2']
    #         variety_2_list.append(variety_2)
    #     for i in range(len(variety)):
    #         rgx_result = rgx_str_list[i]
    #         variety_1_result =  variety_1_list[i]
    #         variety_2_result = variety_2_list[i]
    #     variety_2_tmp_dict = {}
    #     for item in variety_2_:
    #         # print(variety_2_list)
    #         # print(item)
    #         if item["variety_name"] in set(variety_2_list):
    #             variety_2_tmp_dict[item["variety_name"]] = []
    #             for item_rgx in item["variety_list"]:
    #                 if item_rgx in rgx_str_list:
    #                     variety_2_tmp_dict[item["variety_name"]] = variety_2_tmp_dict[item["variety_name"]] + [item_rgx]
    #     variety_2_tmp_str = ""
    #     print(variety_2_tmp_dict)
    #     variety_mp_str = ""
    #     variety_tmp_dict = {}
    #     for t in range(len(variety)):
    #         if (variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)") in variety_tmp_dict:
    #             variety_tmp_dict[variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)"] = variety_tmp_dict[variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)"] + ","+ rgx_str_list[t]
    #         else:
    #             variety_tmp_dict[variety_1_list[t] + "(一级分类)" + "_" + variety_2_list[t] + "(二级分类)"] = variety_1_list[t] + "\t" + variety_2_list[t] + "\t" + rgx_str_list[t]
    #             # variety_mp_str = variety_mp_str + variety_1_list[t] + "(一级分类)" +"_"+ variety_2_list[t] + "(二级分类)" +":"+ rgx_str_list[t] + "\n"
    #
    #     variety_tmp_list = []
    #     for k, v in variety_tmp_dict.items():
    #         variety_tmp_list.append(v)
    #     # variety_tmp_result = ""
    #     # for k,v in variety_tmp_dict.items():
    #     #     variety_tmp_result = variety_tmp_result + v
    #         # variety_2_tmp_str = variety_2_tmp_str + k + ":" + ",".join(v) + "\n"
    #     #
    #
    #     for k,v in variety_2_tmp_dict.items():
    #         variety_2_tmp_str = variety_2_tmp_str + k + ":" + ",".join(v) + "\n"
    #
    #     for i in range(len(variety_tmp_list)):
    #         if i == 0:
    #             write_list.append("新浪-黑猫投诉" + "\t" + " " +'\t'+complain_data + \
    #         "\t" + variety_tmp_list[i])
    #         else:
    #             write_list.append( " " + "\t" + " " + "\t" + " "\
    #         "\t" + variety_tmp_list[i])
    #     # variety_2 = ",".join(set(complain_data_list["variety_2"]))
    #     # variety_1 = ",".join(set(complain_data_list["variety_1"]))
    #     # write_list.append("id:" + complain_id + "\n" + "topic:" + complain_data + "\n" + "title:" + complain_problem_ori + \
    #     #                   "\n" + "problemLabelList:" + complain_problem + "\n" + "\n" + "一级分类：" + ",".join(set(variety_1_list)) + "\n" + "二级分类：" + ",".join(set(variety_2_list)) +"\n" +\
    #     #                   variety_2_tmp_str + "\n" + "---------------------" + "\n")
    #     # write_list.append(
    #     #     "id:" + complain_id + "\n" + "topic:" + complain_data + "\n" + "title:" + complain_problem_ori + \
    #     #     "\n" + "problemLabelList:" + complain_problem + "\n" + "\n" + variety_tmp_result + "\n" + "---------------------" + "\n")
    #     # write_list.append("\n".join([complain_id,complain_company,complain_data,complain_problem_ori,complain_problem,variety_1_result,variety_2_result,rgx_result])+"\n")
    #
    # # random.shuffle(write_list)
    #
    # with io.open("./data/data_result_update_4.txt", "w", encoding="utf-8") as f1:
    #     for write_item in write_list:
    #         f1.write(write_item + "\n")




