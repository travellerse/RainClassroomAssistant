import random
import threading
import time
import traceback

import requests

from Scripts.Classes import Lesson
from Scripts.Utils import get_on_lesson, test_network


def monitor(main_ui):
    # 监听器函数

    def del_onclass(lesson_obj):
        # 作为回调函数传入start_lesson
        on_lesson_list.remove(lesson_obj)

    # 已经签到完成加入监听列表的课程
    on_lesson_list = []
    # 检测到的未加入监听列表的课程
    lesson_list = []
    network_status = True
    sessionid = main_ui.config["sessionid"]
    while True:
        # 获取课程列表
        try:
            lesson_list = get_on_lesson(sessionid, main_ui.config["region"])
            # lesson_list_old = get_on_lesson_old()
        except requests.exceptions.ConnectionError:
            meg = "网络异常，监听中断"
            main_ui.add_message_signal.emit(meg, 8)
            network_status = False
            main_ui.add_message_signal.emit(traceback.format_exc(), 0)
        except Exception:
            main_ui.add_message_signal.emit(traceback.format_exc(), 0)
        # 网络异常处理
        while not network_status:
            ret = test_network()
            if ret == True:
                try:
                    lesson_list = get_on_lesson(sessionid, main_ui.config["region"])
                    # lesson_list_old = get_on_lesson_old()
                except:
                    main_ui.add_message_signal.emit(traceback.format_exc(), 0)
                else:
                    network_status = True
                    meg = "网络已恢复，监听开始"
                    main_ui.add_message_signal.emit(meg, 8)
                    break
            # 可结束线程的计时器
            timer = 0
            while timer <= 5:
                time.sleep(1)
                timer += 1
                if not main_ui.is_active:
                    # 由于on_lesson_list在多线程操作之下，此处必须使用列表复制，以保证列表完整性
                    for lesson in on_lesson_list.copy():
                        lesson.wsapp.close()
                    return
        # 课程列表
        for lesson in lesson_list:
            lessionid = lesson["lessonId"]
            lessonname = lesson["courseName"]
            classroomid = lesson["classroomId"]
            lesson_obj = Lesson(lessionid, lessonname, classroomid, main_ui)
            if lesson_obj not in on_lesson_list:
                if main_ui.config["sign_config"]["delay_time"]["type"] == 1:
                    delay_time = random.randint(
                        10,
                        max(
                            10,
                            main_ui.config["sign_config"]["delay_time"]["custom"][
                                "time"
                            ],
                        ),
                    )
                else:
                    delay_time = 0
                thread = threading.Thread(
                    target=lesson_obj.start_lesson,
                    args=(
                        delay_time,
                        del_onclass,
                    ),
                    daemon=True,
                )
                thread.start()
                on_lesson_list.append(lesson_obj)

        # for lesson in lesson_list_old:
        #     lessionid = lesson["lesson_id"]
        #     lessonname = lesson["classroom"]["name"]
        #     classroomid = lesson["classroomId"]

        # 可结束线程的计时器
        timer = 0
        while timer <= 30:
            time.sleep(1)
            timer += 1
            if not main_ui.is_active:
                # 由于on_lesson_list在多线程操作之下，此处必须使用列表复制，以保证列表完整性
                for lesson in on_lesson_list.copy():
                    lesson.wsapp.close()
                return
