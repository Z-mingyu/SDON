import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


CN_font = FontProperties(fname='C:\Windows\Fonts\simsun.ttc', size=7)  # 中文字体
EN_font = FontProperties(fname='C:\Windows\Fonts\euclid.ttf', size=7)  # 英文字体
plt.rcParams['figure.figsize'] = (5.57, 2.36220471*3/4)  # 设置图片大小（单位：英寸）
plt.rcParams['savefig.dpi'] = 600  #设置图片分辨率，600像素/英寸
plt.rcParams['xtick.direction'] = 'out'  # 设置x轴tick向内
plt.rcParams['ytick.direction'] = 'in'

width = 0.03  # 柱状图的宽度
x = [0.1, 0.2,  0.3,  0.4, 0.5]

bottom_color = 'steelblue'
middle_color = 'gold'
top_color = 'limegreen'


plt.subplot(121)  # 子图1

data_1 = [7.189189189, 7.142857143, 6.933333333, 6.541666667, 6.863636364]
data_2 = [7.513513514, 7.457142857, 7.1, 6.541666667, 6.863636364]
data_3 = [7.513513514, 7.485714286, 7.166666667, 6.625, 6.863636364]
data_4 = [7.513513514, 7.457142857,	7.1, 6.541666667, 6.863636364]

for i in range(len(data_2)):
    data_3[i] = data_3[i]-data_2[i]
    data_2[i] = data_2[i]-data_1[i]

plt.bar(x, data_1, width=width, label="时延判决算法", color=bottom_color)
plt.bar(x, data_2, width=width, bottom=data_1, label="联合判决算法",color=middle_color)
plt.bar(x, data_3, width=width, bottom=data_4, label="最多无环路径数", color=top_color)
plt.legend(prop=CN_font, frameon=False)

plt.ylim(6.1, 8.1)


plt.xlabel("用户可接受故障概率", fontproperties=CN_font)
plt.ylabel("平均无环链路数", fontproperties=CN_font)

plt.xticks(fontproperties=EN_font)  # 设置坐标轴字体
plt.yticks(fontproperties=EN_font)

plt.title("(a) 管控中心至控制器平均链路长度对比", y=-0.42, fontproperties=CN_font)



# 修改坐标轴宽度
ax = plt.gca() # gca = 'get current axis' 获取当前坐标
line_width = 0.5
ax.spines['top'].set_linewidth(line_width)
ax.spines['bottom'].set_linewidth(line_width)
ax.spines['left'].set_linewidth(line_width)
ax.spines['right'].set_linewidth(line_width)
ax.set_xticks(x)  # 若横坐标轴刻度显示不完全时，可用这句话重新设置坐标值


plt.subplot(122)
data_1 = [1780.648649, 1826.914286, 1948.633333, 2089.291667, 2135.727273]
data_2 = [1935.081081, 1854.457143, 1953.733333, 2089.291667, 2135.727273]
for i in range(len(data_2)):
    data_2[i] = data_2[i] - data_1[i]

plt.bar(x, data_1, width=width, label="时延判决算法", color=bottom_color)
plt.bar(x, data_2, width=width, bottom=data_1, label="联合判决算法",color=middle_color)
plt.legend(prop=CN_font, frameon=False)
plt.tick_params(labelsize=7)

plt.ylim(1205, 2500)

# 修改坐标轴宽度
ax = plt.gca() # gca = 'get current axis' 获取当前坐标
line_width = 0.5
ax.spines['top'].set_linewidth(line_width)
ax.spines['bottom'].set_linewidth(line_width)
ax.spines['left'].set_linewidth(line_width)
ax.spines['right'].set_linewidth(line_width)

plt.xlabel("用户可接受故障概率", fontproperties=CN_font)
plt.ylabel("管控中心至控制器平均链路长度(千米)", fontproperties=CN_font)

plt.xticks(fontproperties=EN_font)  # 设置坐标轴字体
plt.yticks(fontproperties=EN_font)

plt.title("(b) 管控中心至控制器平均无环路径数对比", y=-0.42, fontproperties=CN_font)  # 加入标题




# 图间设置
plt.subplots_adjust(wspace=0.4)  # 调整子图间距

# 保存图片
# plt.savefig('paper_pic/vcc_pic_choice/{}_{}_{}.jpg'.format(bottom_color,middle_color,top_color), format='jpg', bbox_inches='tight', pad_inches=0)  # 紧凑型保存
# plt.savefig('paper_pic/vcc_pic_choice/{}_{}_{}.svg'.format(bottom_color,middle_color,top_color), format='svg', bbox_inches='tight', pad_inches=0)  # 保存成矢量图，方便修改
plt.show()