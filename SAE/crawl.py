#_*_coding:utf-8_*_
import re, json
from lxml import html
from lxml.html import builder as E

class bbs(object):

    def loadData(self, etreeOBJ, path, counter=0):
        self.page = etreeOBJ
        self.path = path
        self.floor_counter = counter

    def topicList(self):
        path = self.path.get('topicList', None)
        block = self.page.xpath( path['block'] )
        topic_list = []
        # 最后一条是 分页跳转列表,前两条是推广，论坛通知
        for i in block[2:-1]:
            dic = {}
            dic['author'] = i.xpath( path['author'] )[0]
            print dic['author']
            dic['topic'] = i.xpath( path['topic'] )[0]
            print dic['topic']
            dic['topic_link'] = re.search("\d+",i.xpath( path['topic_link'] )[0]).group()
            print dic['topic_link']
            dic['reply'] = i.xpath( path['reply'] )[0]
            print dic['reply'] + "\n"
            topic_list.append( dic )
        topic_list = json.dumps( topic_list )
        return topic_list

    def floors(self):
        f = self.floor_counter# floor counter
        floors = []
        base_url = self.page.xpath ( self.path.get('base', None) )[0]
        print "Base URL: ",base_url

        path = self.path.get('floors', None)
        block = self.page.xpath( path['block'] )
        for i in block:
            dic = {}
            dic['floor'] = f
            f += 1
            print "------------ F"+str(f)+" ------------"
            dic['author'] = i.xpath( path['author'] )[0].text
            print "Author:",dic['author']

            dic['author_link'] = i.xpath( path['author'] )[0].get('href')
            print "Author_link:",dic['author_link']

            avatar_img = i.xpath( path['avatar'] )[0]
            if re.search("none\.gif", avatar_img):
                dic['avatar'] = "static/none.jpg"
            else:
                dic['avatar'] = base_url + avatar_img
            print "Avatar:",dic['avatar']

            dic['reply_time'] = i.xpath( path['reply_time'] )[0]
            print "Reply_time:",dic['reply_time']

            content_list = i.xpath( path['content'] )[0]
            div = E.DIV()
            if len(content_list) == 0:
                text = content_list.text
                div.append( E.P( text ) )
                dic["content"] = html.tostring( div,encoding='utf-8' )
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
                        CLASS = 'normal'
                        try:
                            src = tag.xpath(".//img/@src")[0]
                        except IndexError:
                            src = tag.xpath("./@src")[0]
                        try:
                            alt = tag.xpath(".//span[@class='mr10']")[0].text
                        except IndexError:
                            if( src.find('default') <= 0 ):
                                alt = "image..."
                            else:
                                alt = "emoji"
                                CLASS="emoji"
                        if ( src.find('http://') < 0 ):
                            src = base_url + src
                        div.append( E.IMG( src=src, alt=alt , CLASS=CLASS ) )
                    elif tag.tag == "blockquote":
                        continue
                else:
                    text = tag.text_content().strip()
                    print text
                    print type(text)
                    if text and text.strip() != "" and text != "\n":
                        div.append( E.P( text ) )
            # 结束处理加入字典
            dic["content"] = html.tostring( div,encoding='utf-8' )
            print "Content:",dic['content']
            # 排开楼主楼层处理 answer
            if f > 1:
                text = i.xpath( path['answer'] )[0].text_content()
                if text:
                    text = re.search("(?<= ).+(?= )", text).group()
                    text_re = re.search("(?<=\().+(?=\))", text)
                    if text_re:
                        dic["answer"] = text_re.group()
                    else:
                        dic["answer"] = text
                else:
                    dic["answer"] = None
                print "Answer:",dic['answer']
            floors.append( dic )
        if not self.floor_counter:
            path = self.path.get('title', None)
            block = self.page.xpath( path['block'] )[0]
            dic = {}
            dic['hits'] = block.xpath( path['hits'] )[0]
            print "阅读:",dic['hits']
            dic['reply'] = block.xpath( path['reply'] )[0]
            print "回复:",dic['reply']
            dic['topic'] = block.xpath( path['topic'] )[0]
            print "主题:",dic['topic']
            floors[0].update( dic )

        floors = json.dumps( floors )
        return floors
