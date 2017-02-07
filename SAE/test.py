#_*_coding:utf-8_*_
import urllib2
import re
from lxml import html
from lxml.html import builder as E

    #online test
url = "http://www.e658.cn/bbs/read.php?tid=48641&page=2"
openURL = urllib2.urlopen(url)
    #local test
#url = "2.html"
#openURL = open(url)

container = ""
container = openURL.read()
root = html.fromstring( container )
s = urllib2.urlopen("http://www.e658.cn/bbs").read()
topic = html.fromstring( s )
bbs_path = {
'title':{
    'block':"//div[@class='readTop']",
    'hits':".//div[@class='readNum']//li[1]/em",
    'reply':".//div[@class='readNum']//li[2]/em",
    'topic':".//h1[@id='subject_tpc']"
    } ,
'floors':{
    'block':"//div[@class='read_t']",
    'author':".//div[@class='readName b']//a",
    'avatar':".//a[@class='userCard face_img']/img/@src",
    'reply_time':".//div[@class='tipTop s6']//span[2]/@title",
    'content':".//div[@class='tpc_content']/div[@class='f14 mb10']",
    'answer':".//div[starts-with(@id,'subject')]"
    }
}
topic_path = {
'topicList':{
    'block':"//div[@id='main']//td[@class='list']//tr",
    'author':"./td[contains(@class, 'author')]/a/text()",
    'topic':"./td[contains(@class, 'title')]//a/text()",
    'topic_link':"./td[contains(@class, 'title')]//a/@href",
    'reply':"./td[contains(@class, 'reply')]/text()",
    }
}

class bbs(object):

    def loadData(self, etreeOBJ, path, counter=0):
        self.page = etreeOBJ
        self.path = path
        self.floor_counter = counter

    def topicList(self):
        path = self.path.get('topicList', None)
        block = self.page.xpath( path['block'] )
        topic_list = []
        # 最后一条是 分页跳转列表
        for i in block[2:-1]:
            dic = {}
            dic['author'] = i.xpath( path['author'] )[0]
            print dic['author']
            dic['topic'] = i.xpath( path['topic'] )[0]
            print dic['topic']
            dic['topic_link'] = i.xpath( path['topic_link'] )[0]
            print dic['topic_link']
            dic['reply'] = i.xpath( path['reply'] )[0]
            print dic['reply'] + "\n"
            topic_list.append( dic )
        return topic_list

    def floors(self):
        f = self.floor_counter# floor counter
        floors = []
        if not f:
            path = self.path.get('title', None)
            block = self.page.xpath( path['block'] )[0]
            dic = {}
            dic['hits'] = block.xpath( path['hits'] )[0].text
            print "阅读:",dic['hits']
            dic['reply'] = block.xpath( path['reply'] )[0].text
            print "回复:",dic['reply']
            dic['topic'] = block.xpath( path['topic'] )[0].text
            print "主题:",dic['topic']
            floors.append( dic )

        path = self.path.get('floors', None)
        block = self.page.xpath( path['block'] )
        for i in block:
            f += 1
            floorName = 'f'+str(f)
            print "------------"+floorName+"------------"
            dic = {}
            dic[floorName]={}
            dic[floorName]['author'] = i.xpath( path['author'] )[0].text
            print "Author:",dic[floorName]['author']
            dic[floorName]['avatar'] = i.xpath( path['avatar'] )[0]
            print "Avatar:",dic[floorName]['avatar']
            dic[floorName]['reply_time'] = i.xpath( path['reply_time'] )[0]
            print "Time:",dic[floorName]['reply_time']
            content_list = i.xpath( path['content'] )[0]
            div = E.DIV()
            if len(content_list) == 0:
                text = content_list.text
                div.append( E.P( text ) )
                dic[floorName]["content"] = html.tostring( div,encoding='utf-8' )
            else:
                # 首先处理内部文本
                # 标签后文本
                text = content_list.text
                if text.strip() != "" and text != "\n":
                    div.append( E.P( text ) )
                for tag in content_list:
                    # 针对被 br 隔断的文本
                    text = tag.tail
                    if text and text.strip() != "" and text != "\n":
                        div.append( E.P( text ) )
                    # 纯图片与夹带图片处理
                    if tag.tag == "span" and tag.get('class') == "f12" or tag.tag == "img":
                        try:
                            src = tag.xpath(".//img/@src")[0]
                        except IndexError:
                            src = tag.xpath("./@src")[0]
                        try:
                            alt = tag.xpath(".//span[@class='mr10']")[0].text
                        except IndexError:
                            if len(src) > 18:
                                alt = "image..."
                            else:
                                alt = "emoji"
                        div.append( E.IMG( src=src, alt=alt ) )
                    elif tag.tag == "blockquote":
                        continue
                    else:
                        text = tag.text_content()
                        if text and text.strip() != "" and text != "\n":
                            div.append( E.P( text ) )
            # 结束处理加入字典
            dic[floorName]["content"] = html.tostring( div,encoding='utf-8' )
            print "Content:",dic[floorName]['content']
            # 排开楼主楼层处理 answer
            if f > 1:
                text = i.xpath( path['answer'] )[0].text_content()
                if text:
                    text = re.search("(?<= ).+(?= )", text).group()
                    text_re = re.search("(?<=\().+(?=\))", text)
                    if text_re:
                        dic[floorName]["answer"] = text_re.group()
                    else:
                        dic[floorName]["answer"] = text
                else:
                    dic[floorName]["answer"] = None
                print "Answer:",dic[floorName]['answer']
            floors.append( dic )
        return floors

a = bbs()
a.loadData( root, bbs_path )
a.floors()

b = bbs()
b.loadData( topic,topic_path )
b.topicList( )
