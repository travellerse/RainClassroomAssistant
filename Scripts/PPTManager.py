import hashlib
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont


class PPTManager:
    threading_count = 4
    title_dict = {}

    def __init__(self, data, downloadpath):
        self.title = data["title"].replace("/", "_").strip()
        self.downloadpath = downloadpath
        self.cachedirpath = downloadpath + "\\rainclasscache"
        self.cachepath = downloadpath + "\\rainclasscache\\" + self.title
        self.slides = data["slides"]
        self.width = data["width"]
        self.height = data["height"]
        self.hash_list = set()
        self.check_dir()

    def check_dir(self):
        if not os.path.exists(self.downloadpath):
            os.mkdir(self.downloadpath)
        if not os.path.exists(self.cachedirpath):
            os.mkdir(self.cachedirpath)
        if not os.path.exists(self.cachepath):
            os.mkdir(self.cachepath)

    def download(self):
        download_thread = []
        div_num = int(len(self.slides)/self.threading_count)
        for i in range(0, len(self.slides), div_num):
            slides = self.slides[i:i+div_num]
            download_thread.append(self.DownloadThread(slides, self.cachepath))
        for thread in download_thread:
            thread.start()
        for thread in download_thread:
            thread.join()

    def get_problems(self):
        slides = [problem for problem in self.slides
                  if "problem" in problem.keys()]
        index = [problem["index"] for problem in slides]
        problems = [problem["problem"] for problem in slides]
        for i in range(len(problems)):
            problems[i]["index"] = index[i]
        return problems

    def get_md5(self, file):
        with open(file, "rb") as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        return md5

    def get_sha256(self, file):
        with open(file, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()
        return sha256

    def add_hash(self, path):
        for img in os.listdir(path):
            self.hash_list.add(self.get_md5(path + "\\" + img))
            print(path + "\\" + img)

    def generate_ppt(self):
        new_flag = False
        pdf_name = self.title + ".pdf"
        if os.path.exists(self.downloadpath + "\\" + pdf_name):
            self.add_hash(self.cachepath)
        for slide in self.slides:
            image_name = self.cachepath + "\\" + str(slide["index"]) + ".jpg"
            if "problem" in slide.keys():
                problem = slide["problem"]
                # print(problem)
                img = Image.open(image_name)
                font = ImageFont.truetype(
                    "C:\\Windows\\Fonts\\msyh.ttc", 30)
                draw = ImageDraw.Draw(img)
                draw.text(
                    (50, 50),
                    str(problem["answers"]),
                    fill=(255, 0, 0),
                    font=font,
                )
                img.save(image_name)
            md5 = self.get_md5(image_name)
            if md5 not in self.hash_list:
                print(f"New slide: {slide['index']}")
                new_flag = True
            self.hash_list.add(md5)
        if not new_flag:
            print("No new slides")
            return
        ppt = FPDF("L", "pt", [self.height, self.width])
        for slide in self.slides:
            image_name = self.cachepath + "\\" + str(slide["index"]) + ".jpg"
            ppt.add_page()
            ppt.image(image_name, 0, 0, h=self.height, w=self.width)
        if os.path.exists(self.downloadpath + "\\" + pdf_name):
            mtime = os.path.getmtime(self.downloadpath + "\\" + pdf_name)
            day = time.strftime("%Y%m%d", time.localtime(mtime))
            if day != time.strftime("%Y%m%d", time.localtime()):
                time_info = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                pdf_name = self.title + str(time_info) + ".pdf"
        ppt.output(self.downloadpath + "\\" + pdf_name)

    def start(self):
        if self.title in self.title_dict:
            print("PPTManager with the same title is already running.")
            return
        self.title_dict[self.title] = self
        self.download()
        self.generate_ppt()
        del self.title_dict[self.title]

    class DownloadThread(threading.Thread):
        def __init__(self, slides, cachepath):
            threading.Thread.__init__(self)
            self.slides = slides
            self.cachepath = cachepath

        def download(self, slide):
            url = slide["cover"]
            if url == "":
                return
            index = slide["index"]
            image_name = self.cachepath + "\\" + str(index) + ".jpg"
            with open(image_name, "wb") as f:
                f.write(requests.get(url).content)

        def run(self):
            with ThreadPoolExecutor() as executor:  # Use ThreadPoolExecutor
                for slide in self.slides:
                    # Submit download tasks to the thread pool
                    executor.submit(self.download, slide)


if __name__ == "__main__":
    data = {
        "title": "第一章",
        "slides": [
            {
                "index": 1,
                "cover": "https://rainclass.oss-cn-shanghai.aliyuncs.com/cover/2021/09/17/1631861003.jpg",
                "problem": {
                    "answers": [1, 2, 3, 4]
                }
            },
            {
                "index": 2,
                "cover": "https://rainclass.oss-cn-shanghai.aliyuncs.com/cover/2021/09/17/1631861003.jpg",
                "problem": {
                    "answers": [1, 2, 3, 4]
                }
            }
        ],
        "width": 1920,
        "height": 1080
    }

    def get_time(function):
        start_time = time.time()
        for image in os.listdir(ppt.cachepath):
            function(ppt.cachepath + "\\" + image)
        end_time = time.time()
        print(function.__name__)
        print(f"{end_time - start_time}/{len(os.listdir(ppt.cachepath))}={(end_time - start_time)/len(os.listdir(ppt.cachepath))}")
        print("----------------------------------------------------------------")

    downloadpath = "downloads"
    ppt = PPTManager(data, downloadpath)
    get_time(ppt.get_md5)
    get_time(ppt.get_sha256)
    ppt.start()
