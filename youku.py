#-*coding=utf-8-*
import requests,json

class xiao():

    def __init__(self):
        self.message_url = "http://i.youku.com/u/audience/fun/getNewMsg?su=940988749&ru=814677438"
        self.send_message_url = {"1":"http://i.youku.com/u/audience/fun/postMsg", "2":"http://i.youku.com/u/audience/fun/sendMsgToMSxiaoice"}

    def send_message(self, value):
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Cookie": "__ysuid=xxxxxxxxxxxxxxxxxx; juid=xxxxxxxxxx; cna=xxxxxxxxxxxxxx; __ali=1488202597171Irv; _uab_collina=148820260368280685257725; __aliCount=1; seid=01ba1i2guf2v6c; referhost=http%3A%2F%2Fwww.msxiaoice.com; P_ck_ctb=BBFDA37B1D308D6C5E4774D3502A18CD; P_ck_ctr=6899CF1FE923668497521B1B6988959B; ykss=f20bb5585e61c9c3fd11d77c; _zpdtk=630f413d1a2e4bdbbfcb5b07570c14758e3e8c93; seidtimeout=1488261886766; _umdata=2BA477700510A7DF170CC65269257173B292F8E6CFFA901D1644B336E8301B0294AA30B9E6E87E8DCD43AD3E795C914CEAB2DC753743B1666700146EE6239AC4; P_j_scl=hasCheckLogin; visit=68db89187db770e089498872ea93e0d8; u=%E4%BC%98%E9%85%B7%E7%94%A8%E6%88%B71467111326642447; __ayft=1488258679933; __aysid=1488202599816MZ6; __arpvid=1488260396616MXW8mG-1488260396636; __arycid=; __ayscnt=1; __arcms=; __aypstp=8; __ayspstp=22; rpvid=1488260396399icMLHG-1488260485803; szutsid=940988749; yktk=1%7C1488260558%7C15%7CaWQ6OTQwOTg4NzQ5LG5uOuS8mOmFt%2BeUqOaItzE0NjcxMTEzMjY2NDI0NDcsdmlwOmZhbHNlLHl0aWQ6OTQwOTg4NzQ5LHRpZDow%7Cd6c6f5617067aa4baa2f7f37150017c9%7C87665a5867b034745104ba3c208271b539941284%7C1",
            "Referer": "http://i.youku.com/u/chat/id/UMzI1ODcwOTc1Mg==/type/message",
            "Host": "i.youku.com",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest"
        }
        send_data1 = {
                    "su":"940988749",
                    "ru":"814677438",
                    "msg":"%s"%value
                }
        send_data2 = {
                    "sender_id": "940988749",
                    "mid": "252403378",
                    "content": "%s"%value,
                    "content_type":"text",
                    "msxiaoice_uid":"814677438"
                }
        requests.post(self.send_message_url["1"], headers = header, data = send_data1)
        requests.post(self.send_message_url["2"], headers = header, data = send_data2)
        info = requests.get(self.message_url, headers = header)
        result = []
        try:
            for i in range(len(json.loads(info.content))):
                res = json.loads(info.content)[i]["content"]
                result.append(res)
            return result
        except TypeError:
            return [u"没有结果"]

xx = xiao()
for i in xx.send_message(u"你好"):
    print i
