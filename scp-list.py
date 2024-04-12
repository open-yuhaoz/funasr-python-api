import os

# 设置要处理的目录路径
directory = '/home/tabr/fun/samples/python/wav-data'

# 打开文件列表wav.scp并写入文件路径
with open('wav.scp', 'w') as file:
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            file.write(f"{filename} {os.path.join(directory, filename)}\n")

print("文件列表wav.scp已生成。")
