# 豆瓣电影Top250基本信息抓取
## 代码概述和阅读建议
## Code abstraction and the suggestion of reading the code.

> 注意：运行环境python35
> 需要安装的库：requests，lxml，json（自带的），pymysql(python2需要使用mysqldb)

代码思路：

--------------- 16.7.27 ------------
----------------------------------
1. 获取源代码
这里我用了requests，so easy就获取网页源代码了~~~

2. 将源码转化为能被XPath匹配的格式
3. 利用xpath抓取到需要的信息
4. 对获取到的信息按评分排序 
5. 将信息保存至txt文件

所以阅读代码建议先阅读getData.py，然后在阅读handleData.py


-------------------------
-----------更新日志 16.7.29-------------
--------------------------

**折腾了将近两天才把mysql数据库功能给实现了。**

经过这两天的实践，发现了自己的很多知识点漏洞。尤其是数据编码类型。每次要想实现把数据存入txt或其他文本文件，都要花费好长时间，虽然大致实现思路很清晰，但是总是会遇到很多细枝末节的障碍，基础不牢啊。


说说从昨天到现在一直折腾pymysql的经历吧。（脑袋很混乱。估计下文会更紊乱。。。。）。不过如果你能坚持看完，绝对会有收获，没有的话你来找我（反正你也找不到）

-----------------------------

- **BUG 1**

首先是最简单的pymysql.connect()语句的实现就耗了我大半天的时间。
```python
db = pymysql.connect(host="localhost",user="root",password="123456",db="doubanmovie",charset="utf8")
```

就是这么简单的一行代码。。。简直蠢哭了
我一直以为 ==user== 和 ==password== 两项是随便填的。。随便。。填。。的。。。
所以我付出了惨痛代价，mysql软件安装了三四次，电脑重启无数次。。。最后才慢慢悟出了真理，原来他们是我在安装mysql的时候自己设置的。
另外我要提醒一下小伙伴们，如果你安装mysql只是为了学习的话，建议密码不要太复杂，否则你会后悔的，相信我，恩。

------------------------------

- **BUG 2**
第二个遇到的障碍就是数据库和数据表的创建。
```python
db = pymysql.connect(host="localhost",user="root",password="123456",db="doubanmovie",charset="utf8")
```
上面这行代码中申明了数据库是doubanmovie，能这么写的前提是你已经提前创建了这个名为doubanmovie的数据库，否则。。。崩。。报错，别问我是怎么知道的。

好了，数据库的创建问题已经解决，那么接下来就是数据表的创建了。代码很简单，我轻轻松松的就写出来了（傲娇脸）

```mysql
cursor.execute("create table movie(name text, star text, quote text, info text)")       
```
但就是这么简单的语句也有很多坑。这并不是说这个语句有错，而是它对后面程序的调试很麻烦。因为这个语句执行一次后，如果再执行显然就会报错。你问为什么？因为已经存在名为==movie==的数据表了啊。所以我为了测试数据，就得反反复复的把这个语句注释掉。

后来google，百度查了一下，得到了下面的解决办法，加上"**if not exists**"就可以啦。代码如下：
```mysql
cursor.execute("create table if not exists movie(name text, star text, quote text, info text)")     
```
具体为什么就不解释了，实在不明白就百度翻译一下，因为太显而易见了~~~


- **BUG 3**

第三个bug就是数据插入操作。
这是浪费时间最长的过程，中途差点想放弃了，不过幸好坚持住了~~
具体的原因牵扯到代码，源头很长就不解释了，不过有兴趣的可以看看代码。

值得一提的是在这个过程中学到了一个很棒的用法（在牛人看来肯定很一般，但是这个办法确实解决了我的问题）。

就是插入语句，我们都知道插入语句是
```mysql
insert into 表名(变量名 数据类型) values(......);
```
我要插入的内容存放在字典中，所以最开始的办法超级原始，但不知道为什么就是不行(明明逻辑是对的).废话不多说看栗子：

假如我的数据存放在==movies==列表（list）里，数据存放在字典（dict）里
```python
movies = [
    {
    "name":"肖申克的救赎",
    "star":"9.6",
    "info":"电影介绍",
    "quote":"电影名句"
    },
    {
    ....
    }
]
```
数据处理，执行插入操作
为行文方便，代码有所简略
```python
db = pymysql.connect(host="localhost",user="root",password="123456",db="doubanmovie",charset="utf8")

cursor = db.cursor()
for movie in sort_movies:
    star = movie["star"]
    name = movie["name"]
    info = movie["info"]
    quote = movie["quote"]
    sql = "insert into movie(star,name,info,quote) values('%s', '%s', '%s', '%s');" % (star, name, info, quote)
    try:
        cursor.execute(sql)
        db.commit()
        print("数据插入成功\n*************\n")
    except Exception as e:
        raise e
db.close()  
```

以前的原始方法是
```python
sql = "insert into movie(star,name,info,quote) values(" + r'"' + star + r'","' + name + r'","'+ info + r'","'+ quote + r'",")'   
```

经查stackoverflow，得到如下解决办法（上面代码中已呈现）
```python
sql = "insert into movie(star,name,info,quote) values('%s', '%s', '%s', '%s');" % (star, name, info, quote)
```
这个可以很好的生成mysql执行语句。
stackoverflow的回答中有的人建议把上面代码中的 ==%== 改为 ==,==,具体啥原因参见[stackoverflow Python MySQL Statement returning Error](http://stackoverflow.com/questions/257563/python-mysql-statement-returning-error)


还有得记得加上这行代码
```python
db.commit()
```

----------------------
----------------------
往后版本希望扩展的功能：

- 将数据项增加“年份”，即电影的上映年份
- 电影数据分析
    - 评分情况
    - 前100名中各国家所占比例
    - 各种电影类型所占比例
- 可视化数据


干巴爹！！！！！










-----------------------------
> 当然如果有什么可以完善的也欢迎大家提出修改意见，希望与大家一起学习，进步
> 
> 大家也可以在我的<u>[博客](http://blog.163.com/hexin_mars_blog/blog/static/248215040201662742953509/)</u>中给我留言哈，很高兴能和大家交流沟通