# -*- coding: utf-8 -*-
import csv
import re
import os
import sys
import pandas as pd

# 音标匹配模式
match_str_pa = [r'/.*?/', r'\[.*?\]',r'{.*?}']

def file_is_exist(file_path):

    file_name = file_path.split("/")[-1]

    if os.path.exists(file_path):
        # print(f"File '{file_name}' exists in the current folder.")
        return True
    else:
        # print(f"File '{file_name}' doesn't exist in the current folder.")
        return False

def process(file_path, update):
    out_path = file_path + '.csv'

    # 如果文件存在就算了
    if update == False and file_is_exist(out_path):
        print("csv文件已存在：", out_path )
        print("如果需要更新文件，请带参数 --update 重新执行")
        print("结束处理")
        return None
    # 打开文件
    with open(file_path, 'r', encoding='utf-8') as file:
        # 构建列表
        a = []
        line_num = 0
        for i, line in enumerate(file):
            # 去除空行
            if line.strip():
                # line = "chamber* /ˈtʃeɪmbə(r)/ n. 室；洞穴；（枪）膛"

                line = line.strip()
                # print("line:" ,line.strip('\n'))
                match_str = None
                for patten in match_str_pa:
                    match_str = re.findall(patten, line)
                    if not match_str:
                        continue
                    else:
                        break
                if not match_str:
                    continue
                # print(match_str[0])
                res = line.split(match_str[0])
                res.insert(1, match_str[0])
                # print("res: ", res)
                # print("/n")

                # 将每行内容与行号作为元组放入列表
                yinbiao = " " * 2 + res[1].strip() + " " * 2 
                a.append((line_num, res[0].strip(), yinbiao, res[2].strip()))
                line_num += 1
    
    
    # 构建csv表
    with open(out_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入表头
        writer.writerow(['行号', '单词', '音标', '中文含义'])
        # 写入每个元组
        for row in a:
            writer.writerow(row)

    # 去重
    new_table = pd.read_csv(out_path).drop_duplicates(subset=['单词'], keep='last')
    new_table.to_csv(out_path, mode='w', index=False)

    if  update == False:      
        print("生成csv文档: ", out_path)
    else:
        print("更新csv文档: ", out_path)
    print("*****处理完毕******")


if __name__ == '__main__':
    # 获取命令行参数列表
    args = sys.argv

    # 判断是否传入了参数
    if len(args) > 1:
        # 获取当前路径
        folder_path = os.getcwd()
        
        if args[1] == '--all':
            # 处理当前目录下所有符合条件的文件
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".txt"):
                    file_path = os.path.join(folder_path, file_name)
                    print("待处理的文件路径: ", file_path)
                    process(file_path)
        elif len(args) == 3 and (args[2] == '--update' or args[2] == '-update' or args[2] == '-u'):
            file_path = os.path.join(folder_path, args[1])
            if file_path.endswith(".txt"):
                print("待处理的文件路径: ", file_path)
                process(file_path, update=True)
            else:
                print("Error: 请输入txt文件")
        else:
            # 处理指定的文件
            file_path = os.path.join(folder_path, args[1])
            if file_path.endswith(".txt"):
                print("待处理的文件路径: ", file_path)
                process(file_path, update=False)
            else:
                print("Error: 请输入txt文件")
    else:
        print('Error: 请传入参数')