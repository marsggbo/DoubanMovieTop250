# 豆瓣电影Top250基本信息抓取
## 代码概述和阅读建议
## Code abstraction and the suggestion of reading the code.

1. ### 获取源代码
这里我用了requests，so easy就获取网页源代码了~~~

2. ###将源码转化为能被XPath匹配的格式
3. 利用xpath抓取到需要的信息
4. 对获取到的信息按评分排序 
5. 将信息保存至txt文件

所以阅读代码建议先阅读getData.py，然后在阅读handleData.py

> 当然如果有什么可以完善的也欢迎大家提出修改意见，希望与大家一起学习，进步