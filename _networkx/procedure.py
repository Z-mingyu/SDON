# 该程序为算法的仿真演示程序，每一步结束后按回车开始下一步
import networkx as nx
import matplotlib.pyplot as plt
import parameter
import string
import json
from matplotlib.font_manager import FontProperties

ROUTER_NUM = parameter.ROUTER_NUM
map_file_name = parameter.map_file_name
CN_font = FontProperties(fname='C:\Windows\Fonts\simsun.ttc', size=16)  # 中文字体
node_size = 1000
edge_label_size = 10

'''
初始化MAP信息，MAP为原始地图信息
'''
MAP = [[] for i in range(ROUTER_NUM)]
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

"""
读取json文件信息并转化成字典
"""
with open("../paper_4/topo_info.json", "r") as f:
    topo_info_json = json.load(f)
topo_info = json.loads(topo_info_json)  # topo_info的数据类型为字典
control_links = topo_info["control_links"]
T_cs = topo_info["T_cs"]

with open("../paper_4/step_3.json", "r") as f:
    path_info_json = json.load(f)
path_info = json.loads(path_info_json)  # path_info的数据类型为字典


SPEED = 30  # 拓扑合并时的速度

# 合并图后的最后坐标
if ROUTER_NUM == 11:
    pos_final = [(102, 169), (382, 54),
           (367, 137), (452, 242),
           (600, 130), (563, 364),
           (263, 374), (281, 279),
           (165, 289), (74, 394),
           (432, 486)]
elif ROUTER_NUM == 14:
    pos_final = [(100, 304), (40, 192),
           (96, 97), (145, 169),
           (203, 153), (275, 86),
           (262, 184), (325, 206),
           (411, 206), (412, 97),
           (407, 302), (491, 286),
           (448, 172), (496, 210)]
'''
以上为初始化信息
#########################################################################################
'''
plt.ion()  # 开启interactive mode 成功的关键函数
# fig = plt.figure(figsize=(15, 10))
fig = plt.figure()
G = nx.Graph()

'''
显示原拓扑
'''
for i in range(ROUTER_NUM):
    G.add_nodes_from([i], color='orange')
for i in range(ROUTER_NUM):
    for j in range(ROUTER_NUM):
        if i == j or j < i:
            continue
        if MAP[i][j] != 0:
            G.add_edges_from([(i, j)], label=MAP[i][j])
node_color = [G.node[i]['color'] for i in G]
edge_labels = nx.get_edge_attributes(G, "label")

nx.draw_networkx_nodes(G, pos_final, with_labels=True, node_color=node_color, node_size=node_size)
nx.draw_networkx_labels(G, pos_final)
nx.draw_networkx_edges(G, pos_final)
nx.draw_networkx_edge_labels(G, pos_final, edge_labels=edge_labels, font_size=edge_label_size)
plt.title("NSFnet", fontproperties=CN_font)
plt.axis('off')

plt.show()
plt.pause(0.01)
go_command = input()
fig.clear()
G.clear()


'''
转化成二分图
'''
# 添加节点
for i in range(ROUTER_NUM):
    G.add_nodes_from(["a{}".format(i)], color='orange')
    G.add_nodes_from(["b{}".format(i)], color='dodgerblue')

# 添加边
for i in range(ROUTER_NUM):
    for j in range(ROUTER_NUM):
        G.add_edges_from([("a{}".format(i), "b{}".format(j))])

# 二分图中点的布局
node_color = [G.node[i]['color'] for i in G]
pos = {}
pos_temp = {}
for i in range(ROUTER_NUM):
    pos_temp["a{}".format(i)] = list(pos_final[i])
    pos_temp["b{}".format(i)] = list(pos_final[i])
for i in range(ROUTER_NUM):
    pos["a{}".format(i)] = [i*50, 54]
    pos["b{}".format(i)] = [i*50, 486]

for i in range(ROUTER_NUM):
     while pos_temp["a{}".format(i)][0] != pos["a{}".format(i)][0] or pos["a{}".format(i)][1] != pos_temp["a{}".format(i)][1] \
        or pos["b{}".format(i)][0] != pos_temp["b{}".format(i)][0] or pos["b{}".format(i)][1] != pos_temp["b{}".format(i)][1]:

        if pos["a{}".format(i)][0] > pos_temp["a{}".format(i)][0]:
            if pos["a{}".format(i)][0] - pos_temp["a{}".format(i)][0] >= SPEED:
                pos_temp["a{}".format(i)][0] += SPEED
            else:
                pos_temp["a{}".format(i)][0] += pos["a{}".format(i)][0] - pos_temp["a{}".format(i)][0]
        elif pos["a{}".format(i)][0] < pos_temp["a{}".format(i)][0]:
            if pos_temp["a{}".format(i)][0] - pos["a{}".format(i)][0] >= SPEED:
                pos_temp["a{}".format(i)][0] -= SPEED
            else:
                pos_temp["a{}".format(i)][0] -= pos_temp["a{}".format(i)][0] - pos["a{}".format(i)][0]
        if pos["a{}".format(i)][1] > pos_temp["a{}".format(i)][1]:
            if pos["a{}".format(i)][1] - pos_temp["a{}".format(i)][1] >= SPEED:
                pos_temp["a{}".format(i)][1] += SPEED
            else:
                pos_temp["a{}".format(i)][1] += pos["a{}".format(i)][1] - pos_temp["a{}".format(i)][1]
        elif pos["a{}".format(i)][1] < pos_temp["a{}".format(i)][1]:
            if pos_temp["a{}".format(i)][1] - pos["a{}".format(i)][1] >= SPEED:
                pos_temp["a{}".format(i)][1] -= SPEED
            else:
                pos_temp["a{}".format(i)][1] -= pos_temp["a{}".format(i)][1] - pos["a{}".format(i)][1]

        if pos["b{}".format(i)][0] > pos_temp["b{}".format(i)][0]:
            if pos["b{}".format(i)][0] - pos_temp["b{}".format(i)][0] >= SPEED:
                pos_temp["b{}".format(i)][0] += SPEED
            else:
                pos_temp["b{}".format(i)][0] += pos["b{}".format(i)][0] - pos_temp["b{}".format(i)][0]
        elif pos["b{}".format(i)][0] < pos_temp["b{}".format(i)][0]:
            if pos_temp["b{}".format(i)][0] - pos["b{}".format(i)][0] >= SPEED:
                pos_temp["b{}".format(i)][0] -= SPEED
            else:
                pos_temp["b{}".format(i)][0] -= pos_temp["b{}".format(i)][0] - pos["b{}".format(i)][0]
        if pos["b{}".format(i)][1] > pos_temp["b{}".format(i)][1]:
            if pos["b{}".format(i)][1] - pos_temp["b{}".format(i)][1] >= SPEED:
                pos_temp["b{}".format(i)][1] += SPEED
            else:
                pos_temp["b{}".format(i)][1] += pos["b{}".format(i)][1] - pos_temp["b{}".format(i)][1]
        elif pos["b{}".format(i)][1] < pos_temp["b{}".format(i)][1]:
            if pos_temp["b{}".format(i)][1] - pos["b{}".format(i)][1] >= SPEED:
                pos_temp["b{}".format(i)][1] -= SPEED
            else:
                pos_temp["b{}".format(i)][1] -= pos_temp["b{}".format(i)][1] - pos["b{}".format(i)][1]

        nx.draw_networkx_nodes(G, pos_temp, with_labels=True, node_color=node_color, node_size=node_size)
        nx.draw_networkx_labels(G, pos_temp)
        nx.draw_networkx_edges(G, pos_temp)

        plt.title("将原拓扑划分成完全二分图", fontproperties=CN_font)
        plt.axis('off')
        plt.show()
        plt.pause(0.01)
        fig.clear()


# nx.draw_networkx_nodes(G, pos, with_labels=True, node_color=node_color, node_size=600)
# nx.draw_networkx_labels(G, pos)
#
# nx.draw_networkx_edges(G, pos)
# plt.title("将拓扑划分成完全二分图", fontproperties=CN_font)
# plt.axis('off')
# plt.show()
#
# plt.pause(0.01)
# go_command = input()
# fig.clear()
# plt.axis('off')



'''
显示删除超过长度链路之后的二分图图像
'''
go_command = input()
for i in range(ROUTER_NUM):
    for j in range(ROUTER_NUM):
        if path_info[str(i)][j] == -1:
            G.remove_edges_from([("a{}".format(i), "b{}".format(j))])

        nx.draw_networkx_nodes(G, pos, with_labels=True, node_color=node_color, node_size=node_size)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos)
        plt.title("最长控制链路为{}，删除长度超过该值的链路".format(T_cs), fontproperties=CN_font)
        plt.axis('off')
        plt.show()
        plt.pause(0.01)
        fig.clear()

'''
显示相同合并过程
'''
go_command = input()
for i in range(ROUTER_NUM):
     while pos["a{}".format(i)][0] != pos_final[i][0] or pos["a{}".format(i)][1] != pos_final[i][1] \
             or pos["b{}".format(i)][0] != pos_final[i][0] or pos["b{}".format(i)][1] != pos_final[i][1]:
        if pos["a{}".format(i)][0] > pos_final[i][0]:
            if pos["a{}".format(i)][0] - pos_final[i][0] >= SPEED:
                pos["a{}".format(i)][0] -= SPEED
            else:
                pos["a{}".format(i)][0] -= pos["a{}".format(i)][0] - pos_final[i][0]
        elif pos["a{}".format(i)][0] < pos_final[i][0]:
            if pos_final[i][0] - pos["a{}".format(i)][0] >= SPEED:
                pos["a{}".format(i)][0] += SPEED
            else:
                pos["a{}".format(i)][0] += pos_final[i][0] - pos["a{}".format(i)][0]
        if pos["a{}".format(i)][1] > pos_final[i][1]:
            if pos["a{}".format(i)][1] - pos_final[i][1] >= SPEED:
                pos["a{}".format(i)][1] -= SPEED
            else:
                pos["a{}".format(i)][1] -= pos["a{}".format(i)][1] - pos_final[i][1]
        elif pos["a{}".format(i)][1] < pos_final[i][1]:
            if pos_final[i][1] - pos["a{}".format(i)][1] >= SPEED:
                pos["a{}".format(i)][1] += SPEED
            else:
                pos["a{}".format(i)][1] += pos_final[i][1] - pos["a{}".format(i)][1]

        if pos["b{}".format(i)][0] > pos_final[i][0]:
            if pos["b{}".format(i)][0] - pos_final[i][0] >= SPEED:
                pos["b{}".format(i)][0] -= SPEED
            else:
                pos["b{}".format(i)][0] -= pos["b{}".format(i)][0] - pos_final[i][0]
        elif pos["b{}".format(i)][0] < pos_final[i][0]:
            if pos_final[i][0] - pos["b{}".format(i)][0] >= SPEED:
                pos["b{}".format(i)][0] += SPEED
            else:
                pos["b{}".format(i)][0] += pos_final[i][0] - pos["b{}".format(i)][0]
        if pos["b{}".format(i)][1] > pos_final[i][1]:
            if pos["b{}".format(i)][1] - pos_final[i][1] >= SPEED:
                pos["b{}".format(i)][1] -= SPEED
            else:
                pos["b{}".format(i)][1] -= pos["b{}".format(i)][1] - pos_final[i][1]
        elif pos["b{}".format(i)][1] < pos_final[i][1]:
            if pos_final[i][1] - pos["b{}".format(i)][1] >= SPEED:
                pos["b{}".format(i)][1] += SPEED
            else:
                pos["b{}".format(i)][1] += pos_final[i][1] - pos["b{}".format(i)][1]

        nx.draw_networkx_nodes(G, pos, with_labels=True, node_color=node_color, node_size=node_size)
        nx.draw_networkx_labels(G, pos, font_size=edge_label_size)
        nx.draw_networkx_edges(G, pos)

        plt.title("将相同节点间连线删除，生成新的拓扑", fontproperties=CN_font)
        plt.axis('off')
        plt.show()
        plt.pause(0.001)
        fig.clear()

'''
新拓扑稳定图
'''
G_ = nx.Graph()
for i in range(ROUTER_NUM):
    G_.add_nodes_from([i], color='orange')
for i in range(ROUTER_NUM):
    for j in range(ROUTER_NUM):
        if j <= i:
            continue
        if path_info[str(i)][j] != -1:
            # G_.add_edges_from([(i, j)], label=path_info[str(i)][j])
            G_.add_edge(i, j,label=path_info[str(i)][j])
node_color = [G_.node[i]['color'] for i in G_]
edge_labels = nx.get_edge_attributes(G_, "label")

nx.draw_networkx_nodes(G_, pos_final, with_labels=True, node_color=node_color, node_size=node_size)
nx.draw_networkx_labels(G_, pos_final)
nx.draw_networkx_edges(G_, pos_final)
nx.draw_networkx_edge_labels(G_, pos_final, edge_labels=edge_labels,font_size=edge_label_size)
plt.title("新的拓扑图，两点间连线为其最短路径长度", fontproperties=CN_font)
plt.axis('off')

plt.show()
plt.pause(0.01)
go_command = input()
fig.clear()


'''
在新拓扑中显示选中的控制器
'''
for i in G_.nodes():
    if i in topo_info["v_pc"]:
        G_.node[i]["color"] = 'red'
node_color = [G_.node[i]['color'] for i in G_]
nx.draw_networkx_nodes(G_, pos_final, with_labels=True, node_color=node_color, node_size=node_size)
nx.draw_networkx_labels(G_, pos_final)
nx.draw_networkx_edges(G_, pos_final)
nx.draw_networkx_edge_labels(G_, pos_final, edge_labels=edge_labels,font_size=edge_label_size)
plt.title("红色节点为控制器部署节点", fontproperties=CN_font)
plt.axis('off')
plt.show()
plt.pause(0.01)
go_command = input()
fig.clear()


'''
在新拓扑中显示选中的控制链路
'''
control_node_tuple = []
# print(topo_info["control_node"])
for i in range(ROUTER_NUM):
    if str(i) in topo_info["control_node"].keys():
        if i < topo_info["control_node"][str(i)]:
            control_node_tuple.append((i, topo_info["control_node"][str(i)]))
        else:
            control_node_tuple.append((topo_info["control_node"][str(i)], i))
# 根据是否为控制链路改变链路颜色
edge_color = []
for i in G_.edges():
    if i in control_node_tuple:
        edge_color.append('r')  # 红色为控制链路
    else:
        edge_color.append('k')
nx.draw_networkx_nodes(G_, pos_final, with_labels=True, node_color=node_color, node_size=node_size)
nx.draw_networkx_labels(G_, pos_final)
nx.draw_networkx_edges(G_, pos_final, edge_color= edge_color)
nx.draw_networkx_edge_labels(G_, pos_final, edge_labels=edge_labels,font_size=edge_label_size)
plt.title("红色链路为控制链路", fontproperties=CN_font)
plt.axis('off')
plt.show()
plt.pause(0.01)
go_command = input()
fig.clear()



'''
显示原拓扑(控制器高亮)
'''
# 删除所有边
x = list(G_.edges())[:]
G_.remove_edges_from(x)

for i in range(ROUTER_NUM):
    for j in range(ROUTER_NUM):
        if i == j or j < i:
            continue
        if MAP[i][j] != 0:
            G_.add_edges_from([(i, j)], label=MAP[i][j])
edge_labels = nx.get_edge_attributes(G_, "label")

nx.draw_networkx_nodes(G_, pos_final, with_labels=True, node_color=node_color, node_size=node_size)
nx.draw_networkx_labels(G_, pos_final)
nx.draw_networkx_edges(G_, pos_final)
nx.draw_networkx_edge_labels(G_, pos_final, edge_labels=edge_labels,font_size=edge_label_size)
plt.title("原拓扑部署情况", fontproperties=CN_font)
plt.axis('off')
plt.show()
plt.pause(0.01)
go_command = input()
fig.clear()



'''
在原拓扑中显示控制链路
'''
edge_color = []
for i in G_.edges():
    if list(i) in control_links:
        edge_color.append('r')  # 控制链路用红色表示
    else:
        edge_color.append('k')  # 普通链路用黄色表示
nx.draw_networkx_nodes(G_, pos_final, with_labels=True, node_color=node_color, node_size=node_size)
nx.draw_networkx_labels(G_, pos_final)
nx.draw_networkx_edges(G_, pos_final, edge_color=edge_color)
nx.draw_networkx_edge_labels(G_, pos_final, edge_labels=edge_labels,font_size=edge_label_size)
plt.title("原拓扑部署情况", fontproperties=CN_font)
plt.axis('off')
plt.show()
plt.pause(0.01)
go_command = input()
fig.clear()


plt.subplot(121)
original_node_color = []
original_edge_color = []
for i in range(len(node_color)):
    original_node_color.append('orange')
for i in range(len(edge_color)):
    original_edge_color.append('k')
nx.draw_networkx_nodes(G_, pos_final, with_labels=True, node_color=original_node_color, node_size=node_size)
nx.draw_networkx_labels(G_, pos_final)
nx.draw_networkx_edges(G_, pos_final, edge_color=original_edge_color)
nx.draw_networkx_edge_labels(G_, pos_final, edge_labels=edge_labels,font_size=edge_label_size)
plt.title("原拓扑", fontproperties=CN_font)
plt.axis('off')

plt.subplot(122)

nx.draw_networkx_nodes(G_, pos_final, with_labels=True, node_color=node_color, node_size=node_size)
nx.draw_networkx_labels(G_, pos_final)
nx.draw_networkx_edges(G_, pos_final, edge_color=edge_color)
nx.draw_networkx_edge_labels(G_, pos_final, edge_labels=edge_labels,font_size=edge_label_size)
plt.title("部署情况", fontproperties=CN_font)

plt.axis('off')
plt.show()
plt.pause(0.01)
go_command = input()
fig.clear()
