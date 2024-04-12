
## Install the requirements for client
`Tips`: python3.7+ is required

```shell
pip3 install websockets
```

## API-reference
```shell
python funasr_wss_client.py \
--host [ip_address] \
--port [port id] \
--chunk_size ["5,10,5"=600ms, "8,8,4"=480ms] \
--chunk_interval [duration of send chunk_size/chunk_interval] \
--words_max_print [max number of words to print] \
--audio_in [if set, loadding from wav.scp, else recording from mircrophone] \
--output_dir [if set, write the results to output_dir] \
--mode [`online` for streaming asr, `offline` for non-streaming, `2pass` for unifying streaming and non-streaming asr] \
--thread_num [thread_num for send data]
--hotword [hotword, *.txt(one hotword perline) or hotwords seperate by space (could be: 阿里巴巴 达摩院)]
--ssl [`1` deflaut, where to connect with ssl, if set `0` to close ssl]
```

#### Usage examples
##### ASR offline client
Recording from mircrophone
```shell
# --chunk_interval, "10": 600/10=60ms, "5"=600/5=120ms, "20": 600/12=30ms
python funasr_wss_client.py --host "0.0.0.0" --port 10095 --mode offline
```
Loadding from wav.scp(kaldi style)
```shell
# --chunk_interval, "10": 600/10=60ms, "5"=600/5=120ms, "20": 600/12=30ms
python funasr_wss_client.py --host "0.0.0.0" --port 10095 --mode offline --audio_in "./data/wav.scp" --output_dir "./results"
```

##### ASR streaming client
Recording from mircrophone
```shell
# --chunk_size, "5,10,5"=600ms, "8,8,4"=480ms
python funasr_wss_client.py --host "0.0.0.0" --port 10095 --mode online --chunk_size "5,10,5"
```
Loadding from wav.scp(kaldi style)
```shell
# --chunk_size, "5,10,5"=600ms, "8,8,4"=480ms
python funasr_wss_client.py --host "0.0.0.0" --port 10095 --mode online --chunk_size "5,10,5" --audio_in "./data/wav.scp" --output_dir "./results"
```

##### ASR offline/online 2pass client
Recording from mircrophone
```shell
# --chunk_size, "5,10,5"=600ms, "8,8,4"=480ms
python funasr_wss_client.py --host "0.0.0.0" --port 10095 --mode 2pass --chunk_size "8,8,4"
```
Loadding from wav.scp(kaldi style)
```shell
# --chunk_size, "5,10,5"=600ms, "8,8,4"=480ms
python funasr_wss_client.py --host "0.0.0.0" --port 10095 --mode 2pass --chunk_size "8,8,4" --audio_in "./data/wav.scp" --output_dir "./results"
```

#### Websocket api
```shell
    # class Funasr_websocket_recognizer example with 3 step
    # 1.create an recognizer 
    rcg=Funasr_websocket_recognizer(host="127.0.0.1",port="30035",is_ssl=True,mode="2pass")
    # 2.send pcm data to asr engine and get asr result
    text=rcg.feed_chunk(data)
    print("text",text)
    # 3.get last result, set timeout=3
    text=rcg.close(timeout=3)
    print("text",text)
```

## Acknowledge
1. This project is maintained by [FunASR community](https://github.com/alibaba-damo-academy/FunASR).
2. We acknowledge [zhaoming](https://github.com/zhaomingwork/FunASR/tree/fix_bug_for_python_websocket) for contributing the websocket service.
3. We acknowledge [cgisky1980](https://github.com/cgisky1980/FunASR) for contributing the websocket service of offline model.


###使用方法
1、生成wav.scp文件列表wav.scp并写入文件路径
/home/tabr/fun/samples/python

进入到以上目录执行
python3 scp-list.py

在执行
python3 funasr_wss_client.py --host "127.0.0.1" --port 10095 --ssl 0 --mode offline --audio_in "wav.scp" > test.txt

python3 funasr_wss_client.py --host "127.0.0.1" --port 10095 --ssl 0 --mode offline --hotword "./hotword.txt"  --audio_in "wav.scp" > test.txt



--host 为FunASR runtime-SDK服务部署机器ip，默认为本机ip（127.0.0.1），如果client与服务不在同一台服务器，
       需要改为部署机器ip
--port 10095 部署端口号
--mode offline表示离线文件转写
--audio_in 需要进行转写的音频文件，支持文件路径，文件列表wav.scp
--thread_num 设置并发发送线程数，默认为1
--ssl 设置是否开启ssl证书校验，默认1开启，设置为0关闭
--hotword 热词文件，每行一个热词，格式(热词 权重)：阿里巴巴 20
--use_itn 设置是否使用itn，默认1开启，设置为0关闭




执行数据筛选
python3  data.py











# funasr-python-api
