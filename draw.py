import matplotlib.pyplot as plt
import string
import numpy as np
from matplotlib.font_manager import FontProperties

CN_font = FontProperties(fname='C:\Windows\Fonts\simsun.ttc', size=7)  # 中文字体
EN_font = FontProperties(fname='C:\Windows\Fonts\euclid.ttf', size=7)  # 英文字体
plt.rcParams['figure.figsize'] = (5.57, 2.36220471*3/4)  # 设置图片大小（单位：英寸）
plt.rcParams['savefig.dpi'] = 600  #设置图片分辨率，600像素/英寸
plt.rcParams['xtick.direction'] = 'in'  # 设置x轴tick向内
plt.rcParams['ytick.direction'] = 'in'

makersize = 2  # 线的图标大小
line_width = 0.5

x_label=['10','12','14','16','18','20']
data_1 = [ 0.100, 0.089,0.079,0.092,0.087,0.079]
data_2 = [0.197, 0.194, 0.211,0.251,0.251,  0.309]






plt.subplot(121)  # 子图1


# f = open("paper_1/0.03_0.2_cost.txt", "r", encoding="utf-8")
# lines = f.readlines()
# for i in range(0, lines.__len__()):
#     for j in lines[i].split():
#         data_1.append(float(j.strip(string.whitespace)))
# f.close()
#
# f = open("paper_2/0.03_0.2_cost.txt", "r", encoding="utf-8")
# lines = f.readlines()
# for i in range(0, lines.__len__()):
#     for j in lines[i].split():
#         data_2.append(float(j.strip(string.whitespace)))
# f.close()
#
# f = open("paper_4/0.03_0.2_cost.txt", "r", encoding="utf-8")
# lines = f.readlines()
# for i in range(0, lines.__len__()):
#     for j in lines[i].split():
#         data_3.append(float(j.strip(string.whitespace)))
# f.close()

#x = [i*0.01 for i in range(len(data_2))]
x=[10,12,14,16,18,20]
# plt.plot(x, data_1, '-+', label='算法一', color="b", linewidth=line_width, markersize=makersize+2)
# plt.plot(x, data_2, '-s', label='算法二', linewidth=1, color="g", markersize=makersize)
# plt.plot(x, data_3, '-o', label='算法三', color="y", linewidth=line_width, markersize=makersize)

# 将线的颜色改为了黑色
plt.plot(x, data_1, '-+', label='STCP', color="k", linewidth=line_width, markersize=makersize+2)
plt.plot(x, data_2, '-s', label='TDCP', linewidth=line_width, color="k", markersize=makersize)
#plt.plot(x, data_3, '-o', label='SCD', color="k", linewidth=line_width, markersize=makersize)

plt.legend(prop=EN_font, frameon=False, loc='best')

# 修改坐标轴宽度
ax = plt.gca()  # gca = 'get current axis' 获取当前坐标
ax.spines['top'].set_linewidth(line_width)
ax.spines['bottom'].set_linewidth(line_width)
ax.spines['left'].set_linewidth(line_width)
ax.spines['right'].set_linewidth(line_width)
ax.set_xticks([10,12,14,16,18,20])  # 若横坐标轴刻度显示不完全时，可用这句话重新设置坐标值
# plt.xticks([index for index in x], x_label,fontproperties=EN_font)
ax.set_yticks([0,0.1,0.2,0.3])
plt.ylim(0, 0.35)
plt.title("(a)时延约束下USNET网络故障率", y=-0.42, fontproperties=CN_font)  # 加入标题
plt.xlabel("控制时延约束(ms)", fontproperties=CN_font)
plt.ylabel("故障出现概率", fontproperties=CN_font)

plt.xticks(fontproperties=EN_font)  # 设置坐标轴字体
plt.yticks(fontproperties=EN_font)

# plt.title("(c) p=0.03时三种算法在COST239中的比较", y=-0.42, fontproperties=CN_font)  # 加入标题







plt.subplot(122)

width = 0.5  # 柱状图宽度
x=[10,12,14,16,18,20]
x_origin=[10,12,14,16,18,20]
data_1 = [6,6,4,3,3,3]
data_2 = [9,7,5,3,3,3]
#data_3 = []

# f = open("paper_1/0.03_0.2_nsf.txt", "r", encoding="utf-8")
# lines = f.readlines()
# for i in range(0, lines.__len__()):
#     for j in lines[i].split():
#         data_1.append(float(j.strip(string.whitespace)))
# f.close()
#
# f = open("paper_2/0.03_0.2_nsf.txt", "r", encoding="utf-8")
# lines = f.readlines()
# for i in range(0, lines.__len__()):
#     for j in lines[i].split():
#         data_2.append(float(j.strip(string.whitespace)))
# f.close()
#
# f = open("paper_4/0.03_0.2_nsf.txt", "r", encoding="utf-8")
# lines = f.readlines()
# for i in range(0, lines.__len__()):
#     for j in lines[i].split():
#         data_3.append(float(j.strip(string.whitespace)))
# f.close()



# plt.plot(x, data_1, '-+', label='算法一', color="b", linewidth=line_width, markersize=makersize+2)
# plt.plot(x, data_2, '-s', label='算法二', linewidth=line_width, color="g", markersize=makersize)
# plt.plot(x, data_3, '-o', label='算法三', color="y", linewidth=line_width, markersize=makersize)
# 线条颜色改为黑色
# plt.plot(x, data_1, '-+', label='p=0.02', color="k", linewidth=line_width, markersize=makersize+2)
# plt.plot(x, data_2, '-s', label='p=0.03', linewidth=line_width, color="k", markersize=makersize)
#plt.plot(x, data_3, '-o', label='SCD', color="k", linewidth=line_width, markersize=makersize)
plt.bar(x, data_1, width=width, label="STCP", color="white", edgecolor="black", hatch="///////", linewidth=line_width)
for i in range(len(x)):
    x[i] = x_origin[i] + width
plt.bar(x, data_2, width=width, label="TDCP", color="white", edgecolor="black", hatch='■', linewidth=line_width)
plt.legend(prop=EN_font, frameon=False, loc='best')

# 修改坐标轴宽度
ax = plt.gca() # gca = 'get current axis' 获取当前坐标
line_width = 0.5
ax.spines['top'].set_linewidth(line_width)
ax.spines['bottom'].set_linewidth(line_width)
ax.spines['left'].set_linewidth(line_width)
ax.spines['right'].set_linewidth(line_width)
#ax.set_xticks(x_origin)  # 若横坐标轴刻度显示不完全时，可用这句话重新设置坐标值
plt.xticks([index-0.25  for index in x], x_label,fontproperties=EN_font)
ax.set_yticks([2, 4, 6, 8, 10])
plt.ylim(0, 10)
#ax.axes.xaxis.set_visible(False)
ax.tick_params(bottom=False)#不显示刻度线
#plt.xticks([index  for index in x],fontproperties=EN_font)
plt.xlabel("控制时延约束(ms)", fontproperties=CN_font)
plt.ylabel("控制器部署个数", fontproperties=CN_font)
plt.title("(b)时延约束下USNET网络控制器部署个数", y=-0.42, fontproperties=CN_font)  # 加入标题
plt.xticks(fontproperties=EN_font)  # 设置坐标轴字体
plt.yticks(fontproperties=EN_font)

# plt.title("(d) p=0.03时三种算法在NSF中的比较", y=-0.42, fontproperties=CN_font)  # 加入标题







# 图间设置
plt.subplots_adjust(wspace=0.4)  # 调整子图间距

# 保存图片
plt.savefig('paper_pic/black_white_pic/time.jpg', format='jpg', bbox_inches='tight', pad_inches=0)  # 紧凑型保存
plt.savefig('paper_pic/black_white_pic/time.svg', format='svg', bbox_inches='tight', pad_inches=0)  # 保存成矢量图，方便修改

# plt.show()
