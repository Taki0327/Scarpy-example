import scrapy
import pymysql
class Redcow(scrapy.Spider):
    name = 'redcow'
    i=1
    start_urls = [
        'http://data.sports.sohu.com/nba/nba_team_info.php?teamid=4',
    ]
    sjk=pymysql.connect(host="localhost",user="root",passwd="nzzfl2",db="python",port=3306)
    c=sjk.cursor()
    def parse(self, response):
        for quote in response.css('div.tab tr')[1:]:
            name=quote.css('td.e13 p a::text').get()
            loca=quote.css('td.e14 span::text').get()
            height=quote.css('td.e14::text')[0].get()
            weight=quote.css('td.e14::text')[1].get()
            date=quote.css('td.e14::text')[2].get()
            school=""
            try:
                school=quote.css('td.e14::text')[3].get()
            except Exception as e:
                school=""
            sql="INSERT INTO redcow(name,loca,height,weight,date,school) VALUES('{}','{}','{}','{}','{}','{}')".format(name,loca,height,weight,date,school)
            try:
                self.c.execute(sql)
                self.sjk.commit()
            except Exception as e:
                self.sjk.rollback()
                print(e)
            yield {
                '姓名': name,
                '位置': loca,
                '身高': height,
                '体重': weight,
                '出生日期':date,
                '学校':school
            }
        self.sjk.close()