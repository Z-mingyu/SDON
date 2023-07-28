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
        self.edge_info = []  #  (相邻路由器编号，长度，边的编号) 长度为0代表自己，长度为-1为不可达
        self.neighbor_edge_num = int  # 相邻的边的数量
        self.end_to_end_info={}
        self.master_link = {}  # “link”:[], "len":[]; 下同

#更改网络拓扑时需要改变的两个变量
ROUTER_NUM = parameter.ROUTER_NUM  #11为cost239拓扑个数, 14为NSF拓扑的个数
map_file_name = parameter.map_file_name

ROUTER_LIST = [Router() for i in range(ROUTER_NUM)]
EDGE_NUM = 0

a = [[] for i in range(ROUTER_NUM)]
Failure_rate = [[] for i in range(ROUTER_NUM)]
for i in range(ROUTER_NUM):
    for j in range(ROUTER_NUM):
        Failure_rate[i].append(1)
alphabet = [str(i) for i in range(ROUTER_NUM)]

T_ms = 15 #控制链路端到端时延限制，
V_pc = []  # 控制器部署节点

P_1 = 0.20# 用户可以接受的最大故障概率
p = 0.02  # 光纤百公里故障概率


#将txt文件中的拓扑信息读取后存在数组二维a里面
def init_map():
    f = open(map_file_name, "r", encoding="utf-8")
    lines = f.readlines()
    for i in range(len(a)):
        a[i].clear()
    # 从文件中读取边的信息并保存
    for i in range(ROUTER_NUM):  # i为路由器本身编号

        for edge_len in lines[i].split():
            edge_len = int(edge_len.strip(string.whitespace))
            if edge_len == -1:
                a[i].append(-1)
            else:
                a[i].append(edge_len)
    f.close()

#初始化每个路由器，读取每条邻边的信息和邻边总数
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
                    #将不可达的边编号为0
                else:
                    edge_num += 1
                    ROUTER_LIST[i].edge_info.append({"end_num": end_num, "len": edge_len, "edge_num": edge_num})
                    #给每一条存在的边编号
            elif i > end_num:
                #寻找目的节点编号比当前节点小的边时，直接从目的节点的edge_info中寻找
                for j in ROUTER_LIST[end_num].edge_info:
                    if j["end_num"] == i:
                        ROUTER_LIST[i].edge_info.append({"end_num": end_num, "len": edge_len, "edge_num": j["edge_num"]})
                        if j["len"] != edge_len:
                            print("error：编号相等的边长度不相等",i,end_num)
                        break
            elif i == end_num:
                ROUTER_LIST[i].edge_info.append({"end_num": end_num, "len": edge_len, "edge_num": 0})
                #将自己到自己的边编号为0
            end_num += 1

    #找出每个节点的临边数量
    for i in range(ROUTER_NUM):
        peer_edge_num = 0
        for j in ROUTER_LIST[i].edge_info:
            if j["len"] > 0:
                peer_edge_num += 1
        ROUTER_LIST[i].neighbor_edge_num = peer_edge_num

    return edge_num

def floyd_algorithm():

    init_map()
    path = [[] for i in range(ROUTER_NUM)]
    path_info = [[] for i in range(ROUTER_NUM)]
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            path[i].append(j)
            path_info[i].append([])

    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):

            if a[i][j] == -1 or a[i][j]==0:
                a[i][j] = 10000000
                path[i][j] = -1
            if i == j:
                a[i][j] = 0

    #弗洛伊德算法将a变成最短路径矩阵，并将中转点存入path列表，方便打印路径
    for k in range(ROUTER_NUM):
        for i in range(ROUTER_NUM):
            for j in range(ROUTER_NUM):
                if a[i][j] > a[i][k] + a[k][j]:
                    a[i][j] = a[i][k] + a[k][j]
                    path[i][j] = k
    # 计算完成后，二维矩阵a表示最短路径长度
    #print(a)

    #根据path列表中存的最短路径上一节点的信息，将所有最短路径信息存入path_info列表
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
                # 打印最短路径
                #print("{}到{}的路径为：{}".format(i, j, path_info[i][j]))
                pass

    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            ROUTER_LIST[i].end_to_end_info[str(j)].append(path_info[i][j])  # 传入信息到全局变量中

    # 将路径信息添加进文件，以便动态显示算法过程
    if os.path.exists("step_3.json"):
        os.remove("step_3.json")
    path_info_save = {i: [] for i in range(ROUTER_NUM)}
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            if a[i][j] > T_ms*200:
                path_info_save[i].append(-1)  # 这样使得json文件中0表示相同节点间的权值
                a[i][j]=a[j][i]=-1
            else:
                path_info_save[i].append(a[i][j])
    path_info_json = json.dumps(path_info_save)
    with open("step_3.json", 'a') as f:
        json.dump(path_info_json, f)

    return path_info


#找出当前节点到其他所有节点的最短路径中距离最小的一条路径，返回这个值和对应目的节点编号
#temp为二维数组a的一个行向量
def find(temp, alphabet, index):
    min_len = 100000
    number = -1
    for i in range(len(alphabet)):
        if temp[i] > 0 and temp[i] < min_len and index.count(i) == 0:
            min_len = temp[i]
            number = i
    return min_len, number

# 使用Dijstar扩展算法，寻找所有无环路径
def find_all_path(start, end):  #start中途不会改变，source会改变
    init_map()
    path_info = []  # start到end节点的无重复路径信息

    flag = 1  # 0为不能到达目的地,1为能到达目的地

    while flag:
        path = []
        last_point = {}  # 到达某一节点的前一个点
        source = start

        for i in range(len(alphabet)):
            last_point[alphabet[i]] = source

        index = [alphabet.index(source)]  #已经选过的节点
        temp = a[alphabet.index(source)][:] #当前节点到其他所有节点的距离列表

        #用Dijstar算法算出当前节点到其他所有节点的最短距离，更新temp列表
        for i in range(len(alphabet)):
            x, number = find(temp, alphabet, index)  # x为列表temp中最短路径的长度，number为最短路径目的节点编号
            if number == -1:
                break
            index.append(number)
            source = alphabet[number]
            for j in range(len(alphabet)): #以number节点为中继节点，更新temp列表
                if index.count(j) == 0:
                    if temp[j] == -1 and a[number][j] != -1:
                        temp[j] = temp[j] + a[number][j] + x
                        last_point[alphabet[j]] = source
                    if temp[j] == -1 and a[number][j] == -1:
                        temp[j] = -1
                    if temp[j] != -1 and a[number][j] != -1:

                        if temp[j] > a[number][j] + x:
                            temp[j] = a[number][j] + x
                            last_point[alphabet[j]] = source

        choosed_path = []
        # print(alphabet[i], "的路径是：")

        #判断start->end之间还有没有路径，若没有了，则跳出while循环
        if a[int(end)][int(last_point[end])] == -1:
            flag = 0
        #print(last_point)
        if flag:
            k = last_point[end]
            #将end->start的路径存在path列表
            while k != start:
                path.append(k)
                m = last_point[k]
                k = m
            path.append(start)

            #将path倒序存在choosed_path列表，并将之添加到path_info列表
            for j in range(len(path)):
                # print(path[len(path) - j - 1], '-->')
                choosed_path.append(path[len(path) - j - 1])
            choosed_path.append(end)
            #if len(choosed_path)<5:
            path_info.append(choosed_path)

            # 将选过的边权值置为0，相当于删除start->end的最短路径
            for j in range(len(choosed_path) - 1):
                a[int(choosed_path[j])][int(choosed_path[j+1])] = -1
                a[int(choosed_path[j+1])][int(choosed_path[j])] = -1

            # print(int(end))
            # print("----------------------------")
    return path_info


#计算多条不重复路径的联合错误概率
def calculate_end_to_end_P(path_information,p,start,end):
    init_map()
    links_length=[]
    #根据不重复路径节点信息计算路径长度
    for link in path_information:
        length=0
        for i in range(len(link)-1):
            length+=a[int(link[i])][int(link[i+1])]
        if length<=T_ms*200:

            links_length.append(length)
    P=1
    #print(start,end,links_length)
    for l in links_length:
        P=P*(1-(1-p/100)**l)
    Failure_rate[start][end]=P
    if P<=P_1:
        return True
    else:
        return False

#按照生存性约束条件，将整个拓扑进行分组
def divide_groups():
    b = [[] for _ in range(ROUTER_NUM)]
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            b[i].append(1)
    _=floyd_algorithm()

    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            if a[i][j]==-1:
                b[i][j]=-1

    #对于矩阵b，将不满足生存性条件的边的权值置为-1
    for start in range(ROUTER_NUM):
        for end in range(ROUTER_NUM):
            path_info=find_all_path(str(start),str(end))
            #print(path_info)
            if not calculate_end_to_end_P(path_info,p,start,end) and start!=end:
                b[start][end] = -1
                b[end][start] = -1
    print('\n')
    # for i in range(ROUTER_NUM):
    #     print(b[i])


    groups = []
    unchoosed_nodes = [i for i in range(ROUTER_NUM)]
    start_node = -1
    while len(unchoosed_nodes) > 0:
        start_node = start_node + 1
        sub_group = [start_node]
        if start_node not in unchoosed_nodes:
            continue
        else:
            unchoosed_nodes.remove(start_node)


        for i in range(ROUTER_NUM):
            if i != start_node and i in unchoosed_nodes:
            #判断当前节点i和子集中节点有没有满足生存性要求的链路，有就将当前节点加入子集，没有就不加
                for j in sub_group:
                    if b[i][j] !=-1:
                        unchoosed_nodes.remove(i)
                        #if i not in sub_group:
                        sub_group.append(i)
                        for m in range(i):
                            if m in unchoosed_nodes:
                                for n in sub_group:
                                    if b[m][n] != -1:
                                        unchoosed_nodes.remove(m)
                                        # if i not in sub_group:
                                        sub_group.append(m)
                                        break
                        break



        groups.append(sub_group)
    print("分组为：", groups)
    return groups

# 分布式计算最小支配集
def Minimum_dominating_set():
    b = [[] for _ in range(ROUTER_NUM)]
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            b[i].append(1)
    _ = floyd_algorithm()

    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            if a[i][j] == -1:
                b[i][j] = -1
    # 对于矩阵b，将不满足生存性条件的边的权值置为-1
    for start in range(ROUTER_NUM):
        for end in range(ROUTER_NUM):
            path_info = find_all_path(str(start), str(end))
            #print(path_info)
            if not calculate_end_to_end_P(path_info, p,start,end):
                b[start][end] = -1
                b[end][start] = -1

    result_list = []  # 最终结果
    for group in groups:
        temp_result_list = []
        for i in range(1,len(group)+1):
            if temp_result_list != []:
                break
            candidate_list = list(combinations(group, i)) #combinations:返回从group中取i个元素的所有组合，type：tuple
            for j in candidate_list:
                result_flag = True
                peer_router = []

                #将group中的节点与组合j中的元素进行比较，如果有满足生存性的链路，则加入peer_router列表
                for k in j:
                    for l in group:
                        if b[k][l] != -1 :
                            if l not in peer_router:
                                peer_router.append(l)
                        if k == l:
                            if l not in peer_router:
                                peer_router.append(l)

                #判断group所有的元素是否都加入了peer_router列表
                for k in group:
                    if k not in peer_router:
                        result_flag = False
                        break

                #如果是，则j是一个支配集，加入临时支配集列表temp_result_list
                if result_flag:
                    temp_result_list.append(j)

        # 2、寻找最小个数的极小支配集
        # print('result:', temp_result_list)
        min_mds_len = len(group)
        for i in temp_result_list:
            if len(i) <= min_mds_len:
                min_mds_len = len(i)
        result = []

        #将数量最少的支配集加入result列表，可能有多个数量相同的最小支配集
        for i in temp_result_list:
            if len(i) == min_mds_len:
                result.append(i)


        # 3、寻找最大度数的极小支配集
        final_result = []
        max_edge_num = 0
        for i in result:  # i -> (1, 3, 6)
            valuable_edge_num = 0
            for j in i:
                for l in range(ROUTER_NUM):
                    if a[j][l] != -1 :
                        valuable_edge_num += 1
            if valuable_edge_num > max_edge_num:
                final_result = i
                max_edge_num = valuable_edge_num
        for i in final_result:
            result_list.append(i)

    return result_list

#该算法暂时不考虑保护链路，因此只能求出主链路
def find_control_link():
    for i in range(ROUTER_NUM):
        if i in V_pc:
            continue
        #arrival_links = []  # 可到达该点的所有路径
        min_len = 1000000  # 最短路径长度
        control_num = i  # 相应控制器编号
        for j in V_pc:
            if a[i][j] < min_len and a[i][j] != -1:
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

# def find_min_len_link(arrival_links):
#     min_len_link = []
#     min_len = 1000000  # 最小长度
#     for i in arrival_links:
#         len_temp = 0
#         for j in range(len(i)-1):  # i->['0', '8', '6'],i若长度为3，则j取0，1
#             for k in ROUTER_LIST[int(i[j])].edge_info:
#                 if k["end_num"] == int(i[j+1]):
#                     len_temp = len_temp + k["len"]
#                     break
#         if len_temp < min_len:
#             min_len = len_temp
#             min_len_link = i
#     return min_len_link, min_len

def evaluation():
    num = 0
    P_1 = 0
    for i in range(ROUTER_NUM):

        if ROUTER_LIST[i].master_link == {}:
            continue
        else:
            num += 1
            P_1 = Failure_rate[ROUTER_LIST[i].master_link['link'][0]][ROUTER_LIST[i].master_link['link'][-1]]+ P_1
            #print(P_1)
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

    return max_length, ave_length


#将拓扑信息转化为json文件
def topo_json():
    if os.path.exists("topo_info.json"):
        os.remove("topo_info.json")

    topo_info = {"control_links": control_links,
                 "control_node": control_node,
                 "v_pc": V_pc,
                 "T_ms": T_ms}
    topo_info_json = json.dumps(topo_info)

    with open("topo_info.json", 'a') as f:
        json.dump(topo_info_json, f)


if __name__ == '__main__':
    EDGE_NUM = init_router()  # 初始化路由器信息，并计算边的总数。
    init_map()
    # for i in range(ROUTER_NUM):
    #     print(a[i])




    groups = divide_groups()

    V_pc = Minimum_dominating_set()
    print('V_pc部署在{}'.format(V_pc))

    # for i in range(ROUTER_NUM):
    #     print(ROUTER_LIST[i].end_to_end_info)
    #

    path_info = floyd_algorithm()

    #打印最短路径矩阵
    # for i in range(ROUTER_NUM):
    #     print(a[i])

    control_links, control_node = find_control_link()
    #输出所有节点的控制链路
    for i in range(ROUTER_NUM):
        print("{}号点的控制链路：".format(i))
        print("主链路：{}".format(ROUTER_LIST[i].master_link))
        print("----------------------")


    # 评估
    if os.path.exists("same_control_nsf.txt"):
        os.remove("same_control_nsf.txt")

    P_1 = evaluation()
    f = open("same_control_nsf.txt", 'a')
    f.write('{}'.format(P_1))
    f.close()
    print("百公里光纤故障概率为{}时，故障发生概率为：{}".format(p, P_1))

    # 求最长控制链路、平均链路长度
    max_control_len, ave_control_len = ave_len()
    print("最长控制链路为：{},平均链路长度为：{}".format(max_control_len, ave_control_len))

    #打印节点间的联合链路故障概率
    # for i in range(ROUTER_NUM):
    #     for j in range(ROUTER_NUM):
    #         print(i,j,Failure_rate[i][j])
    #将拓扑信息写入json文件
    topo_json()