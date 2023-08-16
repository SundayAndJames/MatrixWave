from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# 创建 Flask 应用
app = Flask(__name__)
# 允许跨域访问
CORS(app)


# 定义根路由处理函数
@app.route('/')
def index():
    ###### 提取所有网站名
    website_name1 = []
    website_name2 = []
    with open("sequences1.txt", "r", encoding='utf-8') as file1:
        # 遍历文件的每一行
        for line in file1:
            # 遍历行中的每一个字符
            for char in line:
                # 这里做你需要做的处理，比如打印字符
                if char not in website_name1 and char != ' ' and char != "\n":
                    website_name1.append(char)
    with open("sequences2.txt", "r", encoding='utf-8') as file2:
        # 遍历文件的每一行
        for line in file2:
            # 遍历行中的每一个字符
            for char in line:
                # 这里做你需要做的处理，比如打印字符
                if char not in website_name2 and char != ' ' and char != "\n":
                    website_name2.append(char)
    website_name1.append("drop-off")
    website_name = list(set(website_name1 + website_name2))
    print(website_name)

    ###### 提取所有点击流
    click_flows1 = []  # 存储数据集1点击流
    click_flows2 = []  # 存储数据集1点击流
    with open("sequences1.txt", "r", encoding='utf-8') as file1:
        for line in file1:
            click_flow = []
            for char in line:
                if char != ' ':
                    if char == '\n':
                        click_flow.append('drop-off')
                    else:
                        click_flow.append(char)
            click_flows1.append(click_flow)
    with open("sequences2.txt", "r", encoding='utf-8') as file2:
        for line in file2:
            click_flow = []
            for char in line:
                if char != ' ':
                    if char == '\n':
                        click_flow.append('drop-off')
                    else:
                        click_flow.append(char)
            click_flows2.append(click_flow)
    for i in click_flows2:
        print(i)

    ###### 找出最长的点击流路径
    longest_list1 = max(click_flows1, key=len)
    max_length1 = len(longest_list1)
    longest_list2 = max(click_flows2, key=len)
    max_length2 = len(longest_list2)
    max_length = max(max_length1, max_length2)
    print(max_length2)

    ##### node_count_array存储每个步骤的节点访问次数
    node_count_array1 = []
    node_count_array2 = []
    for i in range(max_length):
        node_count = {}
        for name in website_name:
            node_count[name] = 0
        for item in click_flows1:
            try:
                temp = item[i]
                node_count[temp] = node_count[temp] + 1
            except IndexError:
                continue
        node_count_array1.append(node_count)
    for i in range(max_length):
        node_count = {}
        for name in website_name:
            node_count[name] = 0
        for item in click_flows2:
            try:
                temp = item[i]
                node_count[temp] = node_count[temp] + 1
            except IndexError:
                continue
        node_count_array2.append(node_count)

    ##### 给节点访问量按字母排序
    sorted_node_count_array1 = []
    sorted_node_count_array2 = []
    for i in node_count_array1:
        sorted_node_count = sorted(i.items())
        sorted_dict = dict(sorted_node_count)
        num = 0
        for key in sorted_dict:
            sorted_dict[key] = {'node_clicks': sorted_dict[key], 'index': num}
            num = num + 1
        # print(sorted_dict)
        sorted_node_count_array1.append(sorted_dict)
    for i in node_count_array2:
        sorted_node_count = sorted(i.items())
        sorted_dict = dict(sorted_node_count)
        num = 0
        for key in sorted_dict:
            sorted_dict[key] = {'node_clicks': sorted_dict[key], 'index': num}
            num = num + 1
        # print(sorted_dict)
        sorted_node_count_array2.append(sorted_dict)
    for i in sorted_node_count_array1:
        print(i)
    print('\n')
    for i in sorted_node_count_array2:
        print(i)

    # 步骤数
    process_number = max(len(sorted_node_count_array1), len(sorted_node_count_array2)) - 1
    print(process_number)
    # 记录两个数据集的节点访问量
    twosets_nodevolumn = []
    for i in range(process_number):
        node_volumn = {}
        for key in sorted_node_count_array1[0]:
            node_volumn[key] = {"node_clicks": [0, 0]}
        if i < len(sorted_node_count_array1):
            for key in sorted_node_count_array1[i]:
                node_volumn[key]["node_clicks"][0] = sorted_node_count_array1[i][key]["node_clicks"]
        if i < len(sorted_node_count_array2):
            for key in sorted_node_count_array2[i]:
                node_volumn[key]["node_clicks"][1] = sorted_node_count_array2[i][key]["node_clicks"]
        twosets_nodevolumn.append(node_volumn)
    for i in twosets_nodevolumn:
        print(i)
    print('\n')

    ##### 删除在两个数据集中访问量均为0的节点
    deleted_twosets_nodevolumn = []
    for i in twosets_nodevolumn:
        dic = {k: v for k, v in i.items() if (v['node_clicks'][0] != 0 or v['node_clicks'][1] != 0)}
        deleted_twosets_nodevolumn.append(dic)
    for i in deleted_twosets_nodevolumn:
        print(i)

    print('\n')
    ##### 加上索引
    index_twosets_nodevolumn = []
    for i in deleted_twosets_nodevolumn:
        count = 0
        for j in i:
            i[j]['index'] = count
            count = count + 1
        index_twosets_nodevolumn.append(i)
    for i in index_twosets_nodevolumn:
        print(i)

    ##### 创建link矩阵
    link_matrix_array = []
    for i in range(len(index_twosets_nodevolumn)):
        if i < len(index_twosets_nodevolumn) - 1:
            length1 = len(index_twosets_nodevolumn[i])
            length2 = len(index_twosets_nodevolumn[i + 1])
            matrix = [[[0, 0] for _ in range(length2)] for _ in range(length1)]
            # for m in matrix:
            #     print(m)
            # print('\n')
            link_matrix_array.append(matrix)
    # max_length-1是为了去掉最后多出的只有drop-off节点的步骤
    # i用于迭代第几个矩阵
    for i in range(max_length - 2):
        for j in click_flows1:
            try:
                link_matrix_array[i][index_twosets_nodevolumn[i][j[i]]['index']][
                    index_twosets_nodevolumn[i + 1][j[i + 1]]['index']][0] += 1
            except IndexError:
                continue
        for k in click_flows2:
            try:
                link_matrix_array[i][index_twosets_nodevolumn[i][k[i]]['index']][
                    index_twosets_nodevolumn[i + 1][k[i + 1]]['index']][1] += 1
            except IndexError:
                continue

    max_link_volumn = 0
    for i in link_matrix_array:
        for j in i:
            print(j)
            for k in j:
                if (k[0] + k[1]) / 2 >= max_link_volumn:
                    max_link_volumn = (k[0] + k[1]) / 2
        print('\n')

    ##### 构造传回数据

    # 构造每个步骤的网站名称
    websiteNameArrayOfSet = []
    for i in index_twosets_nodevolumn:
        website_names = []
        for key in i:
            website_names.append(key)
        print(website_names)
        websiteNameArrayOfSet.append(website_names)
    # 构造node流量并给出最大平均流量
    nodeVolumnArrayOfSet = index_twosets_nodevolumn
    maxNodeVolumn = 0
    for i in index_twosets_nodevolumn:
        for key in i:
            if maxNodeVolumn < i[key]['node_clicks'][0]:
                maxNodeVolumn = i[key]['node_clicks'][0]
            if maxNodeVolumn < i[key]['node_clicks'][1]:
                maxNodeVolumn = i[key]['node_clicks'][1]
    print(maxNodeVolumn)
    # 构造matrix流量
    matrix_volumn = link_matrix_array

    data = {"网站名称": websiteNameArrayOfSet, "node流量": nodeVolumnArrayOfSet, "最大node流量": maxNodeVolumn,
            "最大link流量": max_link_volumn, "matrix流量": matrix_volumn, 'click_flow1': click_flows1,
            'click_flow2': click_flows2}
    return data


if __name__ == '__main__':
    app.run()
