import os
import threading
import time
import hashlib

import requests
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont


class PPTManager:
    threading_count = 4

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
            print(i, i+div_num)
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

    def get_sha(self, file):
        with open(file, "rb") as f:
            sha = hashlib.sha256(f.read()).hexdigest()
        return sha

    def generate_ppt(self):
        new_flag = False
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
                print(problem["answers"])
                img.save(image_name)
            print(slide)
            sha = self.get_sha(image_name)
            if sha not in self.hash_list:
                new_flag = True
            self.hash_list.add(sha)
        if not new_flag:
            print("No new slides")
            return
        ppt = FPDF("L", "pt", [self.height, self.width])
        pdf_name = self.title + ".pdf"
        for slide in self.slides:
            image_name = self.cachepath + "\\" + str(slide["index"]) + ".jpg"
            ppt.add_page()
            ppt.image(image_name, 0, 0, self.height, self.width)
        if os.path.exists(self.downloadpath + "\\" + pdf_name):
            time_info = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            pdf_name = self.title + str(time_info) + ".pdf"
        ppt.output(self.downloadpath + "\\" + pdf_name)

    def start(self):
        self.download()
        self.generate_ppt()

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
            for slide in self.slides:
                self.download(slide)
