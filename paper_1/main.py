import string
from itertools import combinations
import os
import sys
sys.path.append("..")
import parameter

class Router():
    def __init__(self):
        self.num = int  # 自身路由器编号
        self.edge_info = []  #  (对方路由器编号，长度，边的编号)
        self.neighbor_edge_num = int  # 相邻的边的编号
        self.first_district_num = int  # 每个路由器第一分区所在的编号
        self.first_district_edge = {}  # 第六步中确定的第一分区最短链路

        self.second_district_num = int  # 每个路由器第二分区所在的编号
        self.second_district_edge = {}  # 第六步中确定的第二分区最短链路

        self.third_district_num = int  # 每个路由器第三分区所在的编号
        self.third_district_edge = {}  # 第六步中确定的第三分区最短链路
        self.end_to_end_info = {}

        self.master_link = {}  # “link”:[], "len":[]; 下同
        self.slave_link = {}

ROUTER_NUM = parameter.ROUTER_NUM  #11为cost239拓扑个数
map_file_name = parameter.map_file_name

ROUTER_LIST = [Router() for i in range(ROUTER_NUM)]
EDGE_NUM = 0
alpha = 0.5
p = 0.02  # 光纤百公里故障概率

def init_router():
    edge_num = 0  # 边的编号
    f = open(map_file_name, "r", encoding="utf-8")
    lines = f.readlines()

    # 从文件中读取边的信息并保存
    for i in range(0,lines.__len__()):  # i为路由器本身编号
        end_num = 0  # 对面路由器的编号
        for edge_len in lines[i].split():
            edge_len = int(edge_len.strip(string.whitespace))
            ROUTER_LIST[i].num = i
            if i < end_num:
                if edge_len == -1:
                    ROUTER_LIST[i].edge_info.append({"end_num":end_num, "len":edge_len, "edge_num": 0})
                else:
                    edge_num += 1
                    ROUTER_LIST[i].edge_info.append({"end_num": end_num, "len": edge_len, "edge_num": edge_num})

            elif i > end_num:
                for j in ROUTER_LIST[end_num].edge_info:
                    if j["end_num"] == i:
                        ROUTER_LIST[i].edge_info.append({"end_num": end_num, "len": edge_len, "edge_num": j["edge_num"]})
                        if j["len"] != edge_len:
                            print("error：编号相等的边长度不相等")
                        break
            elif i == end_num:
                ROUTER_LIST[i].edge_info.append({"end_num": end_num, "len": edge_len, "edge_num": 0})
            end_num += 1
    for i in range(ROUTER_NUM):
        peer_edge_num = 0
        for j in ROUTER_LIST[i].edge_info:
            if j["len"] > 0:
                peer_edge_num += 1
        ROUTER_LIST[i].neighbor_edge_num = peer_edge_num
    return edge_num


# 最小点覆盖
def mvc():
    temp = [i for i in range(ROUTER_NUM)]  # [0,1,...,10]

    result_list = []  # 结果的存储列表

    # 穷举法
    for i in range(1, ROUTER_NUM+1):
        candidate_list = list(combinations(temp, i))
        for j in candidate_list:  # j ->  (1,2,...)
            edge_temp = []
            result_flag = True  # 标识是否是点覆盖
            for k in j:
                for l in ROUTER_LIST[k].edge_info:
                    edge_temp.append(l["edge_num"])

            # 检测是否含有所有的边
            for m in range(1, EDGE_NUM+1):
                if m not in edge_temp:
                    result_flag = False
                    break

            if result_flag:
                result_list.append(j)

    min_len = 1000
    for i in result_list:
        if min_len > len(i):
            min_len = len(i)

    result = []
    for i in result_list:
        if len(i) == min_len:
            result.append(i)
    print("最小点覆盖:",result)
    return result

# 极小支配集
def mds():
    temp = [i for i in range(ROUTER_NUM)]  # [0,1,...,10]

    result_list = []  # 结果的存储列表

    # 穷举法
    for i in range(1, ROUTER_NUM + 1):
        candidate_list = list(combinations(temp, i))
        for j in candidate_list:  # j ->  (1,2,...)
            router_temp = []
            result_flag = True  # 标识是否是支配集
            for k in j:
                for l in ROUTER_LIST[k].edge_info:
                    if l["len"] != -1:
                        router_temp.append(l["end_num"])

            # 检测是否含有所有的路由器
            for m in range(0, ROUTER_NUM):
                if m not in router_temp:
                    result_flag = False
                    break

            if result_flag:
                for k in j:
                    for l in ROUTER_LIST[k].edge_info:
                        if l["len"] != -1:
                            router_temp.remove(l["end_num"])
                    for m in range(0, ROUTER_NUM):
                        if m not in router_temp:
                            result_flag = False
                            break

                    if result_flag:
                        break
                    else:
                        result_flag = True
                        for l in ROUTER_LIST[k].edge_info:
                            if l["len"] != -1:
                                router_temp.append(l["end_num"])
                        if j.index(k) == len(j)-1:
                            result_list.append(j)
    print("极小支配集:", result_list)
    return result_list

def step_3(mvc_list, mds_list):
    couple = []
    couple_key = []
    for i in mvc_list:
        for j in mds_list:  # j ->  [(1,2,...),(1,2,...),(1,2,...)]
            if set(j).issubset(set(i)):
                    couple.append({"mvc": i, "mds": j})
                    if i not in couple_key:
                        couple_key.append(i)


    couple_temp_2 = []
    for i in couple_key:
        couple_temp_1 = {"mvc": i, "mds": []}
        for j in couple:
            if j["mvc"] == i:
                couple_temp_1["mds"].append(j["mds"])
        couple_temp_2.append(couple_temp_1)


    couple_temp_3 = []
    # 选取包含节点数最小的
    for i in couple_temp_2:
        couple_temp_1 = {"mvc": i["mvc"], "mds": []}
        min_router_num = 1000
        for j in i["mds"]:
            if min_router_num > len(j):
                min_router_num = len(j)
        for j in i["mds"]:
            if len(j) == min_router_num:
                couple_temp_1["mds"].append(j)
        couple_temp_3.append(couple_temp_1)

    print(couple_temp_3)

    couple_temp_4 = []
    # 选取节点相邻的边最多的，（包含最后的随机选取）
    for i in couple_temp_3:
        max_edge_num = 0
        for j in i["mds"]:   # j -> (2, 6)
            max_edge_num_temp = -1
            for k in j:
                max_edge_num_temp += ROUTER_LIST[k].neighbor_edge_num
            if max_edge_num < max_edge_num_temp:
                max_edge_num = max_edge_num_temp
                couple_temp_1 = {"mvc": i["mvc"], "mds": j}
        couple_temp_4.append(couple_temp_1)

    print("最小点覆盖与极小支配集的组合：", couple_temp_4)
    return couple_temp_4

def step_4(result_3_step):
    min_router_num = 10000
    result_4_step = []
    for i in result_3_step:
        if len(i["mds"]) < min_router_num:
            min_router_num = len(i["mds"])
    for i in result_3_step:
        if len(i["mds"]) == min_router_num:
            result_4_step.append(i)
    print("第四步结果：", result_4_step)
    return result_4_step

def step_5(result_4_step):
    candidate_list = []
    for i in result_4_step:  # i -> [{'mvc': (0, 1, 3, 5, 6, 8, 10, 12), 'mds': (0, 3, 5, 6, 8)}, {'mvc': (0, 1, 3, 5, 6, 8, 11, 13), 'mds': (0, 3, 5, 6, 8)},
        Vj = []   # 最小点覆盖的点
        Vi = []    #不属于最小点覆盖的点
        Vd = []   # 极小支配集的点
        for j in i["mvc"]:
            Vj.append(j)
        for j in range(ROUTER_NUM):
            if j not in i["mvc"]:
                Vi.append(j)
        for j in i["mds"]:
            Vd.append(j)

        D_ij_sum = 0
        for k in Vi:
            min_dis = 1000000
            for j in ROUTER_LIST[k].edge_info:
                if j["end_num"] in Vj and min_dis > j["len"] and j["len"] > 0:
                    min_dis = j["len"]
            D_ij_sum += min_dis

        D_id_sum = 0
        for k in Vi:
            min_dis = 1000000
            for j in ROUTER_LIST[k].edge_info:
                if j["end_num"] in Vd and min_dis > j["len"] and j["len"] > 0:
                    min_dis = j["len"]
            D_id_sum += min_dis

        compare_value = alpha*D_ij_sum+(1-alpha)*D_id_sum
        candidate_list.append({"compare_value":compare_value, "routers": i})

    compare_list = []
    for i in candidate_list:
        compare_list.append(i["compare_value"])
    min_value = min(compare_list)
    for i in candidate_list:
        if i["compare_value"] == min_value:
            print(i["routers"])
            return i["routers"]

def step_6(result_5_step):
    district_num = len(result_5_step["mds"])
    Vx = []  # 最小点覆盖中不属于极小支配集中的点
    Vy = []  # 极小支配集中的点
    for i in result_5_step["mds"]:
        Vy.append(i)
    for i in result_5_step["mvc"]:
        if i not in result_5_step["mds"]:
            Vx.append(i)
    for i in Vx:
        min_dis = 1000000
        shortest_edge = {}
        for j in ROUTER_LIST[i].edge_info:
            if j["end_num"] in Vy and min_dis > j["len"] and j["len"] >= 0:
                min_dis = j["len"]
                shortest_edge = j
        ROUTER_LIST[i].first_district_edge = shortest_edge
        ROUTER_LIST[i].first_district_num = result_5_step["mds"].index(ROUTER_LIST[i].first_district_edge["end_num"])
    for i in Vy:
        ROUTER_LIST[i].first_district_edge = {"len": 0}
        ROUTER_LIST[i].first_district_num = result_5_step["mds"].index(i)

def step_7(result_5_step):
    district_num = len(result_5_step["mds"])
    Vx_list = [[] for i in range(district_num)]  # Vx按区的分组
    for i in result_5_step["mvc"]:
        if i not in result_5_step["mds"]:
            Vx_list[int(ROUTER_LIST[i].first_district_num)].append(i)

    # 初始化Vz
    Vz = []
    for i in range(ROUTER_NUM):
        if i not in result_5_step["mvc"]:
            Vz.append(i)

    for i in Vz:
        compare_list = []
        for j in range(district_num):  # j表示分区
            min_dis_xz = 10000000
            shortest_link = {}
            for k in ROUTER_LIST[i].edge_info:
                if k["end_num"] in Vx_list[j] and min_dis_xz > k["len"] and k["len"] > 0:
                    min_dis_xz = k["len"]


            min_dis_zy = 10000000
            for k in ROUTER_LIST[i].edge_info:
                if k["end_num"] == result_5_step["mds"][j] and min_dis_zy > k["len"] and k["len"] > 0:
                    min_dis_zy = k["len"]
                    shortest_link = k
            if min_dis_zy == 10000000:
                continue
            compare_list.append({"min_xz": min_dis_xz,
                                 "min_zy": min_dis_zy,
                                 "compare_value": alpha*min_dis_xz+(1-alpha)*min_dis_zy,
                                 "district": j,
                                 "shortest_link": shortest_link})

        value_list = []
        for j in compare_list:
                value_list.append(j["compare_value"])

        print(compare_list)
        print(i, value_list)
        # 求首选分区和链路
        min_value = min(value_list)  # 每个点在不同分区的值的最小值
        for j in compare_list:
            if j["compare_value"] == min_value and j["min_zy"] != 10000000:
                ROUTER_LIST[i].first_district_num = j["district"]
                ROUTER_LIST[i].first_district_edge = j["shortest_link"]
                compare_list.remove(j)
                break
        value_list.remove(min_value)

        # 求第二分区和链路
        # min_value = min(value_list)  # 每个点在不同分区的值的最小值
        # for j in compare_list:
        #     if j["compare_value"] == min_value:
        #         ROUTER_LIST[i].second_district_num = j["district"]
        #         ROUTER_LIST[i].second_district_edge = j["shortest_link"]
        #         compare_list.remove(j)
        #         break
        # value_list.remove(min_value)
        #
        # # 求第三分区和链路
        # if len(value_list) > 0 and district_num >= 3:
        #     min_value = min(value_list)  # 每个点在不同分区的值的最小值
        #     for j in compare_list:
        #         if j["compare_value"] == min_value:
        #             ROUTER_LIST[i].third_district_num = j["district"]
        #             ROUTER_LIST[i].third_district_edge = j["shortest_link"]
        #             break
    for i in range(ROUTER_NUM):
        print("num:{}, district:{}, link:{}".format(i, ROUTER_LIST[i].first_district_num,
                                                    ROUTER_LIST[i].first_district_edge))

def evaluation(p=p):
    num = 0
    P_1 = 0
    for i in range(ROUTER_NUM):
        if ROUTER_LIST[i].first_district_edge["len"] == 0:
            continue
        else:
            num += 1
            W = ROUTER_LIST[i].first_district_edge["len"] / 100
            P_1 = 1 - (1 - p) ** W + P_1
    if num == 0:
        return 0
    else:
        P_1_ave = P_1 / num

    return P_1_ave

def ave_len():
    num = 0
    length = 0
    max_length = 0
    for i in range(ROUTER_NUM):
        if ROUTER_LIST[i].first_district_edge["len"] == 0:
            continue
        else:
            num += 1
            length = length + ROUTER_LIST[i].first_district_edge["len"]
            if ROUTER_LIST[i].first_district_edge["len"] > max_length:
                max_length = ROUTER_LIST[i].first_district_edge["len"]
    if num == 0:
        return 0
    else:
        ave_length = length / num

    return max_length, ave_length



if __name__ == '__main__':
    EDGE_NUM = init_router()  # 初始化路由器信息，并计算边的总数。
    # print(EDGE_NUM)
    # for i in range(11):
    #     print(ROUTER_LIST[i].edge_info)
    mvc_list = mvc()  # 最小点覆盖列表
    mds_list = mds()  # 极小支配集
    result_3_step = step_3(mvc_list, mds_list)

    result_4_step = step_4(result_3_step)

    result_5_step = step_5(result_4_step)

    step_6(result_5_step)

    step_7(result_5_step)

    # 评估
    if os.path.exists("same_control_nsf.txt"):
        os.remove("same_control_nsf.txt")
    for i in range(11):
        P_1 = evaluation(i * 0.01)
        f = open("same_control_nsf.txt", 'a')
        f.write('{}\n'.format(P_1))
        f.close()
        print("百公里光纤故障概率为{}时，故障发生概率为：{}".format(i * 0.01, P_1))

    # 求最长控制链路、平均链路长度
    max_control_len, ave_control_len = ave_len()
    print("最长控制链路为：{},平均链路长度为：{}".format(max_control_len, ave_control_len))