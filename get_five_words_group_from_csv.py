# -*- coding: utf-8 -*-
import csv
import os
import sys
import csv
import random
import pandas as pd

# 定义每组的数量
EXPORT_NUM = 5


def path_is_exist(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False


def export_5_words_md(shuffle_file_path, num, update=False):

    with open(shuffle_file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        # 第一行是csv表头
        data = list(reader)[1:]

    grouped_data = [data[i:i+num] for i in range(0, len(data), num)]
    grouped_data_reversed  = grouped_data[::-1]
    md_file_path = shuffle_file_path + '.md'

    md_file_reversed_name = "reversed_" + os.path.basename(md_file_path)
    md_file_reversed_path = os.path.join(os.path.dirname(csv_file_path),
                                        md_file_reversed_name) 

    def save_md(md_file_path, grouped_data, reversed=False):
        with open(md_file_path, 'w', encoding='utf-8') as f:
            if reversed == True:
                i = len(grouped_data) - 1
                for  group in grouped_data:
                    f.write(f'# {i}\n')
                    for row in group:
                        row = [row[1], row[3]]
                        # 逆序写入md，加入空格 与换行
                        f.write('  '.join(row) + '\n')
                    f.write('\n')
                    i = i-1
            else:
               for i , group in enumerate(grouped_data):
                f.write(f'# {i}\n')
                for row in group:
                    row = [row[1], row[3]]
                    # 顺序写入md，加入空格 与换行
                    f.write('  '.join(row) + '\n')
                f.write('\n')

    # 如果不存在，就保存为md文档
    if not path_is_exist(md_file_path):
        save_md(md_file_path, grouped_data)
        print("生成md文档: ", md_file_path)

        save_md(md_file_reversed_path, grouped_data_reversed, True)
        print("生成逆序md文档: ", md_file_reversed_path)
        
        return 
    
    if update == False and path_is_exist(md_file_path):
        print("md 文件已存在: ", md_file_path )
        print("如果需要更新文件，请带参数 --update 重新执行")
    
    if path_is_exist(md_file_path) and update==True:
        save_md(md_file_path, grouped_data)
        print("更新md文档: ", md_file_path)
        save_md(md_file_reversed_path, grouped_data_reversed, True)
        print("更新逆序md文档: ", md_file_reversed_path)


def merge_csv_return_diff(a_name, b_name):
    # 读取表a和表b的数据
    table_a = pd.read_csv(a_name)

    table_b = pd.read_csv(b_name)
    table_b_renamed = table_b.rename(columns={"行号": "行号_y","音标": "音标_y", "中文含义":"中文含义_y"})
    merged_table = pd.merge(table_a, table_b_renamed, on='单词', how='left', indicator=True)

    duplicates = False
    try:
        table_b['行号'] = table_b['单词'].map(table_a.set_index('单词')['行号'])
        table_b['中文含义'] = table_b['单词'].map(table_a.set_index('单词')['中文含义'])
    except Exception as e:
        print('error: {}'.format(e))
        # 对table_a表格的“单词”列进行去重
        duplicates = True
        table_a = table_a.drop_duplicates(subset=['单词'])
        print("可能是添加的单词重复了，进行了去重")
    
        table_b['行号'] = table_b['单词'].map(table_a.set_index('单词')['行号'])
        table_b['中文含义'] = table_b['单词'].map(table_a.set_index('单词')['中文含义'])

    # 找出在表a中存在但在表b中不存在的行
    table_c = merged_table[merged_table['_merge'] == 'left_only']
    # 提取特定列数据
    df_new = table_c.iloc[:,:4]
    table_b = pd.concat([table_b,df_new])

    return table_a, table_b, df_new, duplicates


def export_shuffle_csv(csv_file_path, update):
    shuffle_file_name = 'new_shuffle_'+os.path.basename(csv_file_path)
    shuffle_file_dir = os.path.dirname(csv_file_path)
    shuffle_file_path = os.path.join(shuffle_file_dir, shuffle_file_name)
    # 如果不存在，则继续处理
    if not path_is_exist(shuffle_file_path):
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            head = rows[0]
            rows = rows[1:]
        random.shuffle(rows)
        with open(shuffle_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 这是写一行
            writer.writerow(head)
            # 这是写多行
            writer.writerows(rows)
        print("生成乱序版csv文档: ", shuffle_file_path)
        return shuffle_file_path
    if update == False and path_is_exist(shuffle_file_path):
        print("乱序版 csv 文件已存在: ", shuffle_file_path )
        print("如果需要更新文件，请带参数 --update 重新执行")
    
    if update == True and path_is_exist(shuffle_file_path):
        table_a, table_updated,  need_add, duplicates= merge_csv_return_diff(csv_file_path,shuffle_file_path)
        print("----------------更新分割线--------------------")
        print("更新的内容:\n", need_add)
        print("----------------更新分割线--------------------")
        table_updated.to_csv(shuffle_file_path, mode='w', index=False)
        print("更新后乱序版csv文档: ", shuffle_file_path)
        if duplicates:
            table_a.to_csv(csv_file_path, mode='w', index=False)
            print("去重后的csv文档: ", shuffle_file_path)

    return shuffle_file_path


def get_shuffle_csv_and_md(csv_file_path, num=EXPORT_NUM, update=False):
    print("开始处理", "是否更新模式：", update)
    print("待处理的文件路径：", csv_file_path)
 
    shuffle_file_path = export_shuffle_csv(csv_file_path, update)
    export_5_words_md(shuffle_file_path, num, update)
    print("结束处理")


if __name__ == '__main__':
    # 获取命令行参数列表
    args = sys.argv
    # 判断是否传入了参数
    if len(args) > 1:
        # 获取当前路径
        folder_path = os.getcwd()

        # 处理指定的文件
        if args[1].endswith(".csv"):
            csv_file_path = os.path.join(folder_path, args[1])
            if len(args) == 3 and (args[2] == '--update' or args[2] == '-update'or args[2] == '-u'):
                get_shuffle_csv_and_md(csv_file_path,update=True)
            else:          
                get_shuffle_csv_and_md(csv_file_path)
            
        else:
            print("Error: 需要 .csv 文件")
        
    else:
        print('Error: 请传入参数')
