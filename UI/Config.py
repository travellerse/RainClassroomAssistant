# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Config.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import functools
import json

from PyQt5 import QtCore, QtGui, QtWidgets

from Scripts.Utils import get_config_path, resource_path


class Config_Ui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 600)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                             "font: 9pt \"微软雅黑\";")
        Dialog.setWindowIcon(QtGui.QIcon(
            resource_path("UI\\Image\\favicon.ico")))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(
            QtCore.QRect(0, -56, 393, 580))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents)
        self.verticalLayout_12.setObjectName("verticalLayout_12")

        self.sign_config = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.sign_config.setObjectName("sign_config")
        self.verticalLayout_sign_config = QtWidgets.QVBoxLayout(
            self.sign_config)
        self.verticalLayout_sign_config.setObjectName(
            "verticalLayout_sign_config")
        self.when_delay_on = QtWidgets.QWidget(self.sign_config)
        self.when_delay_on.setEnabled(True)
        self.when_delay_on.setObjectName("when_delay_on")
        self.verticalLayout_when_delay_on = QtWidgets.QVBoxLayout(
            self.when_delay_on)
        self.verticalLayout_when_delay_on.setObjectName(
            "verticalLayout_when_delay_on")
        self.label_9 = QtWidgets.QLabel(self.when_delay_on)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_when_delay_on.addWidget(self.label_9)

        self.delay_time_radio = QtWidgets.QRadioButton(self.when_delay_on)
        self.delay_time_radio.setChecked(False)
        self.delay_time_radio.setObjectName("delay_time_radio")
        self.verticalLayout_when_delay_on.addWidget(self.delay_time_radio)
        self.when_delay_time = QtWidgets.QWidget(self.when_delay_on)
        self.when_delay_time.setEnabled(True)
        self.when_delay_time.setObjectName("when_delay_time")
        self.verticalLayout_when_delay_time = QtWidgets.QVBoxLayout(
            self.when_delay_time)
        self.verticalLayout_when_delay_time.setContentsMargins(0, 0, 0, 3)
        self.verticalLayout_when_delay_time.setObjectName(
            "verticalLayout_when_delay_time")
        self.delay_time_input = QtWidgets.QSpinBox(self.when_delay_time)
        self.delay_time_input.setMaximum(32767)
        self.delay_time_input.setObjectName("delay_time_input")
        self.verticalLayout_when_delay_time.addWidget(self.delay_time_input)
        self.label_10 = QtWidgets.QLabel(self.when_delay_time)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_when_delay_time.addWidget(self.label_10)
        self.cutoff_time_input = QtWidgets.QSpinBox(self.when_delay_on)
        self.cutoff_time_input.setMaximum(32767)
        self.cutoff_time_input.setObjectName("cutoff_time_input")
        self.verticalLayout_when_delay_time.addWidget(self.cutoff_time_input)
        self.verticalLayout_when_delay_on.addWidget(self.when_delay_time)

        self.no_delay_radio = QtWidgets.QRadioButton(self.when_delay_on)
        self.no_delay_radio.setChecked(False)
        self.no_delay_radio.setObjectName("no_delay_radio")
        self.verticalLayout_when_delay_on.addWidget(self.no_delay_radio)

        self.verticalLayout_sign_config.addWidget(self.when_delay_on)
        self.verticalLayout_12.addWidget(self.sign_config)

        self.danmu_config = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.danmu_config.setObjectName("danmu_config")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.danmu_config)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.danmu_on = QtWidgets.QCheckBox(self.danmu_config)
        self.danmu_on.setObjectName("danmu_on")
        self.verticalLayout_2.addWidget(self.danmu_on)
        self.when_danmu_on = QtWidgets.QWidget(self.danmu_config)
        self.when_danmu_on.setEnabled(False)
        self.when_danmu_on.setObjectName("when_danmu_on")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.when_danmu_on)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.when_danmu_on)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.danmu_spinBox = QtWidgets.QSpinBox(self.when_danmu_on)
        self.danmu_spinBox.setMaximum(32767)
        self.danmu_spinBox.setProperty("value", 5)
        self.danmu_spinBox.setObjectName("danmu_spinBox")
        self.verticalLayout_3.addWidget(self.danmu_spinBox)
        self.verticalLayout_2.addWidget(self.when_danmu_on)
        self.verticalLayout_12.addWidget(self.danmu_config)
        self.audio_config = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.audio_config.setObjectName("audio_config")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.audio_config)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.audio_on = QtWidgets.QCheckBox(self.audio_config)
        self.audio_on.setObjectName("audio_on")
        self.verticalLayout_4.addWidget(self.audio_on)
        self.when_audio_on = QtWidgets.QWidget(self.audio_config)
        self.when_audio_on.setEnabled(False)
        self.when_audio_on.setObjectName("when_audio_on")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.when_audio_on)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.widget_4 = QtWidgets.QWidget(self.when_audio_on)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_11.setContentsMargins(9, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_11.addWidget(self.label_4)
        self.verticalLayout_10.addWidget(self.widget_4)
        self.widget_3 = QtWidgets.QWidget(self.when_audio_on)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.when_audio_on_1 = QtWidgets.QWidget(self.widget_3)
        self.when_audio_on_1.setObjectName("when_audio_on_1")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.when_audio_on_1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.self_danmu = QtWidgets.QCheckBox(self.when_audio_on_1)
        self.self_danmu.setObjectName("self_danmu")
        self.verticalLayout_7.addWidget(self.self_danmu)
        self.others_danmu = QtWidgets.QCheckBox(self.when_audio_on_1)
        self.others_danmu.setObjectName("others_danmu")
        self.verticalLayout_7.addWidget(self.others_danmu)
        self.receive_problem = QtWidgets.QCheckBox(self.when_audio_on_1)
        self.receive_problem.setObjectName("receive_problem")
        self.verticalLayout_7.addWidget(self.receive_problem)
        self.answer_result = QtWidgets.QCheckBox(self.when_audio_on_1)
        self.answer_result.setObjectName("answer_result")
        self.verticalLayout_7.addWidget(self.answer_result)
        self.horizontalLayout_4.addWidget(self.when_audio_on_1)
        self.when_audio_on_2 = QtWidgets.QWidget(self.widget_3)
        self.when_audio_on_2.setObjectName("when_audio_on_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.when_audio_on_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.self_called = QtWidgets.QCheckBox(self.when_audio_on_2)
        self.self_called.setObjectName("self_called")
        self.verticalLayout_6.addWidget(self.self_called)
        self.others_called = QtWidgets.QCheckBox(self.when_audio_on_2)
        self.others_called.setObjectName("others_called")
        self.verticalLayout_6.addWidget(self.others_called)
        self.course = QtWidgets.QCheckBox(self.when_audio_on_2)
        self.course.setObjectName("course")
        self.verticalLayout_6.addWidget(self.course)
        self.network = QtWidgets.QCheckBox(self.when_audio_on_2)
        self.network.setObjectName("network")
        self.verticalLayout_6.addWidget(self.network)
        self.horizontalLayout_4.addWidget(self.when_audio_on_2)
        self.verticalLayout_10.addWidget(self.widget_3)
        self.verticalLayout_4.addWidget(self.when_audio_on)
        self.verticalLayout_12.addWidget(self.audio_config)

        self.answer_config = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.answer_config.setObjectName("answer_config")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.answer_config)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.answer_on = QtWidgets.QCheckBox(self.answer_config)
        self.answer_on.setObjectName("answer_on")
        self.verticalLayout_5.addWidget(self.answer_on)
        self.when_answer_on = QtWidgets.QWidget(self.answer_config)
        self.when_answer_on.setEnabled(False)
        self.when_answer_on.setObjectName("when_answer_on")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.when_answer_on)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_3 = QtWidgets.QLabel(self.when_answer_on)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_8.addWidget(self.label_3)
        self.delay_time_radio_1 = QtWidgets.QRadioButton(self.when_answer_on)
        self.delay_time_radio_1.setChecked(True)
        self.delay_time_radio_1.setObjectName("delay_time_radio_1")
        self.verticalLayout_8.addWidget(self.delay_time_radio_1)
        self.delay_time_radio_2 = QtWidgets.QRadioButton(self.when_answer_on)
        self.delay_time_radio_2.setObjectName("delay_time_radio_2")
        self.verticalLayout_8.addWidget(self.delay_time_radio_2)
        self.delay_time_radio_3 = QtWidgets.QRadioButton(self.when_answer_on)
        self.delay_time_radio_3.setObjectName("delay_time_radio_3")
        self.verticalLayout_8.addWidget(self.delay_time_radio_3)
        self.delay_time_radio_4 = QtWidgets.QRadioButton(self.when_answer_on)
        self.delay_time_radio_4.setChecked(True)
        self.delay_time_radio_4.setObjectName("delay_time_radio_4")
        self.verticalLayout_8.addWidget(self.delay_time_radio_4)
        self.when_delay_time_4 = QtWidgets.QWidget(self.when_answer_on)
        self.when_delay_time_4.setEnabled(False)
        self.when_delay_time_4.setObjectName("when_delay_time_4")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.when_delay_time_4)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 3)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.delay_time_4_input = QtWidgets.QSpinBox(self.when_delay_time_4)
        self.delay_time_4_input.setObjectName("delay_time_4_input")
        self.verticalLayout_10.addWidget(self.delay_time_4_input)
        self.label_2 = QtWidgets.QLabel(self.when_answer_on)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_8.addWidget(self.when_delay_time_4)
        self.verticalLayout_8.addWidget(self.label_2)
        self.verticalLayout_5.addWidget(self.when_answer_on)
        self.verticalLayout_12.addWidget(self.answer_config)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.btn_wid = QtWidgets.QWidget(Dialog)
        self.btn_wid.setObjectName("btn_wid")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.btn_wid)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.save = QtWidgets.QPushButton(self.btn_wid)
        self.save.setMaximumSize(QtCore.QSize(16777215, 40))
        self.save.setObjectName("save")
        self.horizontalLayout.addWidget(self.save)
        self.cancel = QtWidgets.QPushButton(self.btn_wid)
        self.cancel.setMaximumSize(QtCore.QSize(16777215, 40))
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.verticalLayout.addWidget(self.btn_wid)

        # 动作绑定
        self.cancel.clicked.connect(Dialog.reject)
        self.delay_time_radio.clicked.connect(self.enable_delay_sign_custom)
        self.no_delay_radio.clicked.connect(self.enable_delay_sign_custom)
        self.danmu_on.stateChanged.connect(self.enable_danmu_config)
        self.audio_on.stateChanged.connect(self.enable_audio_config)
        self.answer_on.stateChanged.connect(self.enable_answer_config)
        self.delay_time_radio_1.clicked.connect(self.enable_delay_custom)
        self.delay_time_radio_2.clicked.connect(self.enable_delay_custom)
        self.delay_time_radio_3.clicked.connect(self.enable_delay_custom)
        self.delay_time_radio_4.clicked.connect(self.enable_delay_custom)
        self.save.clicked.connect(functools.partial(
            self.save_config, dialog=Dialog))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def enable_danmu_config(self):
        # 启用自动弹幕详细配置Widget
        if self.danmu_on.isChecked():
            self.when_danmu_on.setEnabled(True)
        else:
            self.when_danmu_on.setEnabled(False)

    def enable_audio_config(self):
        # 启用语言提醒详细配置Widget
        if self.audio_on.isChecked():
            self.when_audio_on.setEnabled(True)
        else:
            self.when_audio_on.setEnabled(False)

    def enable_answer_config(self):
        # 启用自动答题详细配置Widget
        if self.answer_on.isChecked():
            self.when_answer_on.setEnabled(True)
        else:
            self.when_answer_on.setEnabled(False)

    def enable_delay_sign_custom(self):
        # 启用自定义延迟详细配置Widget
        if not self.delay_time_radio.isChecked():
            self.when_delay_time.setEnabled(False)
        else:
            self.when_delay_time.setEnabled(True)

    def enable_delay_custom(self):
        # 启用自定义延迟详细配置Widget
        if not self.delay_time_radio_4.isChecked():
            self.when_delay_time_4.setEnabled(False)
        else:
            self.when_delay_time_4.setEnabled(True)

    def load_config(self, config):
        # 签到配置
        self.when_delay_on.setEnabled(True)
        if config["sign_config"]["delay_time"]["type"] == 1:
            self.delay_time_radio.setChecked(True)
            self.when_delay_time.setEnabled(True)
        elif config["sign_config"]["delay_time"]["type"] == 2:
            self.no_delay_radio.setChecked(True)
            self.when_delay_time.setEnabled(False)
        self.delay_time_input.setValue(
            config["sign_config"]["delay_time"]["custom"]["time"])
        self.cutoff_time_input.setValue(
            config["sign_config"]["delay_time"]["custom"]["cutoff"])
        # 弹幕配置
        self.danmu_on.setChecked(config["auto_danmu"])
        self.danmu_spinBox.setValue(config["danmu_config"]["danmu_limit"])
        # 语音配置
        self.audio_on.setChecked(config["audio_on"])
        self.self_danmu.setChecked(
            config["audio_config"]["audio_type"]["send_danmu"])
        self.others_danmu.setChecked(
            config["audio_config"]["audio_type"]["others_danmu"])
        self.receive_problem.setChecked(
            config["audio_config"]["audio_type"]["receive_problem"])
        self.answer_result.setChecked(
            config["audio_config"]["audio_type"]["answer_result"])
        self.self_called.setChecked(
            config["audio_config"]["audio_type"]["im_called"])
        self.others_called.setChecked(
            config["audio_config"]["audio_type"]["others_called"])
        self.course.setChecked(
            config["audio_config"]["audio_type"]["course_info"])
        self.network.setChecked(
            config["audio_config"]["audio_type"]["network_info"])
        # 答题配置
        self.answer_on.setChecked(config["auto_answer"])
        if config["answer_config"]["answer_delay"]["type"] == 1:
            self.delay_time_radio_1.setChecked(True)
        elif config["answer_config"]["answer_delay"]["type"] == 2:
            self.delay_time_radio_2.setChecked(True)
        elif config["answer_config"]["answer_delay"]["type"] == 3:
            self.delay_time_radio_3.setChecked(True)
        elif config["answer_config"]["answer_delay"]["type"] == 4:
            self.delay_time_radio_4.setChecked(True)
        self.delay_time_4_input.setValue(
            config["answer_config"]["answer_delay"]["custom"]["percent"])
        self.dialog_config = config

    def save_config(self, dialog):
        config = self.dialog_config
        # 签到配置
        if self.delay_time_radio.isChecked():
            config["sign_config"]["delay_time"]["type"] = 1
        elif self.no_delay_radio.isChecked():
            config["sign_config"]["delay_time"]["type"] = 2
        config["sign_config"]["delay_time"]["custom"]["time"] = self.delay_time_input.value()
        config["sign_config"]["delay_time"]["custom"]["cutoff"] = self.cutoff_time_input.value()
        # 弹幕配置
        config["auto_danmu"] = self.danmu_on.isChecked()
        config["danmu_config"]["danmu_limit"] = self.danmu_spinBox.value()
        # 语音配置
        config["audio_on"] = self.audio_on.isChecked()
        config["audio_config"]["audio_type"]["send_danmu"] = self.self_danmu.isChecked()
        config["audio_config"]["audio_type"]["others_danmu"] = self.others_danmu.isChecked()
        config["audio_config"]["audio_type"]["receive_problem"] = self.receive_problem.isChecked()
        config["audio_config"]["audio_type"]["answer_result"] = self.answer_result.isChecked()
        config["audio_config"]["audio_type"]["im_called"] = self.self_called.isChecked()
        config["audio_config"]["audio_type"]["others_called"] = self.others_called.isChecked()
        config["audio_config"]["audio_type"]["course_info"] = self.course.isChecked()
        config["audio_config"]["audio_type"]["network_info"] = self.network.isChecked()
        # 答题配置
        config["auto_answer"] = self.answer_on.isChecked()
        if self.delay_time_radio_1.isChecked():
            config["answer_config"]["answer_delay"]["type"] = 1
        elif self.delay_time_radio_2.isChecked():
            config["answer_config"]["answer_delay"]["type"] = 2
        elif self.delay_time_radio_3.isChecked():
            config["answer_config"]["answer_delay"]["type"] = 3
        elif self.delay_time_radio_4.isChecked():
            config["answer_config"]["answer_delay"]["type"] = 4
        config["answer_config"]["answer_delay"]["custom"]["percent"] = self.delay_time_4_input.value()
        # 保存
        config_path = get_config_path()
        with open(config_path, "w+") as f:
            json.dump(config, f)
        dialog.accept()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "配置"))
        self.sign_config.setTitle(_translate("Dialog", "签到配置"))
        self.label_9.setText(_translate("Dialog", "签到延迟时长"))
        self.delay_time_radio.setText(
            _translate("Dialog", "自定义（于10~n秒内随机决定时间签到）"))
        self.label_10.setText(
            _translate("Dialog", "  延迟生效时间点（课程开始前n秒内启用延迟）"))
        self.no_delay_radio.setText(
            _translate("Dialog", "不延时"))
        self.danmu_config.setTitle(_translate("Dialog", "弹幕配置"))
        self.danmu_on.setText(_translate("Dialog", "启用自动发送弹幕"))
        self.label.setText(_translate("Dialog", "自动弹幕阈值（每分钟内收到n条弹幕后自动发送相同弹幕）"))
        self.audio_config.setTitle(_translate("Dialog", "语音配置"))
        self.audio_on.setText(_translate("Dialog", "启用语音提醒"))
        self.label_4.setText(_translate("Dialog", "需要语音提醒的内容"))
        self.self_danmu.setText(_translate("Dialog", "自动发送弹幕情况提醒"))
        self.others_danmu.setText(_translate("Dialog", "他人弹幕发送语音提醒"))
        self.receive_problem.setText(_translate("Dialog", "收到题目提醒"))
        self.answer_result.setText(_translate("Dialog", "自动答题情况提醒"))
        self.self_called.setText(_translate("Dialog", "自己被点名提醒"))
        self.others_called.setText(_translate("Dialog", "他人被点名提醒"))
        self.course.setText(_translate("Dialog", "课程相关提醒"))
        self.network.setText(_translate("Dialog", "网络断开/重连提醒"))
        self.answer_config.setTitle(_translate("Dialog", "答题配置"))
        self.answer_on.setText(_translate("Dialog", "启用自动答题"))
        self.label_3.setText(_translate("Dialog", "答题延迟时长"))
        self.delay_time_radio_1.setText(
            _translate("Dialog", "中庸（于收到题目前50%秒内随机决定时间）"))
        self.delay_time_radio_2.setText(
            _translate("Dialog", "激进（于收到题目前30%秒内随机决定时间）"))
        self.delay_time_radio_3.setText(
            _translate("Dialog", "保守（于收到题目前20%~70%秒内随机决定时间）"))
        self.delay_time_radio_4.setText(
            _translate("Dialog", "自定义（于收到题目前n%秒内随机决定时间）"))
        self.label_2.setText(_translate(
            "Dialog", "注：如果您采用自定义延迟时长，当延迟时长大于题目所给时限时，将按照系统默认算法重新计算延迟时长。"))
        self.save.setText(_translate("Dialog", "保存"))
        self.cancel.setText(_translate("Dialog", "取消"))
