
# Introduce #

Easily monitor LOG output for specified apk apps with adb logcat

1. Filter out the useless LOG of other apps
1. Display in different colors according to LOG level
1. Cross-platform

移动应用开发辅助工具.通过 adb logcat 可以比较方便地监视指定 apk 应用的LOG输出

1. 过滤掉其它APP的无用的LOG
1. 根据LOG等级用不同的颜色显示
1. 跨平台


# 配置开发环境 #

* Python3
* python3 -m pip install termcolor
* 编辑 config.py 中的 Android SDK 路径 和 
* 编辑 config.py 中的 AppName ( Apk 包名 )

# 运行 #

python3 DroidCat.py

# 效果 #

![运行效果](https://raw.githubusercontent.com/linzhanyu/DroidCat/master/Image/perview.png)

