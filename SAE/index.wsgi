#_*_ coding:utf-8 _*_
import sae
import os, sys
import web, urllib2
from crawl import bbs
from lxml import html

urls = (
    "/" ,"bbs_index",
    "/api/bbs/topic","bbs_topic",
    "/api/bbs/topic/detail/(.*)","bbs_topic_detail",
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join( app_root, 'templates' )
render = web.template.render( templates_root )

class bbs_index:
    def GET(self):
        f = open("./static/index.html")
        content = f.read()
        f.close
        return content

class bbs_topic:
    def GET(self):
        topic = bbs()
        topic_path = {
        'topicList':{
            'block':"//div[@id='main']//td[@class='list']//tr",
            'author':"./td[contains(@class, 'author')]/a/text()",
            'topic':"./td[contains(@class, 'title')]//a/text()",
            'topic_link':"./td[contains(@class, 'title')]//a/@href",
            'reply':"./td[contains(@class, 'reply')]/text()"
            }
        }
        topic_url = "http://www.e658.cn/bbs/"
        topicOBJ = html.fromstring( urllib2.urlopen(topic_url).read() )

        topic.loadData( topicOBJ, topic_path )
        content = topic.topicList()
        return content
class bbs_topic_detail:
    def GET(self, articleID):
        detail = bbs()
        detail_path = {
        'title':{
            'block':"//div[@class='readTop']",
            'hits':".//div[@class='readNum']//li[1]/em/text()",
            'reply':".//div[@class='readNum']//li[2]/em/text()",
            'topic':".//h1[@id='subject_tpc']/text()"
            } ,
        'floors':{
            'block':"//div[@class='read_t']",
            'author':".//div[@class='readName b']//a",
            'avatar':".//a[@class='userCard face_img']/img/@src",
            'reply_time':".//div[@class='tipTop s6']//span[2]/@title",
            'content':".//div[@class='tpc_content']/div[@class='f14 mb10']",
            'answer':".//div[starts-with(@id,'subject')]"
            } ,
        'base':"//base/@href"
        }
        detail_url = "http://www.e658.cn/bbs/read.php?tid="+articleID
        # 简直没有人性记住 转码 转码
        f = urllib2.urlopen(detail_url).read() 
        f = f.decode('gbk')
        detailOBJ = html.fromstring( f )

        detail.loadData( detailOBJ, detail_path )
        content = detail.floors()
        return content

app = web.application( urls, globals() ).wsgifunc()
application = sae.create_wsgi_app( app )
