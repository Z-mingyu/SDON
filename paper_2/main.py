import string
from itertools import combinations
import os
import sys
import json
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
T_cs = 20*200  # 可以通过调整该值，来影响控制器(V_pc)的个数
V_pc = []  # 控制器部署节点
V_cc = []  # 管控中心
p = 0.02  # 光纤百公里故障概率

def init_map():
    f = open(map_file_name, "r", encoding="utf-8")
    lines = f.readlines()
    for i in range(len(a)):
        a[i].clear()
    # 从文件中读取边的信息并保存
    for i in range(0, lines.__len__()):  # i为路由器本身编号

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

def find(temp, alphabet, index):
    min_len = 100000
    number = -1
    for i in range(len(alphabet)):
        if temp[i] > 0 and temp[i] < min_len and index.count(i) == 0:
            min_len = temp[i]
            number = i
    return min_len, number

# 使用Dijstar扩展算法，寻找所有满足步骤一中的路径
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

        if a[int(end)][int(last_point[end])] == 0 or a[int(last_point[end])][int(end)] == 0:
            flag = 0

        if flag != 0:
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
            path = []

    #print(path_info)
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
            if len_temp < T_cs:    # 将不满足时延要求的路径排除
                ROUTER_LIST[int(start)].end_to_end_info[end].append(path_list)  # 传入信息到全局变量中
    else:
        return path_info

def find_V_pc():   # 确定控制器部署节点
    candidate_list = []
    for i in range(ROUTER_NUM):
        V_pc_flag = True
        for j in range(ROUTER_NUM):
            if len(ROUTER_LIST[i].end_to_end_info[str(j)]) < 2 and j != i:
                V_pc_flag = False
        if V_pc_flag:
            candidate_list.append(i)
    # print(candidate_list)
    if len(candidate_list) == 0:  # 如果没有节点能覆盖全图
    # 因为有多个控制器，所以返回一个列表。
        nodes = [i for i in range(ROUTER_NUM)]
        for i in range(2, ROUTER_NUM+1):
            combinations_list = list(combinations(nodes, i))
            for j in combinations_list:  # j -> (1, 2, 3)
                compare_list = list(j)  # 用来判断是否可以覆盖全图
                for k in j:
                    for l in range(ROUTER_NUM):
                        if len(ROUTER_LIST[k].end_to_end_info[str(l)]) >= 2 and l not in compare_list:
                            compare_list.append(l)
                if len(compare_list) == ROUTER_NUM:
                    return list(j)


    elif len(candidate_list) == 1: # 如果只有一个节点能覆盖全图，且到达其他节点均有两条以上的路径
        return candidate_list

    else:  # 如果有多个节点均能覆盖全图，且到达其他节点均有两条以上的路径
        max_link_num = 0
        link_num_temp = 0
        V_pc_temp = ROUTER_NUM + 1
        for i in candidate_list:
            for j in range(ROUTER_NUM):
                link_num_temp = link_num_temp + len(ROUTER_LIST[i].end_to_end_info[str(j)])
            # print(i, link_num_temp)
            if link_num_temp >= max_link_num:
                V_pc_temp = i
                max_link_num = link_num_temp
            link_num_temp = 0
        return [V_pc_temp]

def find_V_cc(V_pc):  # 穷举法寻找部署位置
    min_dis = 100000
    V_cc_temp = ROUTER_NUM

    for i in V_pc:
        len_temp = 0
        arrival_flag = True
        for j in V_pc:

            k = find_all_path(str(i), str(j), True)  # 寻找每个节点到其他节点的最短路径
            if len(k) == 0 and i != j:
                arrival_flag = False
                break
            elif len(k) == 0 and i == j:
                continue
            l = k[0]  # l -> [0,2,8]  此处可以记录路径
            front_index = -1
            for front_node in l:
                front_index += 1
                if front_index != len(l) - 1:
                    last_node = l[front_index + 1]
                    for m in ROUTER_LIST[int(front_node)].edge_info:
                        if m["end_num"] == int(last_node):
                            len_temp = len_temp + m["len"]

        if len_temp < min_dis and arrival_flag:
            min_dis = len_temp
            V_cc_temp = i

    return V_cc_temp, min_dis

# vcc中专用函数
def vcc_find_all_path(start, end):  # start中途不会改变，source会改变
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

        if a[int(end)][int(last_point[end])] == 0 or a[int(last_point[end])][int(end)] == 0:
            flag = 0

        if flag != 0:
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
            path = []

    print(path_info)
    return path_info


def find_control_link():
    for i in range(ROUTER_NUM):
        if i in V_pc:
            continue
        arrival_links = []
        for j in V_pc:  # 将所有可以到达V_pc的路径归纳起来（到达任意一个V_pc的路径至少要有两条）
            if len(ROUTER_LIST[i].end_to_end_info[str(j)]) >= 2:
                for k in ROUTER_LIST[i].end_to_end_info[str(j)]:
                    arrival_links.append(k)

        master_link, master_link_len = find_min_len_link(arrival_links)
        ROUTER_LIST[i].master_link = {"link": master_link, "len": master_link_len}


        # 1、确定控制器
        control = master_link[len(master_link)-1]  # 取最后一个为控制器部署节点

        # 2、将主链路从arrival_links中删除
        arrival_links.remove(master_link)


        # 3、将不包含第一步中的控制器的路径删除
        remove_links = []
        for link in arrival_links:
            if control not in link:
                remove_links.append(link)
        for link in remove_links:
            arrival_links.remove(link)

        # 4、寻找从链路
        slave_link, slave_link_len = find_min_len_link(arrival_links)
        ROUTER_LIST[i].slave_link = {"link": slave_link, "len": slave_link_len}

    # 将控制链路加入文件中，以便画图

    control_links = []
    for i in range(ROUTER_NUM):
        if ROUTER_LIST[i].master_link == {}:
            continue
        print("ROUTER_CONTROL_LINK", ROUTER_LIST[i].master_link)
        for j in range(len(ROUTER_LIST[i].master_link["link"]) - 1):
            k = j + 1
            temp_links = []
            # 将端对端链路中编号较小的节点放在前面
            if int(ROUTER_LIST[i].master_link["link"][j]) < int(ROUTER_LIST[i].master_link["link"][k]):
                temp_links = [int(ROUTER_LIST[i].master_link["link"][j]), int(ROUTER_LIST[i].master_link["link"][k])]
            else:
                temp_links = [int(ROUTER_LIST[i].master_link["link"][k]), int(ROUTER_LIST[i].master_link["link"][j])]
            if temp_links not in control_links:
                control_links.append(temp_links)

    return control_links

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

    return  max_length, ave_length

def find_vcc_control_links():
    # 将控制链路写入文件，方便画图
    vcc_control_links = []
    for i in vcc_control_links_without_worked:
        for j in range(len(i)-1):
            k = j + 1
            temp_links = []
            if i[j] < i[k]:
                temp_links = [i[j], i[k]]
            else:
                temp_links = [i[k], i[j]]
        if temp_links not in vcc_control_links:
            vcc_control_links.append(temp_links)

    return vcc_control_links

# 将拓扑信息转化为json文件
def topo_json():
    if os.path.exists("topo_info.json"):
        os.remove("topo_info.json")

    topo_info = {"control_links": control_links,
                 "vcc_control_links": vcc_control_links,
                 "v_pc": V_pc,
                 "v_cc": V_cc}
    topo_info_json = json.dumps(topo_info)

    with open("topo_info.json", 'a') as f:
        json.dump(topo_info_json, f)

if __name__ == '__main__':
    EDGE_NUM = init_router()  # 初始化路由器信息，并计算边的总数。
    # print("共有{}条边".format(EDGE_NUM))
    # for i in range(11):
    #     print(ROUTER_LIST[i].edge_info)


    for start in range(ROUTER_NUM):
        for end in range(ROUTER_NUM):
            find_all_path(str(start), str(end), False)  # start, source, end
        print(ROUTER_LIST[start].end_to_end_info)
    V_pc = find_V_pc()
    print("V_pc部署在{}".format(V_pc))

    vcc_control_links_without_worked = []  # 未处理的vcc控制链路数据
    if len(V_pc) > 1:  # 如果多于1个控制器，则寻找部署管控中心的节点
        V_cc, min_dis = find_V_cc(V_pc)
        vcc_vpc_links_num = 0
        for i in V_pc:
            path_info = vcc_find_all_path(str(V_cc), str(i))
            if path_info != []:
                vcc_control_links_without_worked.append(path_info[0])
            vcc_vpc_links_num += len(path_info)
        vcc_vpc_links_ave_num = vcc_vpc_links_num/(len(V_pc)-1)
    else:
        V_cc = V_pc[0]
        min_dis = 0
        vcc_vpc_links_ave_num = 0


    control_links = find_control_link()


    vcc_control_links = find_vcc_control_links()

    # 输出所有节点的控制链路
    for i in range(ROUTER_NUM):
        print("{}号点的控制链路：".format(i))
        print("主链路：{}".format(ROUTER_LIST[i].master_link))
        print("保护链路：{}".format(ROUTER_LIST[i].slave_link))
        print("----------------------")

    # 评估
    if os.path.exists("same_control_nsf.txt"):
        os.remove("same_control_nsf.txt")
    for i in range(11):
        P_1 = evaluation(i*0.01)
        f = open("same_control_nsf.txt", 'a')
        f.write('{}\n'.format(P_1))
        f.close()
        print("百公里光纤故障概率为{}时，故障发生概率为：{}".format(i*0.01, P_1))

    # 求最长控制链路、平均链路长度
    max_control_len, ave_control_len = ave_len()
    print("最长控制链路为：{},平均链路长度为：{}".format(max_control_len, ave_control_len))

    print("V_cc部署在{}, 链路总长度为{},平均控制链路数为{}".format(V_cc, min_dis, vcc_vpc_links_ave_num))

    topo_json()