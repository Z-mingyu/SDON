import random
import os

node_num = 20
connect_probility = 0.30
min_len = 600
max_len = 2300
exp = 1000 # 正态分布的期望值
var = 500  # 正态分布的方差

def product_topo():
    node_list = [[] for i in range(node_num)]
    for i in range(node_num):
        for j in range(node_num):
            if i == j:  # 如果i,j相等，两者之间距离为0
                node_list[i].append(0)
                continue
            if j < i:
                node_list[i].append(node_list[j][i])
                continue

            if random.random() < connect_probility:  # 如果小于连接概率，则随机生成两点之间的路径长度
                # node_list[i].append(random.randint(min_len, max_len))

                random_len = int(abs(random.normalvariate(exp, var)))
                while random_len == 0:
                    random_len = int(abs(random.normalvariate(exp, var)))
                node_list[i].append(random_len)
                # node_list[i].append(400)
            else:
                node_list[i].append(-1)
    return node_list

def check_topo():
    flag = False # 默认为不合格
    for i in range(node_num):
        flag = False
        for j in node_list[i]:
            if j > 0:
                flag = True
                break
        if not flag:
            break
    return flag

if __name__ == '__main__':
    node_list = product_topo()
    while not check_topo():  # 如果生成拓扑不合格
        node_list = product_topo()

    if os.path.exists("random_topo.txt"):
        os.remove("random_topo.txt")
    f = open("random_topo.txt", 'a')
    for i in range(node_num):
        for j in range(node_num):
            if j == (node_num-1): # 最后一个则换行
                f.write('{}\n'.format(node_list[i][j]))
            else:
                f.write('{}\t'.format(node_list[i][j]))

    # print(node_list)