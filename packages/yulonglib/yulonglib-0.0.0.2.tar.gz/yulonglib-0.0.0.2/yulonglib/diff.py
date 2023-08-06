#-*-coding:utf-8-*-
import requests
import copy
import threading
import time
from yulonglib.jseq import Jseq

class Diff():

    def __init__(self,url):

        self.url=url
        self.cookies  = ""
        self.s = requests.session()
        self.multi = 0


    def j_root(self,results,tags,rootlist):
        if len(tags)>0 and tags[0]:
            if isinstance(results,dict):
                result=results.get(tags.pop(0))
                self.j_root(result,tags,rootlist)
            elif isinstance(results,list):
                if results and isinstance(results[0],dict):
                    tag=tags.pop(0)
                    for result in results:
                        if isinstance(result,dict):
                            r=result.get(tag)
                            self.j_root(r,tags,rootlist)
                elif results and isinstance(results[0],list):
                    for result in results:
                        self.j_root(r,tags,rootlist)
        elif results and isinstance(results,list):
            rootlist.update(results)
        elif results and isinstance(results,dict):
            rootlist.append(results)

    def diff_d(self,d,tagsk,tagsv):

        for result in rootlist:
            k=self.leaf(result,tagsk)
            mydict[k]={}
            for tagv in tagsv:
                mydict[k]["|".join(map(str,tagv))]=self.leaf(result,tagv)
        return mydict

    def work(self,url,tagsr,rootlist):
        resp=self.s.get(url,cookies=self.cookies)
        if not resp:
            print "no"
            return
        try:
            jsondata = resp.json()
        except:
            print("warning",resp)
            return
        mytagsr=copy.deepcopy(tagsr)
        self.j_root(jsondata,mytagsr,rootlist)

    def j_dict(self,paras,tagsr,tagsk,*tagsv):

        tagsv = map(lambda tagv:tagv if isinstance(tagv,tuple) else (tagv,) ,tagsv)
        if not isinstance(tagsr,tuple):
            tagsr=(tagsr,)
        tagsr=list(tagsr)
        if not isinstance(tagsk,tuple):
            tagsk=(tagsk,)

        rootlist=Generator()
        if isinstance(paras,int):
            url=self.url
            for i in xrange(paras):
                self.work(url,tagsr,rootlist)
        elif self.multi:
            threads=[]
            for i in paras:
                print i
                url=self.url % i
                t = threading.Thread(target=self.work,args=(url,tagsr,rootlist))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        else:
            for i in paras:
                url=self.url % i
                self.work(url,tagsr,rootlist)
        mydict=self.l_dict(rootlist,tagsk,tagsv)
        return mydict
 
    def l_ld(self,rootlist,tagsv):
        myld=[]
        for result in rootlist:
            myk={}
            for tagv in tagsv:
                myk["|".join(map(str,tagv))]=self.leaf(result,tagv)
            myld.append(myk)
        return myld


    def j_ld(self,paras,tagsr,*tagsv):

        tagsv = map(lambda tagv:tagv if isinstance(tagv,tuple) else (tagv,) ,tagsv)
        if not isinstance(tagsr,tuple):
            tagsr=(tagsr,)
        tagsr=list(tagsr)

        rootlist=Generator()
        if isinstance(paras,int):
            url=self.url
            for i in xrange(paras):
                self.work(url,tagsr,rootlist)
        elif self.multi:
            threads=[]
            for i in paras:
                url=self.url % i
                t = threading.Thread(target=self.work,args=(url,tagsr,rootlist))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        else:
            for i in paras:
                url=self.url % i
                self.work(url,tagsr,rootlist)
        myld=self.l_ld(rootlist,tagsv)
        return myld

    def l_filter(self,rootlist,func,*tagsks): 

        tagsks = map(lambda tagsk:tagsk if isinstance(tagsk,tuple) else (tagsk,) ,tagsks)
        mylist=[ i for i in rootlist if func(*[self.leaf(i,tagsk) for tagsk in tagsks]) ]
        return mylist

    def j_filter(self,paras,func,tagsr,*tagsk):

        if not isinstance(tagsr,tuple):
            tagsr=(tagsr,)
        tagsr=list(tagsr)
        tagsk = map(lambda tagk:tagk if isinstance(tagk,tuple) else (tagk,) ,tagsk)

        rootlist=Generator()
        if isinstance(paras,int):
            url=self.url
            for i in xrange(paras):
                self.work(url,tagsr,rootlist)
        else:
            for i in paras:
                url=self.url % i
                self.work(url,tagsr,rootlist)
        mylist=self.l_filter(rootlist,func,*tagsk)
        return mylist
 
    def l_list(self,rootlist,*tagsk): 
        if isinstance(tagsk[0],tuple):
            tagsk=tagsk[0]
        mylist=[ self.leaf(i,tagsk) for i in rootlist if isinstance(i,dict) ]
        return mylist

    def j_list(self,paras,tagsk,*tagsr):

        if not isinstance(tagsk,tuple):
            tagsk=(tagsk,)
        tagsr = map(lambda tagr:list(tagr) if isinstance(tagr,tuple) else [tagr,] ,tagsr)

        rootlist=Generator()
        if isinstance(paras,int):
            url=self.url
            for i in xrange(paras):
                resp=self.s.get(url,cookies=self.cookies)
                if not resp:
                    continue
                jsondata = resp.json()
                for tagr in tagsr:
                    self.j_root(jsondata,tagr,rootlist)
        else:
            for i in paras:
                url=self.url % i
                resp=self.s.get(url,cookies=self.cookies)
                if not resp:
                    continue
                jsondata = resp.json()
                mytagsr=copy.deepcopy(tagsr)
                for tagr in mytagsr:
                    self.j_root(jsondata,tagr,rootlist)
        mylist=self.l_list(rootlist,*tagsk)

        return mylist


    def l_del(self,rootlist,*tagsk):

        tagsk = map(lambda tagk:tagk if isinstance(tagk,tuple) else (tagk,) ,tagsk)
        mylist=[]
        for jsondata in rootlist: 
            for tagk in tagsk:
                jsondata=self.del_json(jsondata,tagk)
            mylist.append(jsondata)
        return mylist

    def j_del(self,paras,*tagsk):

        tagsk = map(lambda tagk:tagk if isinstance(tagk,tuple) else (tagk,) ,tagsk)
        mylist=[]
        if isinstance(paras,int):
            url=self.url
            for i in xrange(paras):
                resp=self.s.get(url,cookies=self.cookies)
                if not resp:
                    continue
                jsondata = resp.json()
                for tagk in tagsk:
                    jsondata=self.del_json(jsondata,tagk)
                mylist.append(jsondata)
        else:
            for i in paras:
                url=self.url % i
                resp=self.s.get(url,cookies=self.cookies)
                if not resp:
                    continue
                jsondata = resp.json()
                for tagk in tagsk:
                    jsondata=self.del_json(jsondata,tagk)
                mylist.append(jsondata)
        return mylist

    def findall_del(self,seq,*tagsk):
        if isinstance(seq,list):
            for i in seq:
                self.findall_del(i,*tagsk)
        elif isinstance(seq,dict):
            for k,v in seq.items():
                if k in tagsk:
                    del seq[k]
                else:
                    self.findall_del(v,*tagsk)

    def j_findall_del(self,paras,*tagsk):
        mylist=[]
        if isinstance(paras,int):
            url=self.url
            for i in xrange(paras):
                resp=self.s.get(url,cookies=self.cookies)
                if not resp:
                    continue
                jsondata = resp.json()
                self.findall_del(jsondata,*tagsk)
                mylist.append(jsondata)
        else:
            for i in paras:
                url=self.url % i
                resp=self.s.get(url,cookies=self.cookies)
                if not resp:
                    continue
                jsondata = resp.json()
                self.findall_del(jsondata,*tagsk)
                mylist.append(jsondata)
        return mylist

    def findall(self,seq,*tagsk):
        if isinstance(seq,list):
            for i in seq:
                for j in  self.findall(i,*tagsk):
                    yield j
        elif isinstance(seq,dict):
            for k,v in seq.items():
                if k in tagsk:
                    yield v
                else:
                    for j in self.findall(v,*tagsk):
                        yield j
    
    def j_findall(self,paras,*tagsk):
        mylist=[]
        if isinstance(paras,int):
            url=self.url
            for i in xrange(paras):
                resp=self.s.get(url,cookies=self.cookies)
                if not resp:
                    continue
                jsondata = resp.json()
                result=self.findall(jsondata,*tagsk)
                mylist+=list(result)
        else:
            for i in paras:
                url=self.url % i
                resp=self.s.get(url,cookies=self.cookies)
                if not resp:
                    continue
                jsondata = resp.json()
                result=self.findall(jsondata,*tagsk)
                mylist+=list(result)
        return mylist
        

if __name__ == "__main__":
    url="http://10.77.104.182/topic/aggregate.php?sid=finder&uid=111111111111111&count=10&type=0&web_degrade=4&seqid=1111&page="
    J=Jseq(url)
    res=J.j_leaf(xrange(1,10),"statuses",0,"dup")
    for i in res:
        print i
