from flask import Flask, request, jsonify
import subprocess
import json
import re

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/execute_command', methods=['POST'])
def execute_command():
    try:
        host = "192.168.11.212"
        port = 10095
        ssl = 0
        mode = "offline"
        data = request.get_json()
        hotword = data.get('hotword')
        audio_in = data.get('audio_in')
        command = f'/usr/bin/python3 /opt/wav/python/funasr_wss_client.py  --host {host} --port {port} --ssl {ssl} --mode {mode} --hotword {hotword} --audio_in {audio_in}'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
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

        '''
        response = app.response_class(
            response=json.dumps(output, ensure_ascii=False),
            status=200 if result.returncode == 0 else 500,
            mimetype='application/json; charset=utf-8'
        )
        '''
        response = app.response_class(
            response=json.dumps({'chinese_content': chinese_content}, ensure_ascii=False),
            status=200,
            mimetype='application/json; charset=utf-8'
        )
        return response

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
