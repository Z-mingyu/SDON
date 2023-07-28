import string
from itertools import combinations
import math
import os
import sys
import json
import random
sys.path.append("..")
import parameter

class Router():
    def __init__(self):
        self.num = int  # 自身路由器编号
        self.edge_info = []  #  (对方路由器编号，长度，边的编号) 长度为0代表自己，长度为-1为不可达
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

#更改地图时需要改变的两个变量
ROUTER_NUM = parameter.ROUTER_NUM  #11为cost239拓扑个数, 14为NSF拓扑的个数
map_file_name = parameter.map_file_name

ROUTER_LIST = [Router() for i in range(ROUTER_NUM)]
EDGE_NUM = 0
alpha = 0.5
a = [[] for i in range(ROUTER_NUM)]
alphabet = [str(i) for i in range(ROUTER_NUM)]
T_cs = 0  # 可以通过调整该值，来影响控制器(V_pc)的个数
V_pc = []  # 控制器部署节点
V_cc = []  # 管控中心
P_1 = 0.20  # 用户可以接受的最大故障概率
p = 0.02  # 光纤百公里故障概率

def init_map():
    f = open(map_file_name, "r", encoding="utf-8")
    lines = f.readlines()
    for i in range(len(a)):
        a[i].clear()
    # 从文件中读取边的信息并保存
    for i in range(0, ROUTER_NUM):  # i为路由器本身编号

        for edge_len in lines[i].split():
            edge_len = int(edge_len.strip(string.whitespace))
            if edge_len == -1:
                a[i].append(0)
            else:
                a[i].append(edge_len)
    f.close()

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
    # for i in range(ROUTER_NUM):
    #     for j in range(ROUTER_NUM):
    #         ROUTER_LIST[i].end_to_end_info
    return edge_num

def floyd_algorithm():

    init_map()
    # print(a)
    path = [[] for i in range(ROUTER_NUM)]
    path_info = [[] for i in range(ROUTER_NUM)]
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            path[i].append(j)
            path_info[i].append([])

    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):

            if a[i][j] == -1:
                a[i][j] = 10000000
                path[i][j] = -1
            if a[i][j] == 0:
                path[i][j] = -1
                a[i][j] = 10000000
            if i == j:
                a[i][j] = 0


    for k in range(ROUTER_NUM):
        for i in range(ROUTER_NUM):
            for j in range(ROUTER_NUM):
                if a[i][j] > a[i][k] + a[k][j]:
                    a[i][j] = a[i][k] + a[k][j]
                    path[i][j] = k
    # 计算完成后，二维矩阵a表示最短路径长度
    print(a)

    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            path_info[i][j].append(i)
            path_info[i][j].append(j)

            temp = path[i][j]
            if temp not in path_info[i][j]:
                path_info[i][j].insert(1, temp)
            while path[i][temp] != temp:
                temp = path[i][temp]
                path_info[i][j].insert(1, temp)


    # print(path_info)


    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            ROUTER_LIST[i].end_to_end_info[str(j)] = []
            if i == j:
                continue
            else:
                # print("{}到{}的路径为：{}".format(i, j, path_info[i][j]))
                pass
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            if a[i][j] < T_cs:    # 将不满足时延要求的路径排除
                ROUTER_LIST[i].end_to_end_info[str(j)].append(path_info[i][j])  # 传入信息到全局变量中

    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            if a[i][j] > T_cs:
                a[i][j] = -1

    # 将路径信息添加进文件，以便动态显示算法过程
    if os.path.exists("step_3.json"):
        os.remove("step_3.json")
    path_info_save = {i: [] for i in range(ROUTER_NUM)}
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            if a[i][j] > T_cs:
                path_info_save[i].append(-1)  # 这样使得json文件中0表示相同节点间的权值
            else:
                path_info_save[i].append(a[i][j])
    path_info_json = json.dumps(path_info_save)
    with open("step_3.json", 'a') as f:
        json.dump(path_info_json, f)

    return path_info

def find(temp, alphabet, index):
    min_len = 100000
    number = -1
    for i in range(len(alphabet)):
        if temp[i] > 0 and temp[i] < min_len and index.count(i) == 0:
            min_len = temp[i]
            number = i
    return min_len, number

# 使用Dijstar扩展算法，寻找所有无环路径
def find_all_path(start, end, vcc_flag):  # start中途不会改变，source会改变
    init_map()
    path_info = []  # start到end节点的无重复路径信息

    flag = 1  # 0为不能到达目的地,1为能到达目的地

    while flag:
        temp = []
        path = []
        index = []  # 已经选过的节点
        last_point = {}  # 到达某一节点的前一个点
        source = start

        for i in range(len(alphabet)):
            last_point[alphabet[i]] = source

        index = [alphabet.index(source)]
        temp = a[alphabet.index(source)][:]
        for i in range(len(alphabet)):
            x, number = find(temp, alphabet, index)  # x为最短路径的长度，number为最短路径对端编号
            if number == -1:
                break
            index.append(number)
            source = alphabet[number]
            for j in range(len(alphabet)):
                if index.count(j) == 0:
                    if temp[j] == 0 and a[number][j] != 0:
                        temp[j] = temp[j] + a[number][j] + x
                        last_point[alphabet[j]] = source
                    if temp[j] == 0 and a[number][j] == 0:
                        temp[j] = 0
                    if temp[j] != 0 and a[number][j] != 0:

                        if temp[j] > a[number][j] + x:
                            temp[j] = a[number][j] + x
                            last_point[alphabet[j]] = source

        choosed_path = []
        # print(alphabet[i], "的路径是：")

        if a[int(end)][int(last_point[end])] == 0:
            flag = 0

        if flag:
            k = last_point[end]
            while k != start:
                path.append(k)
                m = last_point[k]
                k = m
            path.append(start)
            for j in range(len(path)):
                # print(path[len(path) - j - 1], '-->')
                choosed_path.append(path[len(path) - j - 1])
            choosed_path.append(end)
            path_info.append(choosed_path)

            for j in range(len(choosed_path) - 1):  # 将选过的边权值置为0
                a[int(choosed_path[j])][int(choosed_path[j+1])] = 0
                a[int(choosed_path[j+1])][int(choosed_path[j])] = 0

            # print(int(end))
            # print("----------------------------")
            path.clear()

    # print(path_info)
    if vcc_flag == False:
        ROUTER_LIST[int(start)].end_to_end_info[end] = []
        for path_list in path_info:
            len_temp = 0
            front_index = -1
            for front_node in path_list:
                front_index += 1
                if front_index != len(path_list)-1:
                    last_node = path_list[front_index+1]
                    for i in ROUTER_LIST[int(front_node)].edge_info:
                        if i["end_num"] == int(last_node):
                            len_temp = len_temp + i["len"]
            # print(len_temp, path_list)
            # if len_temp < T_cs:    # 将不满足时延要求的路径排除
            if path_list not in ROUTER_LIST[int(start)].end_to_end_info[end]:
                ROUTER_LIST[int(start)].end_to_end_info[end].append(path_list)  # 传入信息到全局变量中
    else:
        return path_info

def divide_groups():
    print(a)
    b = [[] for i in range(ROUTER_NUM)]
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            b[i].append(j)
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            if a[i][j] <= 0:
                b[i][j] = -1
    print(b)
    groups = []
    join_flag = False
    unchoosed_nodes = [i for i in range(ROUTER_NUM)]
    start_node = -1
    while len(unchoosed_nodes) > 0:
        start_node = start_node + 1
        sub_group = [start_node]
        if start_node not in unchoosed_nodes:
            continue
        else:
            unchoosed_nodes.remove(start_node)


        for time in range(ROUTER_NUM):
            for i in range(ROUTER_NUM):
                if i != start_node and i in unchoosed_nodes:
                    for j in sub_group:
                        if a[i][j] > 0:
                            unchoosed_nodes.remove(i)
                            if i not in sub_group:
                                sub_group.append(i)
                            break

        groups.append(sub_group)

    print("分组为：", groups)
    return groups

# 极小支配集
def mds():
    temp = [i for i in range(0, ROUTER_NUM)]  # [0,1,...,10]

    result_list = []  # 结果的存储列表

    # 1、穷举法，寻找所有支配集
    for i in range(1, len(temp)):
        # print(i)
        if result_list != []:
            break
        if i < len(groups):
            continue

        candidate_list = list(combinations(temp, i))
        for j in candidate_list:  # j ->  (1,2,...)
            router_temp = []
            result_flag = True  # 标识是否是支配集
            for k in j:
                for l in range(ROUTER_NUM):
                    if a[k][l] != -1 and a[k][l] < T_cs:
                        router_temp.append(l)


            # 检测是否含有所有的路由器
            for m in temp:
                if m not in router_temp:
                    result_flag = False
                    break

            if result_flag:
                for k in j:
                    for l in range(ROUTER_NUM):
                        if a[k][l] != -1 and a[k][l] < T_cs:
                            router_temp.remove(l)
                    for m in temp:
                        if m not in router_temp:
                            result_flag = False
                            break

                    if result_flag:
                        break
                    else:
                        result_flag = True
                        for l in range(ROUTER_NUM):
                            if a[k][l] != -1 and a[k][l] < T_cs:
                                router_temp.append(l)
                        if j.index(k) == len(j)-1:
                            result_list.append(j)

    # 2、寻找最小个数的极小支配集
    min_mds_len = len(temp)
    for i in result_list:
        if len(i) <= min_mds_len:
            min_mds_len = len(i)
    result = []
    for i in result_list:
        if len(i) == min_mds_len:
            result.append(i)

    # 3、寻找最大边数的极小支配集
    final_result = []
    max_edge_num = 0
    print('result:',result)
    for i in result:  # i -> (1, 3, 6)
        valuable_edge_num = 0
        for j in i:
            for l in range(ROUTER_NUM):
                if a[j][l] != -1 and a[j][l] < T_cs:
                    valuable_edge_num += 1
        if valuable_edge_num > max_edge_num:
            final_result = i
            max_edge_num = valuable_edge_num


    return list(final_result)

# 分布式计算极小支配集
def distribute_mds():
    mds_list = []  # 最终结果
    for group in groups:
        temp_result_list = []
        for i in range(len(group)+1):
            if temp_result_list != []:
                break
            candidate_list = list(combinations(group, i))
            for j in candidate_list:  # j ->  (1,2,...)
                result_flag = True
                peer_router = []
                for k in j:
                    for l in group:
                        if a[k][l] != -1 and a[k][l] < T_cs:
                            if l not in peer_router:
                                peer_router.append(l)
                        if k == l:
                            if l not in peer_router:
                                peer_router.append(l)
                for k in group:
                    if k not in peer_router:
                        result_flag = False
                        break
                if result_flag:
                    temp_result_list.append(j)

        # 2、寻找最小个数的极小支配集
        # print('result:', temp_result_list)
        min_mds_len = len(group)
        for i in temp_result_list:
            if len(i) <= min_mds_len:
                min_mds_len = len(i)
        result = []
        for i in temp_result_list:
            if len(i) == min_mds_len:
                result.append(i)


        # 3、寻找最大边数的极小支配集
        final_result = []
        max_edge_num = 0
        # print('result:', result)
        for i in result:  # i -> (1, 3, 6)
            valuable_edge_num = 0
            for j in i:
                for l in range(ROUTER_NUM):
                    if a[j][l] != -1 and a[j][l] < T_cs:
                        valuable_edge_num += 1
            if valuable_edge_num > max_edge_num:
                final_result = i
                max_edge_num = valuable_edge_num
        for i in final_result:
            mds_list.append(i)
        # if len(group) == 1:
        #     mds_list.append(group[0])
    return mds_list

# 该算法暂时不考虑保护链路，因此只能求出主链路
def find_control_link():
    for i in range(ROUTER_NUM):
        if i in V_pc:
            continue
        arrival_links = []  # 可到达改点的所有路径
        min_len = 1000000  # 最短路径长度
        control_num = i  # 相应控制器编号
        for j in range(ROUTER_NUM):
            if i == j:
                continue
            if a[i][j] < min_len and a[i][j] != -1 and j in V_pc:
                min_len = a[i][j]
                control_num = j

        master_link_len = min_len
        master_link = path_info[control_num][i]
        # master_link, master_link_len = find_min_len_link(arrival_links)
        ROUTER_LIST[i].master_link = {"link": master_link, "len": master_link_len}

    # 将控制链路加入文件中，以便画图

    control_links = []
    control_node = {}  # 每个节点的控制节点，用字典表示
    for i in range(ROUTER_NUM):
        if ROUTER_LIST[i].master_link == {}:
            continue
        for j in range(len(ROUTER_LIST[i].master_link["link"])-1):
            control_node[i] = ROUTER_LIST[i].master_link["link"][0]

            k = j+1
            temp_links = []

            # 将端对端链路中编号较小的节点放在前面
            if ROUTER_LIST[i].master_link["link"][j] < ROUTER_LIST[i].master_link["link"][k]:
                temp_links = [ROUTER_LIST[i].master_link["link"][j], ROUTER_LIST[i].master_link["link"][k]]
            else:
                temp_links = [ROUTER_LIST[i].master_link["link"][k], ROUTER_LIST[i].master_link["link"][j]]
            if temp_links not in control_links:
                control_links.append(temp_links)

    return control_links, control_node

def find_min_len_link(arrival_links):
    min_len_link = []
    min_len = 1000000  # 最小长度
    for i in arrival_links:
        len_temp = 0
        for j in range(len(i)-1):  # i->['0', '8', '6'],i若长度为3，则j取0，1
            for k in ROUTER_LIST[int(i[j])].edge_info:
                if k["end_num"] == int(i[j+1]):
                    len_temp = len_temp + k["len"]
                    break
        if len_temp < min_len:
            min_len = len_temp
            min_len_link = i
    return min_len_link, min_len

def evaluation(p=p):
    num = 0
    P_1 = 0
    for i in range(ROUTER_NUM):

        if ROUTER_LIST[i].master_link == {}:
            continue
        else:
            num += 1
            W = ROUTER_LIST[i].master_link["len"]/100
            P_1 = 1-(1-p)**W + P_1
    if num == 0:
        return 0
    else:
        P_1_ave = P_1/num

    return P_1_ave

def find_W(P_1, p):  # 在指定时延下确定最长控制链路, P_1为用户可以接受的故障出现概率，p为光纤百公里故障概率
    W = 100*math.log(1-P_1)/math.log(1-p)
    return W

def ave_len():
    num = 0
    length = 0
    max_length = 0
    for i in range(ROUTER_NUM):

        if ROUTER_LIST[i].master_link == {}:
            continue
        else:
            num += 1
            length = length + ROUTER_LIST[i].master_link["len"]
            if ROUTER_LIST[i].master_link["len"] > max_length:
                max_length = ROUTER_LIST[i].master_link["len"]
    if num == 0:
        return 0
    else:
        ave_length = length / num

    return max_length, ave_length

def find_vcc():
    distance_list = []
    links_num_list = []
    for i in V_pc:
        links_num = 0
        for j in V_pc:
            links_num = links_num + len(ROUTER_LIST[i].end_to_end_info[str(j)])
        links_num_list.append(links_num)

    for i in V_pc:
        distance = 0
        for j in V_pc:
            if i == j:
                continue
            len_temp = 0
            front_index = -1

            for front_node in ROUTER_LIST[i].end_to_end_info[str(j)][0]:
                front_index += 1
                if front_index != len(ROUTER_LIST[i].end_to_end_info[str(j)][0]) - 1:
                    last_node = ROUTER_LIST[i].end_to_end_info[str(j)][0][front_index + 1]
                    for k in ROUTER_LIST[int(front_node)].edge_info:
                        if k["end_num"] == int(last_node):
                            len_temp = len_temp + k["len"]

            distance = distance + len_temp
        distance_list.append(distance)
    max_distance = max(distance_list)
    min_distance = min(distance_list)
    max_links_num = max(links_num_list)
    score_list = []
    for i in range(len(V_pc)):
        if max_distance == min_distance:
            score = (1-P_1) + P_1*links_num_list[i]/max_links_num
        else:
            score = P_1*((max_distance-distance_list[i])/(max_distance-min_distance)) + (1-P_1)*links_num_list[i]/max_links_num
        score_list.append(score)
    print("各控制器的得分为：{}".format(score_list))
    vcc = V_pc[score_list.index(max(score_list))]
    vcc_vpc_links_len = distance_list[score_list.index(max(score_list))]/(len(V_pc) - 1)
    vcc_vpc_links_ave_num = links_num_list[score_list.index(max(score_list))]/(len(V_pc) - 1)

    print("最多平均控制链路数：{}".format(max(links_num_list)/(len(V_pc) - 1)))
    f_vcc = V_pc[distance_list.index(min_distance)]
    f_vcc_vpc_links_len = min_distance/(len(V_pc) - 1)
    f_vcc_vpc_links_ave_num = links_num_list[distance_list.index(min_distance)]/(len(V_pc) - 1)
    print("只依靠时延情况下：V_cc部署在点:{},链路总长度为{},平均控制链路数为{}".format(f_vcc, f_vcc_vpc_links_len, f_vcc_vpc_links_ave_num))

    # 随机部署
    # vcc_index = random.randint(0, len(V_pc) - 1)
    # # f_vcc = V_pc[vcc_index]
    # # f_vcc_vpc_links_len = distance_list[vcc_index]/(len(V_pc) - 1)
    # # f_vcc_vpc_links_ave_num = links_num_list[vcc_index] / (len(V_pc) - 1)
    # print("随机部署情况下：V_cc部署在点:{},链路总长度为{},平均控制链路数为{}".format(f_vcc, f_vcc_vpc_links_len, f_vcc_vpc_links_ave_num))


    # 将控制链路写入文件，方便画图
    vcc_control_links = []
    for i in V_pc:
        if i == vcc:
            continue
        for j in range(len(ROUTER_LIST[i].end_to_end_info[str(vcc)][0])-1):
            k = j+1
            temp_links = []
            # 将端点值小的放在前面
            if int(ROUTER_LIST[i].end_to_end_info[str(vcc)][0][j]) < \
                    int(ROUTER_LIST[i].end_to_end_info[str(vcc)][0][k]):
                temp_links = [int(ROUTER_LIST[i].end_to_end_info[str(vcc)][0][j]),
                              int(ROUTER_LIST[i].end_to_end_info[str(vcc)][0][k])]
            else:
                temp_links = [int(ROUTER_LIST[i].end_to_end_info[str(vcc)][0][k]),
                              int(ROUTER_LIST[i].end_to_end_info[str(vcc)][0][j])]
            if temp_links not in vcc_control_links:
                vcc_control_links.append(temp_links)

    return vcc, vcc_vpc_links_len, vcc_vpc_links_ave_num, vcc_control_links

# 将拓扑信息转化为json文件
def topo_json():
    if os.path.exists("topo_info.json"):
        os.remove("topo_info.json")

    topo_info = {"control_links": control_links,
                 "vcc_control_links": vcc_control_links,
                 "control_node": control_node,
                 "v_pc": V_pc,
                 "v_cc": V_cc,
                 "T_cs": T_cs}
    topo_info_json = json.dumps(topo_info)

    with open("topo_info.json", 'a') as f:
        json.dump(topo_info_json, f)


if __name__ == '__main__':
    # 1、在指定概率下确定最长控制链路长度
    T_cs = find_W(P_1, p)
    print('最长控制链路长度为{}'.format(T_cs))

    EDGE_NUM = init_router()  # 初始化路由器信息，并计算边的总数。
    # print(a)
    path_info = floyd_algorithm()
    # # print("共有{}条边".format(EDGE_NUM))
    # # for i in range(11):
    # #     print(ROUTER_LIST[i].edge_info)
    # for start in range(ROUTER_NUM):
    #     for end in range(ROUTER_NUM):
    #         find_all_path(str(start), str(end), False)  # start, source, end
    #     # print(ROUTER_LIST[start].end_to_end_info)
    #
    groups = divide_groups()

    # V_pc = mds()
    V_pc = distribute_mds()
    print('V_pc部署在{}'.format(V_pc))

    # for i in range(ROUTER_NUM):
    #     print(ROUTER_LIST[i].end_to_end_info)
    #
    control_links, control_node = find_control_link()

    # 输出所有节点的控制链路
    for i in range(ROUTER_NUM):
        print("{}号点的控制链路：".format(i))
        print("主链路：{}".format(ROUTER_LIST[i].master_link))
        print("----------------------")


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


    # 清空信息，寻找vcc
    for i in range(ROUTER_NUM):
        ROUTER_LIST[i].end_to_end_info = {}
    for start in V_pc:
        for end in V_pc:
            find_all_path(str(start), str(end), False)  # start, source, end
        # print(ROUTER_LIST[start].end_to_end_info)
    V_cc,vcc_vpc_links_len, vcc_vpc_links_ave_num, vcc_control_links = find_vcc()
    print("V_cc部署在点:{},链路总长度为{},平均控制链路数为{}".format(V_cc,vcc_vpc_links_len, vcc_vpc_links_ave_num))

    # 将拓扑信息写入json文件
    topo_json()