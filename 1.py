from aip import AipSpeech
import requests
import json
import os
import wave
from pyaudio import PyAudio, paInt16
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

APP_ID = '10866404'
API_KEY = 'EkOxMItHrkZv25gLj91iXNXk'
SECRET_KEY = '7680ecfeb76a8e5778a33b136b7900d5'
APP_ID2 = '10870874'
API_KEY2 = 'zYayPd1D6FDKieTfEF1RDiQq'
SECRET_KEY2 = 'e57a7a0dd6d1ced7476673cabaffcb23'
key = '559d57f32b8445c598d8fb65554e8320'
client1 = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
client2 = AipSpeech(APP_ID2, API_KEY2, SECRET_KEY2)
framerate = 8000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2
TIME = 2
chunk = 2024
cs = 1


def get_file_content(fillePath):
    with open(fillePath, 'rb') as fp:
        return fp.read()


def save_wave_file(filename, data):
    '''save the date to the wavfile'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()


def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1,
                     rate=framerate, input=True,
                     frames_per_buffer=NUM_SAMPLES)
    my_buf = []
    count = 0
    while count < TIME * 5:  # 控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count += 1
        print('.')
    save_wave_file('01.wav', my_buf)
    stream.close()


def play(gequ):
    if gequ == 'audio.mp3':
        os.system('ffmpeg -i audio.mp3 02.wav')
    elif gequ == 'mtq.mp3':
        os.system('ffmpeg -i mtq.mp3 02.wav')
    elif gequ == 'tq.mp3':
        os.system('ffmpeg -i tq.mp3 02.wav')
    elif gequ == 'kb.mp3':
        os.system('ffmpeg -i kb.mp3 02.wav')
    wf = wave.open('02.wav', 'rb')
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=
    wf.getnchannels(), rate=wf.getframerate(), output=True)
    while True:
        data = wf.readframes(chunk)
        if data == b"": break
        stream.write(data)
    stream.close()
    p.terminate()

driver = webdriver.Chrome()
webdriver.Firefox
while True:
    info=''
    # 优先判断输入内容
    driver.get("http://www.st.com")
    while (info != "退出"):
        #if a['err_no'] == 3301:
            # mtq=client2.synthesis('我没有听清','zh',1,{
            #     'vol': 10,
            #     'spd': 4,
            #     'per': 4,
            # })
            # if not isinstance(mtq, di+ct):
            #     with open('mtq.mp3', 'wb') as f:
            #         f.write(mtq)
            # play('mtq.mp3')
            #info = ''
        my_record()
        os.system('ffmpeg -y  -i 01.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm')
        os.system('del 02.wav')
        a = client1.asr(get_file_content('16k.pcm'), 'pcm', 16000, {
            'lan': 'zh'
        })
        if a['err_no'] != 3301:
            info = a['result'][0]
            if  info== '，':
                continue
            print(info)
            if info == '查询天气，':
                driver.get("http://www.st.com/login.html")
                mtq = client2.synthesis('你要查哪个城市', 'zh', 1, {
                    'vol': 10,
                    'spd': 4,
                    'per': 4,
                })
                if not isinstance(mtq, dict):
                    with open('tq.mp3', 'wb') as f:
                        f.write(mtq)
                play('tq.mp3')
                my_record()
                os.system('ffmpeg -y  -i 01.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm')
                os.system('del 02.wav')
                a = client1.asr(get_file_content('16k.pcm'), 'pcm', 16000, {
                    'lan': 'zh'
                })
                while(a['err_no'] == 3301):
                    mtq = client2.synthesis('你要查哪个城市', 'zh', 1, {
                        'vol': 10,
                        'spd': 4,
                        'per': 4,
                    })
                    if not isinstance(mtq, dict):
                        with open('tq.mp3', 'wb') as f:
                            f.write(mtq)
                    play('tq.mp3')
                else :
                    city = a['result'][0]
                    city = city.rstrip('，')
                driver.get("http://www.st.com/test.php?city="+city)
                continue
            elif info == '查询课表，':
                driver.get("http://www.st.com/login.html")
                mtq = client2.synthesis('你要查哪个班级', 'zh', 1, {
                    'vol': 10,
                    'spd': 4,
                    'per': 4,
                })
                if not isinstance(mtq, dict):
                    with open('kb.mp3', 'wb') as f:
                        f.write(mtq)
                play('kb.mp3')
                my_record()
                os.system('ffmpeg -y  -i 01.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm')
                os.system('del 02.wav')
                a = client1.asr(get_file_content('16k.pcm'), 'pcm', 16000, {
                    'lan': 'zh'
                })
                while (a['err_no'] == 3301):
                    mtq = client2.synthesis('你要查哪个班级', 'zh', 1, {
                        'vol': 10,
                        'spd': 4,
                        'per': 4,
                    })
                    if not isinstance(mtq, dict):
                        with open('kb.mp3', 'wb') as f:
                            f.write(mtq)
                    play('kb.mp3')
                else:
                    kb = a['result'][0]
                    kb = kb.rstrip('，')
                driver.get("http://www.st.com/"+kb+".html")
                continue
            elif info == '退出查询，' or info=='主页，':
                driver.get("http://www.st.com")
                continue
            else :
                url = 'http://www.tuling123.com/openapi/api?key=' + key + '&info=' + info
                res = requests.get(url)
                res.encoding = 'utf-8'
                jd = json.loads(res.text)
                result = client2.synthesis(jd['text'], 'zh', 1, {
                    'vol': 10,
                    'spd': 4,
                    'per': 4,
                })
                if not isinstance(result, dict):
                    with open('audio.mp3', 'wb') as f:
                        f.write(result)
                print(jd['text'])
                play('audio.mp3')
    driver.get("http://www.st.com")