#coding=utf-8
from handleData import SaveTxt
from getData import getMovieData

if __name__ == "__main__":
	try:
		movies = getMovieData()
		SaveTxt(movies)
		print("Job Done!")
	except Exception as e:
		print("OMG,出错了，再仔细产看一下代码吧！！！")