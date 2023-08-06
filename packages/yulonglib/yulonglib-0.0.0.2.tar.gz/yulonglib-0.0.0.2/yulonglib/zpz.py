#!/usr/local/python275/bin/python
#-*-coding:utf-8-*-
import requests
import random
import time
from libqa.api import Api
from yulonglib.jseq import Jseq

class Zpz():

    def __init__(self, **xargs):
        args = {k:v for k,v in xargs.items() if v}
        self.mid = args.get("mid",4326681785629171)
        self.times = int(args.get("times",10))
        self.query = args.get("query",u"鴊嘑墝鏈恆闳")
        self.uid = args.get("uid","2008783705")
        self.uids = ["5418385983","5605764618","5418388891","5418389288","5418766702","5418767325","5418390702","5210812449","5462732639","5462737368","5605765336","3455000512"]
        self.text_list=["泌","魃","魈","魁","鬾","魑","魅","魍","魉","惎","穊","陂","忮","诐","弑","翆","织","缢","澻","企","屣","胔","俐","襚","膇","跂","眙","裡","德","痢","嚱","奰","蒉","璲","瑟","司"]
        self.what={"repost":self.repost,"comment":self.comment,"attitudes":self.attitudes}
        self.how={"multi":self.multi,"follow":self.follow,"mingren":self.mingren}

    def newpost(self):
        API=Api(self.uid)
        random.shuffle(self.text_list)
        text="".join(self.text_list).decode("utf-8")+self.query
        data = {"status":text}
        result=API.post_data("2/statuses/update",data)
        mid = result.get("mid")
        self.mid = mid
        time.sleep(2)
        return mid

    def repost(self,uid):
        API=Api(uid)
        random.shuffle(self.text_list)
        repost_text="".join(self.text_list)
        repost_data={"id":self.mid,"status":repost_text,"visible":0}
        result=API.post_data("2/statuses/repost",repost_data)

    def comment(self,uid):
        API=Api(uid)
        random.shuffle(self.text_list)
        comment_text="".join(self.text_list)
        comment_data={"id":self.mid,"comment":comment_text}
        result=API.post_data("2/comments/create",comment_data)

    def attitudes(self,uid):
        API=Api(uid)
        attitudes_data={"id":self.mid}
        result=API.post_data("attitudes/create",attitudes_data)

    def multi(self,sth,uid=None):
        for u in self.uids[:self.times]:
            self.what[sth](u)
            time.sleep(7)

    def follow(self,sth,uid="2770909092"):
        self.what[sth](uid)

    def mingren(self,sth,uid="2424130295"):
        self.what[sth](uid)

    def flow(self):
        self.multi("repost")
        self.multi("comment")
        self.multi("attitudes")

    def how_what(self,h,w,*uid):
        self.how[h](w,*uid)

if __name__=="__main__":   
    ZPZ=Zpz(times="")
    print ZPZ.mid
    print ZPZ.times
    #ZPZ.how_what("follow","repost")
    #ZPZ.how_what("mingren","comment","2008783705")
    #ZPZ.how_what("multi","comment","2008783705")
