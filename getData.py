#coding=utf-8
import requests
from lxml import etree

def getMovieData():
	movies = []
	url = r'https://movie.douban.com/top250'
	parameter = r'?start=0&filter='

	try:
		while str(parameter[0]):
			# 生成链接
			urls = url + str(parameter[0])

			r = requests.get(urls)

			#获取网站源代码
			sourceCode = r.text

			# 将源码转化为能被XPath匹配的格式
			html = etree.HTML(sourceCode)

			# 获取网站链接的参数，即下一页地址
			# parameter = html.xpath('/*/span[@class="next"]/a/@href')
			parameter = html.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href')

			items = html.xpath('//ol/li/div[@class="item"]')
			for item in items:
				movie = {
					"name": '',
					"info": '',
					"star": '',
					"quote": ''
				}
				name, info, star, quote = "", "", "", ""
				try:
					name = item.xpath('./div[@class="info"]/div[@class="hd"]/a//span/text()')
					infos = item.xpath('./div[@class="info"]/div[@class="bd"]/p[@class=""]//text()')
					star = item.xpath('./div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')
					quote = item.xpath('./div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()')

					info = (infos[0] + infos[1]).replace(" ", '').replace('\n', '').replace('\xa0', ' ')

					movie["name"] = name
					movie["info"] = info
					movie["star"] = star
					if quote:
						movie["quote"] = quote
					else:
						movie["quote"] = ""
					movies.append(movie)
				except Exception as e:
					raise e
	except Exception as e:
		print('加载完毕')

	# 按评分排序
	movies = sorted(movies, key=lambda x: x['star'], reverse=True)

	return movies


