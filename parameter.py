'''
该程序负责三种算法的拓扑参数，不同拓扑图下节点个数和拓扑文件不同
'''

import random_topo



# ROUTER_NUM = 11  #11为cost239拓扑个数, 14为NSF拓扑的个数
# map_file_name = "COST239.txt"

#
# ROUTER_NUM = 14  #14为NSF拓扑个数, 14为NSF拓扑的个数
# map_file_name = "NSF.txt"

# ROUTER_NUM = 24  #24为USNET拓扑个数
# map_file_name = "../USNET.txt"


# ROUTER_NUM = 25  #25为Agis拓扑个数
# map_file_name = "../Agis.txt"


'''
用于产生随机拓扑
'''
ROUTER_NUM = random_topo.node_num
map_file_name = "../random_topo.txt"