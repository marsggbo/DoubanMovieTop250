#coding=utf-8
from getData import getMovieData
import json
import pymysql

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

			star = movie["star"][0]

			for x in movie["name"]:
				name += str(x)
			info = movie["info"]
			quote = movie["quote"]
			f.writelines('\n\n-----------------------------------------------------------\n' + str(i) + u'.  评分:' + star + '\n')
			f.writelines(name + '\n')
			f.writelines(info + '\n')
			f.writelines(quote)
			i += 1


def SaveMySQL(sort_movies):
	try:
		db = pymysql.connect(host="localhost",user="root",password="123456",db="doubanmovie",charset="utf8")

		cursor = db.cursor()

		# 为了避免以后更新数据时由于已经存在这个表而产生错误
		# 所以if not exists 语句是判断是否已经有这个表，若没有则创建新表，有则跳过这一语句
		cursor.execute("create table if not exists movie(name text, star text, quote text, info text)")		

		for movie in sort_movies:
			star = str(movie["star"][0]).replace(r"'",'')
			name = str(movie["name"]).replace('[','').replace(']','').replace(r"'",'')
			info = str(movie["info"].replace('[','').replace(']','')).replace(r"'",'')
			quote = str(movie["quote"][0]).replace(r"'",'')
			sql = "insert into movie(star,name,info,quote) values('%s', '%s', '%s', '%s');" % (star, name, info, quote)
			print(sql + "\n********************\n")
			try:
				cursor.execute(sql)
				db.commit()
				print("数据插入成功\n*************\n")
			except Exception as e:
				raise e
		db.close()		
	except Exception as e:
		raise e