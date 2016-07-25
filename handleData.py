#coding=utf-8
from getData import getMovieData
import json

def SaveJson(sort_movies):
	f = open('DoubanMovie.json', 'w', encoding='utf-8')
	for movie in sort_movies:
		jsObj = json.dumps(movie)
		f.writelines(jsObj)
	f.close()


def SaveTxt(sort_movies):
	i = 1
	with open('DoubanMovie.txt', 'w', encoding='utf-8') as f:
		for movie in sort_movies:
			name, info, star, quote = "", "", "", ""

			# star是list类型，所以需要加上下标
			star = movie["star"][0]

			# 电影名称有很多个，所以需要用“+”运算拼接起来
			# 但要注意必须在每次循环开始前初始化各个变量，否则就会使得之前的数据与后来的拼接在一起了
			# 不要问我怎么知道的。。。。血的教训啊！！！
			for x in movie["name"]:
				name += str(x)
			info = movie["info"]
			quote = movie["quote"]
			f.writelines('\n\n-----------------------------------------------------------\n' + str(i) + u'.  评分:' + star + '\n')
			f.writelines(name + '\n')
			f.writelines(info + '\n')
			f.writelines(quote)
			i += 1
