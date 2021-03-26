import xlrd
import io
import json

def read_xlrd(excelFile):
    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(0)
    all_addr_list = []
    for rowNum in range(table.nrows):
        tmp_dict = {}
        rowVale = table.row_values(rowNum)
        for colNum in range(table.ncols):
            # print(rowVale[colNum])
            if colNum == 0:
                tmp_dict['addr_code'] = rowVale[colNum]
            if colNum == 1:
                tmp_dict['addr_name'] = rowVale[colNum]
            if colNum == 2:
                tmp_dict['address_parent'] = rowVale[colNum]
            if colNum == 3:
                tmp_dict['address_order'] = rowVale[colNum]
        all_addr_list.append(tmp_dict)
    f1 = io.open("./data/addr_dict.txt","w",encoding="utf-8")
    for item in all_addr_list:
        item_ = json.dumps(item,ensure_ascii=False)
        f1.write(item_ + "\n")
    f1.close()

    # if判断是将 id 进行格式化
    # print("未格式化Id的数据：")
    # print(table.cell(1, 0))
    # 结果：number:1001.0

def struct_addr_dict(addr_file):
    del_list = ["县"]
    addr_list = []
    addr_list_province = []
    addr_list_city = []
    addr_list_district = []
    addr_list_province_nest = []
    addr_list_city_nest = []
    with io.open(addr_file,"r",encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            line_dict = json.loads(line_str)
            addr_list.append(line_dict)

    for item in addr_list:
        if len(item["address_parent"]) == 1:
            addr_list_province.append(item)
        elif len(item["address_parent"]) == 2 and item["addr_name"] not in del_list:        #加了这一句有可能通过街道乡镇找不到县
            addr_list_city.append(item)
        elif item["address_parent"][4:] == "00000000":
            if item['addr_name'] not in del_list:
                addr_list_district.append(item)
        else:
            continue

    # print(len(addr_list_province))
    # print(len(addr_list_city))
    # print(len(addr_list_district))

    for addr_province in addr_list_province:
        tmp_list = []
        tmp_dict = {}
        for addr_city in addr_list_city:
            if addr_province["addr_code"] == addr_city["address_parent"]:
                tmp_list.append(addr_city)
        tmp_dict['city'] = addr_province["addr_name"]
        tmp_dict["city_item"] = tmp_list
        addr_list_province_nest.append(tmp_dict)

    for addr_city in addr_list_city:
        tmp_list = []
        tmp_dict = {}
        for addr_district in addr_list_district:
            if addr_city["addr_code"] == addr_district["address_parent"]:       #只对应了县和市的映射，所以如果有镇等的存在不会映射到市
                tmp_list.append(addr_district)
        tmp_dict['district'] = addr_city["addr_name"]
        tmp_dict["district_item"] = tmp_list
        addr_list_city_nest.append(tmp_dict)

    return addr_list_province, addr_list_city, addr_list_district, addr_list_province_nest, addr_list_city_nest


if __name__ == '__main__':
    # excelFile = 'data/address_info.xlsx'
    # read_xlrd(excelFile=excelFile)
    addr_list_province, addr_list_city, addr_list_district, addr_list_province_nest, addr_list_city_nest = struct_addr_dict("./data/addr_dict.txt")
    all_addr_dict = {
        "addr_list_province":addr_list_province,
        "addr_list_city": addr_list_city,
        "addr_list_district": addr_list_district,
        "addr_list_province_nest": addr_list_province_nest,
        "addr_list_city_nest": addr_list_city_nest
    }
    with io.open("./data_dict.json","w",encoding="utf-8") as f:
        json.dump(all_addr_dict,f,ensure_ascii=False)