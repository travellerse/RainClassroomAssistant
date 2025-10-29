import json
import random
import threading
import time
import traceback

import requests
import websocket

from Scripts.PPTManager import PPTManager
from Scripts.Utils import (
    calculate_waittime,
    dict_result,
    get_user_info,
    is_debug,
    get_host,
)


class Lesson:
    def __init__(self, lessonid, lessonname, classroomid, main_ui):
        self.classroomid = classroomid
        self.lessonid = lessonid
        self.lessonname = lessonname
        self.sessionid = main_ui.config["sessionid"]
        self.headers = {
            "Cookie": "sessionid=%s" % self.sessionid,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        }
        self.receive_danmu = {}
        self.sent_danmu_dict = {}
        self.danmu_dict = {}
        self.problems_ls = []
        self.problems_dict = {}
        self.unlocked_problem = []
        self.classmates_ls = []
        self.add_message = main_ui.add_message_signal.emit
        self.add_course = main_ui.add_course_signal.emit
        self.del_course = main_ui.del_course_signal.emit
        self.config = main_ui.config
        self.region = int(self.config["region"])
        code, rtn = get_user_info(self.sessionid, self.config["region"])
        self.user_uid = rtn["id"]
        self.user_uname = rtn["name"]
        self.main_ui = main_ui
        # self.pptmanager_dict = {}

    def _download(self, data):
        data["title"] = data["title"].replace("/", "_").strip()
        self.print_problems(data)
        self.add_message("开始下载ppt : " + data["title"] + ".pdf", 0)
        try:
            pdfname, usetime = PPTManager(data, self.lessonname).start()
            if pdfname is None or usetime is None:
                if is_debug():
                    self.add_message(
                        "重复下载ppt取消 : " + pdfname + f"，耗时{usetime}秒", 0
                    )
                return
            self.add_message("下载ppt成功 : " + pdfname + f"，耗时{usetime}秒", 0)
        except Exception as e:
            self.add_message("下载ppt失败 : " + data["title"] + ".pdf", 0)
            self.add_message(traceback.format_exc(), 0)

    def download_ppt(self, presentationid):
        threading.Thread(
            target=self._download, args=(self._get_ppt(presentationid),), daemon=True
        ).start()

    def _get_ppt(self, presentationid):
        # 获取课程各页ppt
        r = requests.get(
            url=f"https://{get_host(self.config['region'])}/api/v3/lesson/presentation/fetch?presentation_id={presentationid}",
            headers=self.headers,
            proxies={"http": None, "https": None},
        )
        return dict_result(r.text)["data"]

    def print_problems(self, data):
        answers = {}
        slides = [problem for problem in data["slides"] if "problem" in problem.keys()]
        index = [problem["index"] for problem in slides]
        problems = [problem["problem"] for problem in slides]
        for i in range(len(problems)):
            problems[i]["index"] = index[i]
        for problem in problems:
            answers[problem["index"]] = problem["answers"]
        self.add_message(
            f"{self.lessonname}:{data['title']} 的答案为" + str(answers), 0
        )

    def get_problems(self, presentationid):
        # 获取课程ppt中的题目
        data = self._get_ppt(presentationid)
        slides = [problem for problem in data["slides"] if "problem" in problem.keys()]
        index = [problem["index"] for problem in slides]
        problems = [problem["problem"] for problem in slides]
        for i in range(len(problems)):
            problems[i]["index"] = index[i]
        return problems

    def answer_questions(self, problemid, problemtype, answer, limit):
        # 回答问题
        if answer and problemtype != 3:
            wait_time = calculate_waittime(
                limit,
                self.config["answer_config"]["answer_delay"]["type"],
                self.config["answer_config"]["answer_delay"]["custom"]["percent"],
            )
            if wait_time != 0:
                meg = "%s检测到问题，将在%s秒后自动回答，答案为%s" % (
                    self.lessonname,
                    wait_time,
                    answer,
                )
                # threading.Thread(target=say_something,args=(meg,)).start()
                self.add_message(meg, 3)
                time.sleep(wait_time)
            else:
                meg = "%s检测到问题，剩余时间小于15秒，将立即自动回答，答案为%s" % (
                    self.lessonname,
                    answer,
                )
                self.add_message(meg, 3)
                # threading.Thread(target=say_something,args=(meg,)).start()
            data = {
                "problemId": problemid,
                "problemType": problemtype,
                "dt": int(time.time()),
                "result": answer,
            }
            r = requests.post(
                url=f"https://{get_host(self.config['region'])}/api/v3/lesson/problem/answer",
                headers=self.headers,
                data=json.dumps(data),
                proxies={"http": None, "https": None},
            )
            return_dict = dict_result(r.text)
            if return_dict["code"] == 0:
                meg = "%s自动回答成功" % self.lessonname
                self.add_message(meg, 4)
                # threading.Thread(target=say_something,args=(meg,)).start()
                return True
            else:
                meg = "%s自动回答失败，原因：%s" % (
                    self.lessonname,
                    return_dict["msg"].replace("_", " "),
                )
                self.add_message(meg, 4)
                # threading.Thread(target=say_something,args=(meg,)).start()
                return False
        else:
            if limit == -1:
                meg = "%s的问题没有找到答案，该题不限时，请尽快前往雨课堂回答" % (
                    self.lessonname
                )
            else:
                meg = "%s的问题没有找到答案，请在%s秒内前往雨课堂回答" % (
                    self.lessonname,
                    limit,
                )
            # threading.Thread(target=say_something,args=(meg,)).start()
            self.add_message(meg, 4)
            return False

    def on_open(self, wsapp):
        self.handshark = {
            "op": "hello",
            "userid": self.user_uid,
            "role": "student",
            "auth": self.auth,
            "lessonid": self.lessonid,
        }
        wsapp.send(json.dumps(self.handshark))

    def checkin_class(self):
        r = requests.post(
            url=f"https://{get_host(self.config['region'])}/api/v3/lesson/checkin",
            headers=self.headers,
            data=json.dumps({"source": 5, "lessonId": self.lessonid}),
            proxies={"http": None, "https": None},
        )
        set_auth = r.headers.get("Set-Auth", None)
        times = 1
        while not set_auth and times <= 3:
            set_auth = r.headers.get("Set-Auth", None)
            times += 1
            time.sleep(1)
        self.headers["Authorization"] = "Bearer %s" % set_auth
        return dict_result(r.text)["data"]["lessonToken"]

    def on_message(self, wsapp, message):
        data = dict_result(message)
        op = data["op"]
        if is_debug():
            print(op)
            self.add_message(op, 0)
        if op == "hello":
            presentations = list(
                set(
                    [
                        slide["pres"]
                        for slide in data["timeline"]
                        if slide["type"] == "slide"
                    ]
                )
            )
            print(data)
            current_presentation = data["presentation"]
            if current_presentation not in presentations:
                presentations.append(current_presentation)
            for presentationid in presentations:
                # print(presentationid)
                self.problems_ls.extend(self.get_problems(presentationid))
                for problem in self.problems_ls:
                    self.problems_dict[problem["index"]] = problem["answers"]
                self.download_ppt(presentationid)
            self.unlocked_problem = data["unlockedproblem"]
            for problemid in self.unlocked_problem:
                self._current_problem(wsapp, problemid)
        elif op == "unlockproblem":
            self.start_answer(data["problem"]["sid"], data["problem"]["limit"])
        elif op == "lessonfinished":
            meg = "%s下课了" % self.lessonname
            # threading.Thread(target=say_something,args=(meg,)).start()
            self.add_message(meg, 7)
            wsapp.close()
        elif op == "presentationupdated":
            self.problems_ls.extend(self.get_problems(data["presentation"]))
            for problem in self.problems_ls:
                self.problems_dict[problem["index"]] = problem["answers"]
            self.download_ppt(data["presentation"])
        elif op == "presentationcreated":
            self.problems_ls.extend(self.get_problems(data["presentation"]))
            for problem in self.problems_ls:
                self.problems_dict[problem["index"]] = problem["answers"]
            self.download_ppt(data["presentation"])
        elif op == "newdanmu" and self.config["auto_danmu"]:
            current_content = data["danmu"].lower()
            uid = data["userid"]
            sent_danmu_user = User(uid)
            if sent_danmu_user in self.classmates_ls:
                for i in self.classmates_ls:
                    if i == sent_danmu_user:
                        meg = "%s课程的%s%s发送了弹幕：%s" % (
                            self.lessonname,
                            i.sno,
                            i.name,
                            data["danmu"],
                        )
                        self.add_message(meg, 2)
                        break
            else:
                self.classmates_ls.append(sent_danmu_user)
                sent_danmu_user.get_userinfo(self.classroomid, self.headers)
                meg = "%s课程的%s%s发送了弹幕：%s" % (
                    self.lessonname,
                    sent_danmu_user.sno,
                    sent_danmu_user.name,
                    data["danmu"],
                )
                self.add_message(meg, 2)
            now = time.time()
            # 收到一条弹幕，尝试取出其之前的所有记录的列表，取不到则初始化该内容列表
            try:
                same_content_ls = self.danmu_dict[current_content]
            except KeyError:
                self.danmu_dict[current_content] = []
                same_content_ls = self.danmu_dict[current_content]
            # 清除超过60秒的弹幕记录
            for i in same_content_ls:
                if now - i > 60:
                    same_content_ls.remove(i)
            # 如果当前的弹幕没被发过，或者已发送时间超过60秒
            if (
                current_content not in self.sent_danmu_dict.keys()
                or now - self.sent_danmu_dict[current_content] > 60
            ):
                if (
                    len(same_content_ls) + 1
                    >= self.config["danmu_config"]["danmu_limit"]
                ):
                    self.send_danmu(current_content)
                    same_content_ls = []
                    self.sent_danmu_dict[current_content] = now
                else:
                    same_content_ls.append(now)
        elif op == "callpaused":
            meg = "%s点名了，点到了：%s" % (self.lessonname, data["name"])
            if self.user_uname == data["name"]:
                self.add_message(meg, 5)
            else:
                self.add_message(meg, 6)
        # 程序在上课中途运行，由_current_problem发送的已解锁题目数据，得到的返回值。
        # 此处需要筛选未到期的题目进行回答。
        elif op == "probleminfo":
            if data["limit"] != -1:
                time_left = int(
                    data["limit"] - (int(data["now"]) - int(data["dt"])) / 1000
                )
            else:
                time_left = data["limit"]
            # 筛选未到期题目
            if time_left > 0 or time_left == -1:
                if self.config["auto_answer"]:
                    self.start_answer(data["problemid"], time_left)
                else:
                    self.add_message(
                        "%s检测到问题，但未开启自动回答" % self.lessonname, 3
                    )

    def start_answer(self, problemid, limit):
        for promble in self.problems_ls:
            if promble["problemId"] == problemid:
                if promble["result"] is not None:
                    # 如果该题已经作答过，直接跳出函数以忽略该题
                    # 该情况理论上只会出现在启动监听时
                    return
                blanks = promble.get("blanks", [])
                answers = []
                if blanks:
                    for i in blanks:
                        answers.append(random.choice(i["answers"]))
                else:
                    answers = promble.get("answers", [])
                threading.Thread(
                    target=self.answer_questions,
                    args=(promble["problemId"], promble["problemType"], answers, limit),
                ).start()
                break
        else:
            if limit == -1:
                meg = "%s的问题没有找到答案，该题不限时，请尽快前往雨课堂回答" % (
                    self.lessonname
                )
            else:
                meg = "%s的问题没有找到答案，请在%s秒内前往雨课堂回答" % (
                    self.lessonname,
                    limit,
                )
            self.add_message(meg, 4)
            # threading.Thread(target=say_something,args=(meg,)).start()

    def _current_problem(self, wsapp, promblemid):
        # 为获取已解锁的问题详情信息，向wsapp发送probleminfo
        query_problem = {
            "op": "probleminfo",
            "lessonid": self.lessonid,
            "problemid": promblemid,
            "msgid": 1,
        }
        wsapp.send(json.dumps(query_problem))

    def start_lesson(self, delay, callback):
        self.auth = self.checkin_class()
        rtn = self.get_lesson_info()
        teacher = rtn["teacher"]["name"]
        title = rtn["title"]
        timestamp = rtn["startTime"] // 1000
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        index = self.main_ui.tableWidget.rowCount()
        self.add_course([self.lessonname, title, teacher, time_str], index)
        if self.lessonname.find("清华实践") != -1:
            meg = "%s测试课程，不进行监听" % self.lessonname
            self.add_message(meg, 7)
            return callback(self)
        if (
            int(time.time()) - timestamp
            <= self.config["sign_config"]["delay_time"]["custom"]["cutoff"]
            and delay > 0
        ):
            meg = f"检测到课程{self.lessonname}正在上课，将于{delay}秒后加入监听列表"
            self.add_message(meg, 7)
            time.sleep(delay)
        else:
            meg = f"检测到课程{self.lessonname}正在上课，已加入监听列表"
            self.add_message(meg, 7)
        self.wsapp = websocket.WebSocketApp(
            url=f"wss://{get_host(self.config['region'])}/wsapp/",
            header=self.headers,
            on_open=self.on_open,
            on_message=self.on_message,
        )
        self.wsapp.run_forever()
        meg = "%s监听结束" % self.lessonname
        self.add_message(meg, 7)
        self.del_course(index)
        # threading.Thread(target=say_something,args=(meg,)).start()
        return callback(self)

    def send_danmu(self, content):
        url = f"https://{get_host(self.config['region'])}/api/v3/lesson/danmu/send"
        data = {
            "extra": "",
            "fromStart": "50",
            "lessonId": self.lessonid,
            "message": content,
            "requiredCensor": False,
            "showStatus": True,
            "target": "",
            "userName": "",
            "wordCloud": True,
        }
        r = requests.post(
            url=url,
            headers=self.headers,
            data=json.dumps(data),
            proxies={"http": None, "https": None},
        )
        if dict_result(r.text)["code"] == 0:
            meg = "%s弹幕发送成功！内容：%s" % (self.lessonname, content)
        else:
            meg = "%s弹幕发送失败！内容：%s" % (self.lessonname, content)
        self.add_message(meg, 1)

    def get_lesson_info(self):
        url = f"https://{get_host(self.config['region'])}/api/v3/lesson/basic-info"
        r = requests.get(
            url=url, headers=self.headers, proxies={"http": None, "https": None}
        )
        return dict_result(r.text)["data"]

    def __eq__(self, other):
        return self.lessonid == other.lessonid


class User:
    def __init__(self, uid):
        self.uid = uid

    def get_userinfo(self, classroomid, headers):
        r = requests.get(
            f"https://{get_host(self.config['region'])}/v/course_meta/fetch_user_info_new?query_user_id={self.uid}&classroom_id={classroomid}",
            headers=headers,
            proxies={"http": None, "https": None},
        )
        data = dict_result(r.text)["data"]
        self.sno = data["school_number"]
        self.name = data["name"]
