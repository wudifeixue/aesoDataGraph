import re

# 输入文件名
file_name = input("Enter the CSV file name (without .csv extension): ")

# 完整的文件名
input_filename = f"{file_name}.csv"

# 读取原始文件
with open(input_filename, 'r') as file:
    lines = file.readlines()

# 找到开始的那行，它通常是Date (HE),Price ($),30Ravg ($),AIL Demand (MW)
start_index = next((i for i, line in enumerate(lines) if "Date (HE)" in line), None)

# 取从这一行开始的所有行
relevant_data = lines[start_index + 1:]

# 正则表达式匹配和替换
pattern = r'"([^"]+)","([^"]+)","([^"]+)","([^"]+)"'
replacement = r"('\1', \2, \3, \4),"

formatted_data = [re.sub(pattern, replacement, line).strip() for line in relevant_data if re.match(pattern, line)]

# 移除最后的逗号
formatted_data[-1] = formatted_data[-1].rstrip(',')

# 保存到新文件
output_filename = f"{file_name}_insert.sql"
with open(output_filename, 'w') as file:
    # 写入INSERT的起始部分
    file.write("INSERT INTO public.pool_price(date_hours_ending, pool_price, thirty_ravg, all_demand) VALUES\n")
    # 写入格式化后的数据
    file.write("\n".join(formatted_data) + ";")

print(f"SQL script saved to {output_filename}")
