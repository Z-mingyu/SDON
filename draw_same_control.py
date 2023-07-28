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

data_1 = []
data_2 = []
data_3 = []





plt.subplot(121)  # 子图1


f = open("paper_1/same_control_cost.txt", "r", encoding="utf-8")
lines = f.readlines()
for i in range(0, lines.__len__()):
    for j in lines[i].split():
        data_1.append(float(j.strip(string.whitespace)))
f.close()

f = open("paper_2/same_control_cost.txt", "r", encoding="utf-8")
lines = f.readlines()
for i in range(0, lines.__len__()):
    for j in lines[i].split():
        data_2.append(float(j.strip(string.whitespace)))
f.close()

f = open("paper_4/same_control_cost.txt", "r", encoding="utf-8")
lines = f.readlines()
for i in range(0, lines.__len__()):
    for j in lines[i].split():
        data_3.append(float(j.strip(string.whitespace)))
f.close()

x = [i*0.01 for i in range(len(data_2))]

plt.plot(x, data_1, '-+', label='算法一', color="b", linewidth=line_width, markersize=makersize+2)
plt.plot(x, data_2, '-s', label='算法二', linewidth=1, color="g", markersize=makersize)
plt.plot(x, data_3, '-o', label='算法三', color="y", linewidth=line_width, markersize=makersize)
plt.legend(prop=CN_font, frameon=False, loc='best')

# 修改坐标轴宽度
ax = plt.gca() # gca = 'get current axis' 获取当前坐标
ax.spines['top'].set_linewidth(line_width)
ax.spines['bottom'].set_linewidth(line_width)
ax.spines['left'].set_linewidth(line_width)
ax.spines['right'].set_linewidth(line_width)
ax.set_xticks([0.00, 0.02, 0.04, 0.06, 0.08, 0.10])  # 若横坐标轴刻度显示不完全时，可用这句话重新设置坐标值

plt.xlabel("光纤百公里故障概率", fontproperties=CN_font)
plt.ylabel("故障出现概率", fontproperties=CN_font)

plt.xticks(fontproperties=EN_font)  # 设置坐标轴字体
plt.yticks(fontproperties=EN_font)

plt.title("(a) 三种算法在COST239中的可靠性比较", y=-0.42, fontproperties=CN_font)  # 加入标题







plt.subplot(122)

data_1 = []
data_2 = []
data_3 = []

f = open("paper_1/same_control_nsf.txt", "r", encoding="utf-8")
lines = f.readlines()
for i in range(0, lines.__len__()):
    for j in lines[i].split():
        data_1.append(float(j.strip(string.whitespace)))
f.close()

f = open("paper_2/same_control_nsf.txt", "r", encoding="utf-8")
lines = f.readlines()
for i in range(0, lines.__len__()):
    for j in lines[i].split():
        data_2.append(float(j.strip(string.whitespace)))
f.close()

f = open("paper_4/same_control_nsf.txt", "r", encoding="utf-8")
lines = f.readlines()
for i in range(0, lines.__len__()):
    for j in lines[i].split():
        data_3.append(float(j.strip(string.whitespace)))
f.close()

x = [i*0.01 for i in range(len(data_2))]

plt.plot(x, data_1, '-+', label='算法一', color="b", linewidth=line_width, markersize=makersize+2)
plt.plot(x, data_2, '-s', label='算法二', linewidth=line_width, color="g", markersize=makersize)
plt.plot(x, data_3, '-o', label='算法三', color="y", linewidth=line_width, markersize=makersize)
plt.legend(prop=CN_font, frameon=False, loc='best')

# 修改坐标轴宽度
ax = plt.gca() # gca = 'get current axis' 获取当前坐标
ax.spines['top'].set_linewidth(line_width)
ax.spines['bottom'].set_linewidth(line_width)
ax.spines['left'].set_linewidth(line_width)
ax.spines['right'].set_linewidth(line_width)
ax.set_xticks([0.00, 0.02, 0.04, 0.06, 0.08, 0.10])  # 若横坐标轴刻度显示不完全时，可用这句话重新设置坐标值
plt.xlabel("光纤百公里故障概率", fontproperties=CN_font)
plt.ylabel("故障出现概率", fontproperties=CN_font)

plt.xticks(fontproperties=EN_font)  # 设置坐标轴字体
plt.yticks(fontproperties=EN_font)

plt.title("(b) 三种算法在NSF中的可靠性比较", y=-0.42, fontproperties=CN_font)  # 加入标题







# 图间设置
plt.subplots_adjust(wspace=0.4)  # 调整子图间距

# 保存图片
plt.savefig('paper_pic/same_control.jpg', format='jpg', bbox_inches='tight', pad_inches=0)  # 紧凑型保存
plt.savefig('paper_pic/same_control.svg', format='svg', bbox_inches='tight', pad_inches=0)  # 保存成矢量图，方便修改

# plt.show()
