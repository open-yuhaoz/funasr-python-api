import subprocess

command = "pyinstaller --onefile  --add-data 'funasr-server.py:.' --add-data 'funasr_wss_client.py:.'    funasr-server.py"
subprocess.run(command, shell=True)
