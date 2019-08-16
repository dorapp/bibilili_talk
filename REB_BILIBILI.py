#-*coding=utf-8-*
# __Author__: Liod
import requests,json,time,youku,datetime
u"""

简单对话版本的bilibili私信功能,初学python，新手第一个扔在github的项目

"""


class GIL_REBOT:

    def __init__(self):
        self.page = 0
        self.av = 11110
        self.url = {
            "av_url":"http://api.bilibili.com/archive_stat/stat?callback=jQuery17203247801634166214_1487830100756&aid=%s&type=jsonp&_=1487830101093",
            "comment_url":"http://api.bilibili.com/x/v2/reply?callback=jQuery17203247801634166214_1487830100769&jsonp=jsonp&pn=%s&type=1&oid=%s&sort=0&_=1487830102231",
            "personal_url":"http://space.bilibili.com/ajax/member/GetInfo",
            "follow_url":"http://space.bilibili.com/ajax/friend/AddAttention",
            "delete_follow_url":"http://space.bilibili.com/ajax/friend/DelAttention",
            "chat_url":{"captcha_url":"http://www.bilibili.com/plus/widget/ajaxGetCaptchaKey.php?js", "send_message_url":"http://message.bilibili.com/api/msg/send.msg.do", "rid_url":"http://message.bilibili.com/api/msg/query.double.room.do"}
        }
        self.message = {}
        self.result = {}
        self.cookie = ""

        u"""
        萌新没解决自动登录的问题只好暂时用cookie实现的访问各种api
        """



    def select_av(self, av):
        self.result["av_info"] = {}
        u""""
        获取番剧，视频的相关信息，后期处理返回数据的格式问题
        """
        try:
            info = json.loads(requests.get(self.url["av_url"]%av).content[41:-2])["data"]
            comment_info = json.loads(requests.get(self.url["comment_url"]%(1, av)).content[41:-1])["data"]
            self.result["av_info"]["view"] = info["view"]
            self.result["av_info"]["favorite"] = info["favorite"]
            self.result["av_info"]["coin"] = info["coin"]
            self.result["av_info"]["mid"] = comment_info["upper"]["mid"]
        except KeyError:
            return False
        self.result["av_info"]["comment"] = {"hot":{}, "news":{}}
        try:
            for i in range(3):
               try:
                   self.result["av_info"]["comment"]["hot"]["%s"%i] = [comment_info["hots"][i]["member"]["uname"], comment_info["hots"][i]["content"]["message"]]
               except KeyError:
                   self.result["av_info"]["comment"]["hot"] = u"视屏被和谐，萌萌酱也没办法了"
            for i in range(13):
                self.result["av_info"]["comment"]["news"]["%s"%i] = [comment_info["replies"][i]["member"]["uname"], comment_info["replies"][i]["content"]["message"]]
            return self.result
        except IndexError:
            self.result["av_info"]["comment"]["hot"] = u"视屏被和谐，萌萌酱也没办法了"
            self.result["av_info"]["comment"]["news"] = u"视屏被和谐，萌萌酱也没办法了"
            return self.result

    def select_Personal_info(self, mid):
        u"""

        :param mid: 查询用户信息
        :return:    返回值为一个列表
        """
        self.result["mid_info"] = {}
        headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                    "Referer":"http://space.bilibili.com/388434/"
       }
        data = {"mid":"%s"%mid, "_":"1487769159876"}
        personal_info = json.loads(requests.post(self.url["personal_url"], headers = headers, data = data).content)
        self.result["mid_info"]["name"] = personal_info["data"]["name"]
        self.result["mid_info"]["sex"] = personal_info["data"]["sex"]
        self.result["mid_info"]["level"] = personal_info["data"]["level_info"]["current_level"]
        self.result["mid_info"]["mid"] = personal_info["data"]["mid"]
        self.result["mid_info"]["birthday"] = personal_info["data"]["birthday"]
        self.result["mid_info"]["fans"] = personal_info["data"]["fans"]
        self.result["mid_info"]["nd5"] = personal_info["data"]["im9_sign"]
        return self.result["mid_info"]




    def add_mid(self, mid):
        u"""

        没有返回值，是个关注方法
        """
        headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Cookie":"%s"%self.cookie,
            "Referer":"http://space.bilibili.com/11095875/"
        }
        data = {"mid":"%s"%mid}
        follow_info = requests.post(self.url["follow_url"], headers = headers, data = data)
        print json.loads(follow_info.content)["status"]
        if json.loads(follow_info.content)["status"] == True:
            print u"关注成功!"
        else:
            print u"关注失败"



    def private_chat(self):
        u"""
        私聊方法需要先获得captcha的md5加密字符串，然后再获得好友的聊天的rid加密字符串，然后在发送私聊的包,
        时间戳的问题， 去除后面的就是正常的时间格式
        :return:
        返回的为[[message], [], [], []]
        """
        Header = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Cookie":"%s"%self.cookie
        }
        captcha_info = requests.get(self.url["chat_url"]["captcha_url"], headers = Header)
        captcha = captcha_info.content[22:-2]
        rid_url = "http://message.bilibili.com/api/msg/query.room.list.do?captcha=%s&page_no=1"%captcha
        rid_info = requests.get(rid_url, headers = Header)
        rid_info_result = json.loads(rid_info.content)["data"]
        for i in range(len(rid_info_result)):
            #print rid_info_result[i]
            self.message["%s"%i] = {}
            self.message["%s"%i]["room_name"] = (rid_info_result[i]["room_name"])
            self.message["%s"%i]["rid"] = (rid_info_result[i]["rid"])
            self.message["%s"%i]["last_time"] = (rid_info_result[i]["last_time"])
            print self.message["%s"%i]["last_time"]
            self.message["%s"%i]["last_msg"] = (rid_info_result[i]["last_msg"])
            self.message["%s"%i]["msg_count"] = (rid_info_result[i]["msg_count"])
        self.message["captcha"] = (captcha)
        #print self.message
        return self.message



    def get_mid_rid(self, key):
        u"""

        :argument:param key:    key可以为mid或者rid,用于下面的sendmessage消息
        :return:
         函数返回为一个列表，用于查询mid和rid
        """
        syin = ""
        if key.isdigit():
            syin = "mid"
        else:
            syin = "rid"
        Header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Cookie":"%s"%self.cookie
        }
        data = {
            "captcha":"%s"%self.message["captcha"],
            "%s"%syin:"%s"%key
        }
        rid_info = requests.post(self.url["chat_url"]["rid_url"], headers = Header, data = data)
        return [json.loads(rid_info.content)["data"]["rid"], json.loads(rid_info.content)["data"]["mid"]]





    def get_list_message(self):
        while True:
            the_message_list = self.private_chat()
            for i in range(len(the_message_list)-1):
                if the_message_list["%s"%i]["last_msg"] == "help":
                    self.send_message_private(u"你好， 谢谢你的对话, %s"%the_message_list["%s"%i]["last_msg"], the_message_list["%s"%i]["rid"])
                elif the_message_list["%s"%i]["last_msg"][:2] == "av":
                    av_result = self.select_av(the_message_list["%s"%i]["last_msg"][2:])
                    if av_result == False:
                        self.send_message_private(u"视频找不到了，喵喵酱也没办法了", the_message_list["%s"%i]["rid"])
                    else:
                        try :
                            print the_message_list["%s"%i]["last_msg"][2:]
                            hot_string = u"三条热门评论：    [br]ID：    %s   内容:    %s[br]"
                            hot_string1 = ""
                            for t in range(3):
                                hot_string1 += hot_string%(av_result["av_info"]["comment"]["hot"]["%s"%t][0], av_result["av_info"]["comment"]["hot"]["%s"%t][1])
                            comment = u"最新评论:    [br]ID:    %s   内容:    %s[br]"
                            comment1 = ""
                            for b in range(10):
                                comment1 += comment%(av_result["av_info"]["comment"]["news"]["%s"%b][0], av_result["av_info"]["comment"]["news"]["%s"%b][1])
                            Modile = u"此番剧的播放量:    %s[br]此番剧的收藏量：    %s[br]此番剧硬币投放量:    %s[br]投稿作者:    %s[br]"%(av_result["av_info"]["view"], av_result["av_info"]["favorite"], av_result["av_info"]["coin"], av_result["av_info"]["mid"])
                            Modile = Modile + comment1
                            self.send_message_private(Modile, the_message_list["%s"%i]["rid"])
                            self.send_message_private(hot_string1, the_message_list["%s"%i]["rid"])
                        except TypeError:
                            self.send_message_private(u"这个视频好像被和谐了呦，萌萌酱也没办法了！", the_message_list["%s"%i]["rid"])
                else:
                    print the_message_list["%s"%i]["last_time"]
                    print self.ms(the_message_list["%s"%i]["last_time"])
                    result = youku.xx.send_message(the_message_list["%s"%i]["last_msg"])
                    if self.ms(the_message_list["%s"%i]["last_time"]) <= 18:
                        print "asd"
                        print the_message_list["%s" % i]["room_name"], the_message_list["%s" % i]["last_msg"]
                        self.send_message_private("[br]".join(result), the_message_list["%s"%i]["rid"])





    def ms(self, value):
        str = value
        b = str[11:].split(":")
        a = str[:10].split("-")
        a.extend(b)
        b = map(lambda x: int(x), a)
        last_time = datetime.datetime(b[0], b[1], b[2], b[3], b[4], b[5])
        now_time = datetime.datetime.now()
        return (now_time - last_time).seconds


    def send_message_private(self, value, id):
        u"""

        :param value:   这是发送消息的内容
        :param mid:     这个可以是发送消息的内容或者rid
        :return:
        """
        info = self.private_chat()
        rid = self.get_mid_rid(id)
        Header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Cookie": "%s"%self.cookie
        }
        data = {
            "rid":"%s"%rid[0],
            "msg":"%s"%value,
            "captcha":"%s"%info["captcha"]
        }
        send_message_info = json.loads(requests.post(self.url["chat_url"]["send_message_url"], headers = Header, data = data).content)
        if send_message_info["code"] == 0:
            print u"发送成功！ 消息内容为:%s"%value
        else:
            print u"发送失败"
            print send_message_info["message"]



    def run(self):
        self.private_chat()




test = GIL_REBOT()
test.run()
