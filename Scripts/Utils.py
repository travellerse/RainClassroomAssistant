import json
import os
import sys
import threading
from math import exp

import pyttsx3
import requests
import urllib3
from numpy import random

if sys.platform.startswith("win"):
    import win32api
    import win32con
    from win10toast import ToastNotifier

lock = threading.Lock()
toaster = ToastNotifier()


def is_debug():
    # 判断是否为debug模式
    return True if sys.gettrace() else False


def say_something(text):
    # 带线程锁的语音函数
    lock.acquire()
    pyttsx3.speak(text)
    lock.release()


def show_info(text, title):
    toaster.show_toast(
        title, text, icon_path=r"UI\Image\favicon.ico", duration=15, threaded=True
    )
    if sys.platform.startswith("win"):
        win32api.MessageBox(0, text, title, win32con.MB_OK)


def dict_result(text):
    # json string 转 dict object
    return dict(json.loads(text))


def test_network():
    # 网络状态测试
    try:
        http = urllib3.PoolManager()
        http.request("GET", "https://pro.yuketang.cn")
        return True
    except:
        return False


# 类泊松分布：答题等待时间
def lam(limit, percent=None):
    if percent == None:
        if limit == -1:
            lam = random.randint(5, 25)
        elif limit <= 30:
            lam = limit / 3
        elif limit >= 90:
            lam = limit / 2 - 30
        else:
            lam = limit / 5
    else:
        if limit == -1:
            lam = random.randint(5, 25)
        else:
            lam = limit * percent * 0.9 / 150
    return lam


def rand_poisson(lam):
    base = exp(-lam)
    sum = 1
    answer_time = 0
    while sum > base:
        sum = sum * random.random()
        answer_time += 1
    return min(answer_time, lam * 1.4)


def calculate_waittime(limit, type, custom_percent=50):
    # 计算答题等待时间
    """
    type
    1: 中庸
    2: 激进
    3: 保守
    4: 自定义
    """
    if limit == -1:
        limit = 60
    if type == 1:
        wait_time = rand_poisson(lam(limit, 65))
    elif type == 2:
        wait_time = rand_poisson(lam(limit, 35))
    elif type == 3:
        wait_time = limit * 0.2 + rand_poisson(lam(limit, 85)) * 0.8
    elif type == 4:
        wait_time = rand_poisson(lam(limit, custom_percent))
    if wait_time > limit:
        if __name__ == "__main__":
            raise Exception("Error: wait_time > limit")
        wait_time = random.randint(int(limit * 0.25), int(limit * 0.75))
    return int(wait_time)


def get_initial_data(old_config=None):
    # 默认配置信息
    initial_data = {
        "sessionid": "",
        "region": "1",
        "auto_danmu": False,
        "danmu_config": {"danmu_limit": 5},
        "audio_on": True,
        "audio_config": {
            "audio_type": {
                "send_danmu": False,
                "others_danmu": False,
                "receive_problem": True,
                "answer_result": True,
                "im_called": True,
                "others_called": True,
                "course_info": True,
                "network_info": True,
            }
        },
        "auto_answer": True,
        "answer_config": {"answer_delay": {"type": 1, "custom": {"percent": 50}}},
        "sign_config": {
            "delay_time": {"type": 1, "custom": {"time": 120, "cutoff": 120}}
        },
    }

    if old_config:
        for key in old_config:
            if key in initial_data:
                initial_data[key] = old_config[key]

    return initial_data


def get_config_path():
    # 获取配置文件路径
    config_route = get_config_dir() + "\\config.json"
    return config_route


def get_config_dir():
    # 获取配置文件所在文件夹
    appdata_route = os.environ["APPDATA"]
    dir_route = appdata_route + "\\RainClassroomAssistant"
    return dir_route


def get_user_info(sessionid, region):
    # 获取用户信息
    headers = {
        "Cookie": "sessionid=%s" % sessionid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    }
    r = requests.get(
        url=f"https://{get_host(region)}/api/v3/user/basic-info",
        headers=headers,
        proxies={"http": None, "https": None},
    )
    rtn = dict_result(r.text)
    return (rtn["code"], rtn["data"])


def get_on_lesson(sessionid, region):
    # 获取用户当前正在上课列表
    headers = {
        "Cookie": "sessionid=%s" % sessionid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    }
    r = requests.get(
        f"https://{get_host(region)}/api/v3/classroom/on-lesson",
        headers=headers,
        proxies={"http": None, "https": None},
    )
    rtn = dict_result(r.text)
    return rtn["data"]["onLessonClassrooms"]


def get_on_lesson_old(sessionid, region):
    # 获取用户当前正在上课的列表（旧版）
    headers = {
        "Cookie": "sessionid=%s" % sessionid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    }
    r = requests.get(
        f"https://{get_host(region)}/v/course_meta/on_lesson_courses",
        headers=headers,
        proxies={"http": None, "https": None},
    )
    rtn = dict_result(r.text)
    return rtn["on_lessons"]


def get_host(index):
    # 获取host
    host = [
        "www.yuketang.cn",
        "pro.yuketang.cn",
        "changjiang.yuketang.cn",
        "huanghe.yuketang.cn",
    ]
    return host[int(index)]


def get_name(index):
    # 获取host
    name = ["雨课堂", "荷塘雨课堂", "长江雨课堂", "黄河雨课堂"]
    return name[int(index)]


def resource_path(relative_path):
    # 解决打包exe的图片路径问题
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    x = []
    limit = 60
    percent = 95
    _type = 4
    if _type == 1:
        percent = 65
    elif _type == 2:
        percent = 35
    elif _type == 3:
        percent = 85
    lamb = lam(limit, percent)
    print(f"lam = {lamb}")
    _max = 0
    for i in range(100):
        x.append(calculate_waittime(limit, _type, percent))
        if x[i] > _max:
            _max = x[i]
        if x[i] > limit * percent / 100:
            print("error")
            print(x[i])
            break

    print(sum(x) / len(x))
    print(_max, _max / limit / percent * 100)
    show_info(
        f"x的问题没有找到答案，请在{calculate_waittime(limit, _type, percent)}秒内前往雨课堂回答",
        "Problem",
    )
