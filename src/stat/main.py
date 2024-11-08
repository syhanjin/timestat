# -*- coding: utf-8 -*-
import argparse
from pathlib import Path
import sys

from base64 import b64decode
from urllib.parse import unquote
import json

import pandas as pd

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=__doc__)
parser.add_argument('-i', default=None, type=str, help='输入文件')
parser.add_argument('-o', default="combined_result.xlsx", type=str, help="综合统计结果文件")
parser.add_argument('-ao', default="all_tables_output.xlsx", type=str, help="源数据")


def b64_to_df(b64):
    data = json.loads(unquote(b64decode(b64)))
    tables = {}
    for raw in data:
        tables[raw['name']] = pd.DataFrame(
            {x: {y: 1 for y in raw['data'][x]} if x in raw['data'] else {} for x in raw['rows']}
        ).fillna(0).T

    return tables


def get_combined_result(b64_dict):
    combined_tables = {}
    for key, b64 in b64_dict.items():
        tables = b64_to_df(b64)
        for name, df in tables.items():
            if name in combined_tables:
                combined_tables[name] = combined_tables[name].add(df, fill_value=0)
            else:
                combined_tables[name] = df
    return combined_tables


def save_combined_result(combined_tables, filename="combined_result.xlsx"):
    # 使用复合索引将所有表格合并到一个 DataFrame
    combined_df = pd.concat(
        {name: df for name, df in combined_tables.items()},
        names=['Table Name', 'Index']
    ).fillna(0)

    # 保存到 Excel 文件的一个工作表中
    with pd.ExcelWriter(filename) as writer:
        combined_df.to_excel(writer, sheet_name="Combined_Result")

    print(f"汇总结果已保存到 {filename}")


# 保存所有 b64 数据到一个 Excel 文件，每个 b64 数据集对应一个工作表，使用复合索引区分不同的表格
def save_all_tables(b64_dict, filename="all_tables_output.xlsx"):
    with pd.ExcelWriter(filename) as writer:
        for key, b64 in b64_dict.items():
            tables = b64_to_df(b64)

            # 合并当前 b64 数据集中的所有表格为一个 DataFrame，使用复合索引
            combined_df = pd.concat(
                {name: df for name, df in tables.items()},
                names=['Table Name', 'Index']
            ).replace(0, pd.NA)

            # 写入一个工作表
            combined_df.to_excel(writer, sheet_name=key)

    print(f"所有 b64 数据已保存到 {filename}")


def main(argv):
    args = parser.parse_args(argv)
    if not args.i:
        i = input("数据文件路径：")
    else:
        i = args.i
    in_df = pd.read_excel(i)
    b64_dict = {row['name']: row['b64'] for index, row in in_df.iterrows()}
    save_all_tables(b64_dict, filename=args.ao)
    combined_tables = get_combined_result(b64_dict)
    save_combined_result(combined_tables, filename=args.o)


if __name__ == '__main__':
    main(sys.argv[1:])
