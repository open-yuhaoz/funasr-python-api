import subprocess
import json
import re
import os
import tempfile
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 生成临时文件名
def generate_temp_filename():
    return next(tempfile._get_candidate_names())

# 下载文件到本地
def download_file(download_url, filename):
    download_command = f'wget --timeout=5 --tries=1 {download_url} -O /opt/wav-data/{filename}'
    result = subprocess.run(download_command, shell=True)
    return result

# 转换成单声道wav文件
def convert_to_mono_wav(downloaded_file):
    upload_command = f'curl -F "file=@/opt/wav-data/{downloaded_file}" 192.168.11.212:8066/wav > /opt/wav-data/mon_{downloaded_file}'
    subprocess.run(upload_command, shell=True)

# 调用funasr_wss_client.py脚本
def call_funasr_wss_client(host, port, ssl, mode, hotword_file_path, audio_in_file_path):
    command = f'/usr/bin/python3 /opt/wav/python/funasr_wss_client.py --host {host} --port {port} --ssl {ssl} --mode {mode} --hotword {hotword_file_path} --audio_in {audio_in_file_path}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result

@app.route('/execute_command', methods=['POST'])
def execute_command():
    try:
        host = "192.168.11.212"
        port = 10095
        ssl = 0
        mode = "offline"
        data = request.get_json()
        hotword_code = data.get('hotword')
        
        # 根据城市代码生成文件路径
        hotword_file_path = f"/opt/bd-hotwords/{hotword_code}-hotwords/hotwords.txt"

        # 获取上传的文件路径
        download_url = data.get('download_url')
        filename = generate_temp_filename()
       
        # 检查目录下是否是空目录
        cleanup_command = 'rm -rf /opt/wav-data/*'
        subprocess.run(cleanup_command, shell=True)

        # 下载文件到本地的/tmp目录
        result = download_file(download_url, filename)
        
        # 检查下载是否完成
        if result.returncode != 0:
            raise Exception('下载文件失败')

        # 获取下载后的文件名
        downloaded_file = subprocess.check_output(f'ls /opt/wav-data', shell=True).decode().strip()
        print(downloaded_file)
        
        # 调用8066接口转成单声道wav
        convert_to_mono_wav(downloaded_file)

        # 定义转成单声道wav文件
        audio_in_file_path = f'/opt/wav-data/mon_{downloaded_file}'
        print(audio_in_file_path)

        # 调用funasr_wss_client.py脚本
        result = call_funasr_wss_client(host, port, ssl, mode, hotword_file_path, audio_in_file_path)

        cleanup_command = 'rm -rf /opt/wav-data/*'
        subprocess.run(cleanup_command, shell=True)

        if result.returncode == 0:
            output = {'output': result.stdout, 'status': 'success'}
            match = re.search(r'demo:(.*?)Exception: sent 1000 \(OK\);', output['output'], re.DOTALL)
            if match:
                chinese_content = match.group(1).strip()
            else:
                chinese_content = "未找到对话内容"
        else:
            output = {'output': result.stderr, 'status': 'error'}
            chinese_content = "命令执行失败"

        response = app.response_class(
            response=json.dumps({'chinese_content': chinese_content}, ensure_ascii=False),
            status=200,
            mimetype='application/json; charset=utf-8'
        )
        return response

    except Exception as e:
        logging.exception("An error occurred")
        return jsonify({'error': str(e), 'status': 'error'}), 500, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
