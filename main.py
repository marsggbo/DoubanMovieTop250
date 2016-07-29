#coding=utf-8
from handleData import *
from getData import getMovieData
import pymysql

def ChooseMethod():
	x = ''
	x = input("请选择要进行的操作:\n(1):以txt格式存储文件\n(2)以json格式存储文件\n(3)存入mysql数据库\n(4)取消操作\n>>>")
	while x not in ["1", "2", "3", "4"]:
		print("输入有误请重新输入！")
		x = input("请选择要进行的操作:\n(1):以txt格式存储文件\n(2)以json格式存储文件\n(3)存入mysql数据库\n(4)取消操作\n>>>")
	return x

def Continue():
	judge = ''
	judge = input("是否继续实行操作？(y)继续 (n)退出")
	while judge not in ["y", "Y", "n", "N"]:
		print("输入有误请重新输入！")
		judge = input("是否继续实行操作？(y)继续 (n)退出")
	return  judge

if __name__ == "__main__":
	try:
		movies = getMovieData()
		judge = "y"
		while(judge in ["y", "Y"]):
			choose = ChooseMethod()
			if choose=="1":
				SaveTxt(movies)
			elif choose=="2":
				SaveJson(movies)
			elif choose=="3":
				SaveMySQL(movies)
			elif choose=="4":
				print("******退出程序*******")
				break
			judge = Continue()
	except Exception as e:
		print("OMG,出错了，再仔细产看一下代码吧！！！")
		raise e
	# choose = ChooseMethod()