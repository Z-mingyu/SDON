# 该程序为两种算法部署结果比较图，左侧为新算法，右侧为以时延为约束条件的部署算法
import networkx as nx
import matplotlib.pyplot as plt
import parameter
import string
import json
import time

ROUTER_NUM = parameter.ROUTER_NUM
map_file_name = parameter.map_file_name

label_font_size = 16
node_size = 800

MAP = [[] for i in range(ROUTER_NUM)]
pos = []
if ROUTER_NUM == 11:
    pos = [(102, 169), (382, 54),
           (367, 137), (452, 242),
           (600, 130), (563, 364),
           (263, 374), (281, 279),
           (165, 289), (74, 394),
           (432, 486)]
elif ROUTER_NUM == 14:
    pos = [(100, 304), (40, 192),
           (96, 97), (145, 169),
           (203, 153), (275, 86),
           (262, 184), (325, 206),
           (411, 206), (412, 97),
           (407, 302), (491, 286),
           (448, 172), (496, 210)]

def init_map():
    f = open(map_file_name, "r", encoding="utf-8")
    lines = f.readlines()
    for i in range(ROUTER_NUM):
        MAP[i].clear()
    # 从文件中读取边的信息并保存
    for i in range(0, ROUTER_NUM):  # i为路由器本身编号

        for edge_len in lines[i].split():
            edge_len = int(edge_len.strip(string.whitespace))
            if edge_len == -1:
                MAP[i].append(0)
            else:
                MAP[i].append(edge_len)
    f.close()


if __name__ == '__main__':


    plt.subplot(121)

    G1 = nx.Graph()
    #1、初始化地图，保存所有边及信息
    init_map()
    #2、读取json信息，并获取部署信息(V_pc, V_cc, 控制链路等)
    with open("../paper_4/topo_info.json", "r") as f:
        topo_info_json = json.load(f)
    topo_info = json.loads(topo_info_json)  # topo_info的数据类型为字典
    v_cc = topo_info["v_cc"]
    v_pc = topo_info["v_pc"]
    control_links = topo_info["control_links"]
    vcc_control_links = topo_info["vcc_control_links"]
    print(control_links)
    #3、画节点
    for i in range(ROUTER_NUM):
        if i in v_pc:
            G1.add_nodes_from([i], color='orangered')
        else:
            G1.add_nodes_from([i], color='orange')
    node_color = [G1.node[i]['color'] for i in G1]

    nx.draw_networkx_nodes(G1,  pos, with_labels=True, node_color=node_color, node_size=node_size)
    nx.draw_networkx_labels(G1, pos, font_size=label_font_size)
    # 4、画边
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            if i == j or j < i:
                continue
            if MAP[i][j] != 0:
                G1.add_edges_from([(i, j)], label=MAP[i][j])

    edge_color = []
    for i in G1.edges:
        if list(i) in control_links:
            edge_color.append('orangered')  # 控制链路用红色表示
        else:
            edge_color.append('k')  # 普通链路用黄色表示

    edge_labels = nx.get_edge_attributes(G1, "label")
    # print(edge_labels)

    nx.draw_networkx_edges(G1, pos, edge_color=edge_color)
    nx.draw_networkx_edge_labels(G1, pos, edge_labels=edge_labels,font_size=label_font_size)
    plt.axis('off')






    plt.subplot(122)

    G2 = nx.Graph()
    # 1、初始化地图，保存所有边及信息
    init_map()
    # 2、读取json信息，并获取部署信息(V_pc, V_cc, 控制链路等)
    with open("../paper_2/topo_info.json", "r") as f:
        topo_info_json = json.load(f)
    topo_info = json.loads(topo_info_json)  # topo_info的数据类型为字典
    v_cc = topo_info["v_cc"]
    v_pc = topo_info["v_pc"]
    control_links = topo_info["control_links"]
    vcc_control_links = topo_info["vcc_control_links"]
    print(control_links)
    # 3、画节点
    for i in range(ROUTER_NUM):
        if i in v_pc:
            G2.add_nodes_from([i], color='orangered')
        else:
            G2.add_nodes_from([i], color='orange')
    node_color = [G2.node[i]['color'] for i in G2]

    nx.draw_networkx_nodes(G2, pos, with_labels=True, node_color=node_color, node_size=node_size)
    nx.draw_networkx_labels(G2, pos, font_size=label_font_size)
    # 4、画边
    for i in range(ROUTER_NUM):
        for j in range(ROUTER_NUM):
            if i == j or j < i:
                continue
            if MAP[i][j] != 0:
                G2.add_edges_from([(i, j)], label=MAP[i][j])

    edge_color = []
    for i in G2.edges:
        if list(i) in control_links:
            edge_color.append('orangered')  # 控制链路用红色表示
        else:
            edge_color.append('k')  # 普通链路用黄色表示

    edge_labels = nx.get_edge_attributes(G2, "label")
    # print(edge_labels)

    nx.draw_networkx_edges(G2, pos, edge_color=edge_color)
    nx.draw_networkx_edge_labels(G2, pos, edge_labels=edge_labels, font_size=label_font_size)
    plt.axis('off')


    plt.show()
