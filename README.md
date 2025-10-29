> [!IMPORTANT]
> ~~Only 荷塘雨课堂~~（v0.4.0已适配全部4种雨课堂）
>
> 2024/10/13 由于雨课堂不再随着ppt发送其预设答案([详见#3](https://github.com/travellerse/RainClassroomAssistant/issues/3))，自动答题失效
>
> 截止2025/10/29，其他功能暂时正常使用。本仓库停止维护 ~~可能会有重构~~

# RainClassroomAssistant
## 原库https://github.com/TrickyDeath/RainClassroomAssitant
由于上游没有配置许可证，所以本仓库copyright归原作者TrickyDeath所有，且仅供学习交流使用，请勿用于商业用途。

## 介绍
&emsp;&emsp;基于Python的雨课堂线上课划水小助手。

&emsp;&emsp;疫情期间，网课成为了当前重要的教学方式。这种方式在疫情期间为诸位都提供了极大的便利。但是，不免有些线上水课，这些水课老师不仅仅讲的内容枯燥无聊，照着PPT读，还要整出一系列的活来提升听课率，例如：课堂中途偷袭式发题、点名，将弹幕回答问题记录作为考察平时成绩的依据等。为了解决线上水课不能安心划水的问题，雨课堂小助手应运而生。
## 已实现功能
 - 自动签到
 - 自动答题（仅限于上课过程中发布的选择题、多选题、填空题）
 - 自动发弹幕（一定时间内收到一定数量的弹幕后，自动跟风发送相同内容的弹幕）
 - 点名、收到题目等情况下的语音提醒
 - 多线程支持（此脚本支持在有多个正在上课课程的情况下使用）
 - 简洁美观的UI
 - 课堂ppt下载
## 待做功能
- [ ] 自动预习
- [ ] 切换雨课堂配置
- [ ] 自动更新
## 使用方法
### 使用前准备
1. **使用前最好关闭所有代理程序，否则程序可能无法正常使用**
### 使用程序
v0.0.3版本，更新UI，此后版本双击打开即可使用！
### 环境配置
```shell
pip install -r requirements.txt
```
或
```shell
uv add -r requirements.txt
```

什么是uv？
参见 (https://github.com/astral-sh/uv)
### 启动程序
```shell
python RainClassroomAssistant.py
```
或
```shell
uv run RainClassroomAssistant.py
```
### 打包程序
1. 安装pyinstaller(已包含在requirements.txt中)
```shell
pip install pyinstaller
```
2. 使用配置文件打包
```shell
pyinstaller RainClassroomAssistant.spec
```
