# 该程序仅为Dijkstra算法。
a = [[0,5,0,3,0,2,2,0,0,0,0,0,0,0,0],
     [5,0,5,0,1,0,0,0,0,0,0,0,0,0,0],
     [0,5,0,0,0,0,0,0,2,1,0,0,0,0,0],
     [3,0,0,0,2,0,1,2,2,0,0,0,0,0,0],
     [0,1,0,2,0,0,0,3,0,3,0,0,0,0,0],
     [2,0,0,0,0,0,0,4,0,0,2,0,0,0,0],
     [2,0,0,1,0,0,0,0,0,0,0,2,0,0,0],
     [0,0,0,2,3,4,0,0,0,0,0,0,0,0,5],
     [0,0,2,2,0,0,0,0,0,2,0,0,5,0,0],
     [0,0,1,0,3,0,0,0,2,0,0,0,0,1,0],
     [0,0,0,0,0,2,0,0,0,0,0,2,0,0,0],
     [0,0,0,0,0,0,2,0,0,0,2,0,2,0,0],
     [0,0,0,0,0,0,0,0,5,0,0,2,0,4,0],
     [0,0,0,0,0,0,0,0,0,1,0,0,4,0,3],
     [0,0,0,0,0,0,0,5,0,0,0,0,0,3,0]]
temp = []
path = []


index = []  # 已经选过的节点
start = 'F'

source = 'F'

alphabet = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O')

last_point = {}  # 到达某一节点的前一个点
for i in range(len(alphabet)):
    last_point[alphabet[i]] = source

index = [alphabet.index(source)]
temp = a[alphabet.index(source)]


def find(temp,alphabet,index):
    min_len = 100000
    number = 10
    for i in range(len(alphabet)):
        if temp[i] > 0 and temp[i] < min_len and index.count(i) == 0:
            min_len = temp[i]
            number = i
    return min_len, number

for i in range(len(alphabet)):
    x, number = find(temp,alphabet,index)  # x为最短路径的长度，number为最短路径编号
    index.append(number)
    source = alphabet[number]
    for j in range(len(alphabet)):
        if index.count(j) == 0 :
            if temp[j] ==0 and a[number][j] != 0:
                temp[j] = temp[j] + a[number][j] + x
                last_point[alphabet[j]] = source
            if temp[j] ==0 and a[number][j] == 0:
                temp[j] = 0
            if temp[j] != 0 and a[number][j] != 0:

                if temp[j] > a[number][j]+x:
                    temp[j] = a[number][j] + x
                    last_point[alphabet[j]] = source

for i in range(len(alphabet)):
    print(alphabet[i],"的路径是：")
    k = last_point[alphabet[i]]
    while k != start:
        path.append(k)
        m = last_point[k]
        k = m
    path.append(start)
    for j in range(len(path)):
        print(path[len(path)-j-1],'-->')
    print(alphabet[i])
    print("----------------------------")
    path.clear()
    


            
