import hashlib
import os
import re
import threading
import time

import PyPDF2
import requests
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont


class PPTManager:
    threading_count = 8
    title_dict = {}

    def __init__(self, data, lessonname, downloadpath="downloads"):
        self.lessonname = self.validateTitle(lessonname)
        self.title = self.validateTitle(data["title"]).strip()
        self.title_dict[self.title] = 1
        self.timestamp = str(time.time())
        self.timeinfo = time.strftime(
            "%Y%m%d-%H%M%S", time.localtime(float(self.timestamp))
        )
        self.downloadpath = downloadpath

        self.lessondownloadpath = downloadpath + "\\" + self.lessonname

        self.cachedirpath = downloadpath + "\\rainclasscache"
        self.lessonpath = self.cachedirpath + "\\" + self.lessonname
        self.titlepath = self.lessonpath + "\\" + self.title
        self.imgpath = self.titlepath + "\\" + self.timestamp

        self.slides = data["slides"]
        self.width = data["width"]
        self.height = data["height"]
        self.md5_list = []
        self.check_dir()

    def validateTitle(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def check_dir(self):
        if not os.path.exists(self.downloadpath):
            os.mkdir(self.downloadpath)

        if not os.path.exists(self.lessondownloadpath):
            os.mkdir(self.lessondownloadpath)

        if not os.path.exists(self.cachedirpath):
            os.mkdir(self.cachedirpath)
        if not os.path.exists(self.lessonpath):
            os.mkdir(self.lessonpath)
        if not os.path.exists(self.titlepath):
            os.mkdir(self.titlepath)
        if not os.path.exists(self.imgpath):
            os.mkdir(self.imgpath)

    def download(self):
        download_thread = []
        div_num = int(len(self.slides) / self.threading_count)
        if div_num < 1:
            div_num = 1
        for i in range(0, len(self.slides), div_num):
            slides = self.slides[i : min(i + div_num, len(self.slides))]
            download_thread.append(self.DownloadThread(slides, self.imgpath))
        for thread in download_thread:
            thread.start()
        for thread in download_thread:
            thread.join()

    def get_problems(self):
        slides = [problem for problem in self.slides if "problem" in problem.keys()]
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
        pdf_name = self.title + ".pdf"
        for slide in self.slides:
            image_name = self.imgpath + "\\" + str(slide["index"]) + ".jpg"
            md5 = self.get_md5(image_name)
            self.md5_list.append(md5)
            if "problem" in slide.keys():
                problem = slide["problem"]
                # print(problem)
                img = Image.open(image_name)
                font = ImageFont.truetype("C:\\Windows\\Fonts\\msyh.ttc", 30)
                draw = ImageDraw.Draw(img)
                draw.text(
                    (50, 50),
                    str(problem["answers"]),
                    fill=(255, 0, 0),
                    font=font,
                )
                img.save(image_name)
        with open(self.imgpath + "\\md5.txt", "w") as f:
            for md5 in self.md5_list:
                f.write(md5 + "\n")
        hash = self.get_sha256(self.imgpath + "\\md5.txt")
        print(self.title + ":" + hash)
        for pdf in os.scandir(self.downloadpath):
            if pdf.path == self.downloadpath + "\\" + pdf_name:
                os.replace(pdf.path, self.lessondownloadpath + "\\" + pdf_name)
        for pdf in os.scandir(self.lessondownloadpath):
            if pdf.name.endswith(".pdf"):
                try:
                    keywords = PyPDF2.PdfReader(open(pdf.path, "rb")).metadata.get(
                        "/Keywords"
                    )
                    if hash == keywords:
                        return pdf.name
                except Exception as e:
                    print(e)
        ppt = FPDF("L", "pt", [self.height, self.width])
        ppt.set_keywords(hash)
        ppt.set_author("RainClassroom")
        for slide in self.slides:
            image_name = self.imgpath + "\\" + str(slide["index"]) + ".jpg"
            ppt.add_page()
            ppt.image(image_name, 0, 0, h=self.height, w=self.width)
        if os.path.exists(self.lessondownloadpath + "\\" + pdf_name):
            pdf_name = self.title + str(self.timeinfo) + ".pdf"
        ppt.output(self.lessondownloadpath + "\\" + pdf_name)
        return pdf_name

    def delete_cache(self):
        for file in os.listdir(self.imgpath):
            os.remove(self.imgpath + "\\" + file)
        os.rmdir(self.imgpath)

    def start(self):
        if self.title_dict.get(self.title) is None:
            return None, None
        self.download()
        pdfname = self.generate_ppt()
        self.delete_cache()
        usetime = round(time.time() - float(self.timestamp), 4)
        del self.title_dict[self.title]
        return pdfname, usetime

    def __eq__(self, __value: object) -> bool:
        if self.title != __value.title:
            return False
        else:
            return self.slides == __value.slides

    class DownloadThread(threading.Thread):
        def __init__(self, slides, cacheimgpath):
            threading.Thread.__init__(self)
            self.slides = slides
            self.imgpath = cacheimgpath

        def download(self, slide):
            url = slide["cover"]
            if url == "":
                return
            index = slide["index"]
            image_name = self.imgpath + "\\" + str(index) + ".jpg"
            with open(image_name, "wb") as f:
                f.write(requests.get(url).content)

        def run(self):
            for slide in self.slides:
                self.download(slide)


if __name__ == "__main__":
    data = {
        "title": "第一章",
        "slides": [
            {
                "index": 1,
                "cover": "https://rainclass.oss-cn-shanghai.aliyuncs.com/cover/2021/09/17/1631861003.jpg",
                "problem": {"answers": [1, 2, 3, 4]},
            },
            {
                "index": 2,
                "cover": "https://rainclass.oss-cn-shanghai.aliyuncs.com/cover/2021/09/17/1631861003.jpg",
                "problem": {"answers": [1, 2, 3, 4]},
            },
        ],
        "width": 1920,
        "height": 1080,
    }

    def get_time(function):
        start_time = time.time()
        for image in os.listdir(ppt.cachepath):
            function(ppt.cachepath + "\\" + image)
        end_time = time.time()
        print(function.__name__)
        print(
            f"{end_time - start_time}/{len(os.listdir(ppt.cachepath))}={(end_time - start_time)/len(os.listdir(ppt.cachepath))}"
        )
        print("----------------------------------------------------------------")

    downloadpath = "downloads"
    ppt = PPTManager(data, downloadpath)
    get_time(ppt.get_md5)
    get_time(ppt.get_sha256)
    ppt.start()
