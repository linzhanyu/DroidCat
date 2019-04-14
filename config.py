# -*- coding:utf-8 -*-
# from enum import enum
import platform, datetime

g_version = (0,0,0,1)

class Config :
    ADK     = r'/Users/linzhanyu/Downloads/sdk'    # * ADK 路径 如 D:/android/android-sdk
    Unity   = r'Z:\Program Files (x86)\Unity\Editor\Unity.exe'
    LogFile = 'Finance.log'        # 编译日志文件
    AppName = 'com.yanfa.bleach'

__all__ = ['Config', ]

