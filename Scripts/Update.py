import os
import re
import sys

import requests

if os.name == "nt":
    import win32api

from Scripts.Utils import is_debug


def get_version():
    version = ""
    if is_debug():
        with open("file_version_info.txt", "r") as f:
            version_info = f.read()
        version = (
            re.search("u'FileVersion', u'.*'",
                      version_info).group().split("'")[3]
        )
    else:
        if os.name == "nt":
            info = win32api.GetFileVersionInfo(
                win32api.GetModuleFileName(
                    win32api.GetModuleHandle(None)), "\\"
            )  # 获取文件版本信息
            ms = info["FileVersionMS"]
            ls = info["FileVersionLS"]
            version = "%d.%d.%d" % (
                win32api.HIWORD(ms),
                win32api.LOWORD(ms),
                win32api.HIWORD(ls),
            )
        elif (os.paltform == "ios"):
            version = "1.0.0"
    return Version(version)  # 获取文件版本号


class Update:
    def __init__(self, path):
        self.url = "https://gitee.com/travellerse/rain-classroom-assistant-releases/releases/latest/download/RainClassroomAssistant.exe"
        self.path = path
        self.filename = "RainClassroomAssistant.exe"

    def get_url(self):
        tag_url = "https://gitee.com/travellerse/rain-classroom-assistant-releases/releases/latest"
        r = requests.get(tag_url)
        tag = re.search(
            r"travellerse/rain-classroom-assistant-releases/releases/tag/.+?\"", r.text).group()
        tag = tag.split("/")[-1][:-1]
        print(tag)
        self.url = f"https://gitee.com/travellerse/rain-classroom-assistant-releases/releases/download/{tag}/RainClassroomAssistant.exe"
        print(self.url)

    def get_latest_version(self):
        version_latest = "https://gitee.com/travellerse/rain-classroom-assistant-releases/raw/master/version.txt"
        return Version(requests.get(version_latest).text)

    def release_update_script(self):
        with open(self.path+"update.py", "w") as f:
            f.write(
                "import os\n"
                "import time\n"
                "import sys\n"
                "try:\n"
                "   os.system('taskkill /f /im RainClassroomAssistant.exe')\n"
                "except:\n"
                "   pass\n"
                "time.sleep(2)\n"
                "path = os.path.dirname(os.path.realpath(__file__))+'\\\\'\n"
                "os.remove(path+'RainClassroomAssistant.exe')\n"
                "os.rename(path+'_RainClassroomAssistant.exe', path+'RainClassroomAssistant.exe')\n"
                "os.system(path+'RainClassroomAssistant.exe')\n"
                "sys.exit(0)\n"
            )

    def download(self):
        with open(self.path+"_"+self.filename, "wb") as f:
            f.write(requests.get(self.url).content)

    def update(self):
        self.get_url()
        self.download()
        self.release_update_script()
        os.system("python "+self.path+"update.py")
        sys.exit(0)

    def have_new_version(self):
        latest_version = self.get_latest_version()
        current_version = get_version()
        return latest_version > current_version

    def start(self):
        latest_version = self.get_latest_version()
        print(f"最新版本：{latest_version}")
        current_version = get_version()
        print(f"当前版本：{current_version}")
        if latest_version > current_version:
            print("有新版本")
            self.update()
        else:
            print("没有新版本")


class Version:
    # 语义化版本号
    def __init__(self, version: str):
        self.version = version
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.prerelease = ""
        self.buildmetadata = ""
        self.parse_version()

    def parse_version(self):
        version = self.version
        version = version.split("+")
        if len(version) == 2:
            self.buildmetadata = version[1]
        version = version[0].split("-")
        if len(version) == 2:
            self.prerelease = version[1]
        version = version[0].split(".")
        self.major = int(version[0])
        self.minor = int(version[1])
        self.patch = int(version[2])

    def __gt__(self, other):
        if self.major > other.major:
            return True
        elif self.major < other.major:
            return False
        if self.minor > other.minor:
            return True
        elif self.minor < other.minor:
            return False
        if self.patch > other.patch:
            return True
        elif self.patch < other.patch:
            return False
        if self.prerelease == "":
            return False
        if other.prerelease == "":
            return True
        if self.prerelease > other.prerelease:
            return True
        elif self.prerelease < other.prerelease:
            return False
        return False

    def __lt__(self, other):
        if self.major < other.major:
            return True
        elif self.major > other.major:
            return False
        if self.minor < other.minor:
            return True
        elif self.minor > other.minor:
            return False
        if self.patch < other.patch:
            return True
        elif self.patch > other.patch:
            return False
        if self.prerelease == "":
            return True
        if other.prerelease == "":
            return False
        if self.prerelease < other.prerelease:
            return True
        elif self.prerelease > other.prerelease:
            return False
        return False

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch and self.prerelease == other.prerelease

    def __str__(self):
        return self.version


if __name__ == "__main__":
    update = Update(".\\")
    update.get_url()
