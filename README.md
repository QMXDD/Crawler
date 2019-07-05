# Crawler
使用Python爬虫将我的所有CSDN博客的文章标题和访问量爬取下来并生成一个柱状图
首先使用requests库的request函数将页面下载下来
再用正则表达式将文章标题和阅读量筛选出来，并存入文件中
使用pyecharts库中的bar函数将文章标题和阅读量对应着显示出来
博客详解：
入门版：
https://blog.csdn.net/Q_M_X_D_D_/article/details/94594196
进阶版：
https://blog.csdn.net/Q_M_X_D_D_/article/details/94732292
