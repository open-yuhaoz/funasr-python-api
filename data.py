
# 从test.txt中提取每行以"wav:"开头的数据，并写入test1.txt
with open('test.txt', 'r') as file:
    lines = file.readlines()
    extracted_data = [line.split('wav: ')[1].strip() for line in lines if line.startswith('pid')]

with open('test1.txt', 'w') as file:
    for data in extracted_data:
        file.write(data + '\n')

print("数据已从test.txt提取并写入test1.txt文件。")
