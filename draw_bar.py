import matplotlib.pyplot as plt
import string
import numpy as np
from matplotlib.font_manager import FontProperties

filename = 'ab'  # ab 或者cd

CN_font = FontProperties(fname='C:\Windows\Fonts\simsun.ttc', size=7)  # 中文字体
EN_font = FontProperties(fname='C:\Windows\Fonts\euclid.ttf', size=7)  # 英文字体
plt.rcParams['figure.figsize'] = (5.57, 2.36220471*3/4)  # 设置图片大小（单位：英寸）
plt.rcParams['savefig.dpi'] = 600  #设置图片分辨率，600像素/英寸
plt.rcParams['xtick.direction'] = 'out'  # 设置x轴tick向内
plt.rcParams['ytick.direction'] = 'in'

width = 0.1  # 柱状图宽度
line_width = 0.5

x_label=['C-MPC','TDCP','SCD','STCP']

x = [0,1,2,3]
x_origin=[0,1,2,3]
plt.subplot(121)

if filename == 'ab':
    # NSF
    data_2 = [4,7,7,4]# p=0.02时用的数据
    data_3 = [4,7,12,5]# p=0.03时用的数据
else:
    #
    data_2 = [4, 7, 5, 3]
    data_3 = [5, 4, 2, 2, 1, 1, 1]

# 如果要绘制彩色的，则删除相应的hatch、color和linewidth参数即可
plt.bar(x, data_2, width=width, label="p=0.02", color="white", edgecolor="black", hatch="///////", linewidth=line_width)
for i in range(len(x)):
    x[i] = x_origin[i] + width
plt.bar(x, data_3, width=width, label="p=0.03", color="white", edgecolor="black", hatch='■', linewidth=line_width)


plt.legend(prop=EN_font, frameon=False)

plt.xlabel("不同控制器部署算法", fontproperties=CN_font)
plt.ylabel("控制器部署个数", fontproperties=CN_font)

#plt.xticks(fontproperties=EN_font)  # 设置坐标轴字体
plt.xticks([index-0.05  for index in x], x_label,fontproperties=EN_font)
plt.yticks(fontproperties=EN_font)

if filename == 'ab':
    plt.title("(a) NSF网络控制器部署个数", y=-0.42, fontproperties=CN_font)  # 加入标题
else:
    plt.title("(c) 当p=0.03时，COST239网络控制器部署个数", y=-0.42, fontproperties=CN_font)  # 加入标题

ax = plt.gca() # gca = 'get current axis' 获取当前坐标
line_width = 0.5
ax.spines['top'].set_linewidth(line_width)
ax.spines['bottom'].set_linewidth(line_width)
ax.spines['left'].set_linewidth(line_width)
ax.spines['right'].set_linewidth(line_width)
# ax.set_xticks(x_origin)  # 若横坐标轴刻度显示不完全时，可用这句话重新设置坐标值

if filename == 'ab':
    ax.set_yticks([1, 3, 5, 7,9,11,13])
    plt.ylim(0.1, 14)
else:
    ax.set_yticks([1, 3, 5, 7, 9, 11])
    plt.ylim(0.1, 12)





plt.subplot(122)

if filename == 'ab':
    # USNET
    data_2 = [6, 9, 8, 6] # p=0.02时用的数据
    data_3 = [6, 9, 18, 7]# p=0.03时用的数据
else:
# p=0.03时用的数据
    data_2 = [14, 14, 14, 13, 11, 10, 10]
    data_3 = [12, 12, 8, 6, 4, 3, 3]

x = x_origin[:]
plt.bar(x, data_2, width=width, label="p=0.02", color="white", edgecolor="black", hatch="///////", linewidth=line_width)
for i in range(len(x)):
    x[i] = x_origin[i] + width
plt.bar(x, data_3, width=width, label="p=0.03", color="white", edgecolor="black", hatch='■', linewidth=line_width)
plt.legend(prop=EN_font, frameon=False)

plt.xlabel("不同控制器部署算法", fontproperties=CN_font)
plt.ylabel("控制器部署个数", fontproperties=CN_font)

#plt.xticks(fontproperties=EN_font)  # 设置坐标轴字体
plt.xticks([index -0.05 for index in x], x_label,fontproperties=EN_font)
plt.yticks(fontproperties=EN_font)

if filename == 'ab':
    plt.title("(b) USNET网络控制器部署个数", y=-0.42, fontproperties=CN_font)  # 加入标题
else:
    plt.title("(d) 当p=0.03时，NSF网络控制器部署个数", y=-0.42, fontproperties=CN_font)  # 加入标题

# 修改坐标轴宽度
ax = plt.gca() # gca = 'get current axis' 获取当前坐标
line_width = 0.5
ax.spines['top'].set_linewidth(line_width)
ax.spines['bottom'].set_linewidth(line_width)
ax.spines['left'].set_linewidth(line_width)
ax.spines['right'].set_linewidth(line_width)
# ax.set_xticks(x_origin)  # 若横坐标轴刻度显示不完全时，可用这句话重新设置坐标值


if filename == 'ab':
    ax.set_yticks([2, 4, 6, 8, 10, 12, 14,16,18])
    plt.ylim(0.1, 19)
else:
    ax.set_yticks([2,  6, 10, 14,18])
    plt.ylim(0.1, 20)




# 图间设置
plt.subplots_adjust(wspace=0.4)  # 调整子图间距

# 保存图片
if filename == 'ab':
    plt.savefig('paper_pic/black_white_pic/control_compare_ab.jpg', format='jpg', bbox_inches='tight', pad_inches=0)  # 紧凑型保存
    plt.savefig('paper_pic/black_white_pic/control_compare_ab.svg', format='svg', bbox_inches='tight', pad_inches=0)  # 保存成矢量图，方便修改
else:
    plt.savefig('paper_pic/black_white_pic/control_compare_cd.jpg', format='jpg', bbox_inches='tight', pad_inches=0)  # 紧凑型保存
    plt.savefig('paper_pic/black_white_pic/control_compare_cd.svg', format='svg', bbox_inches='tight', pad_inches=0)  # 保存成矢量图，方便修改
# plt.show()
