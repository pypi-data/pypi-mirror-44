import json
from pprint import pprint
class Diff():
    def __init__(self):
        self.order=1
    def leaf(self,result,tags):
        try:
            for i in tags[:-1]:
                result=result[i]
            return result[tags[-1]]
        except Exception as e:
            #print e
            return None
    def diff(self,a,b):
        if isinstance(a,dict) and isinstance(b,dict):
            c={}
            allkeys = set(a.keys())|set(b.keys())
            for key in allkeys:
                av=a.get(key)
                bv=b.get(key)
                if av!=bv:
                    result=self.diff(av,bv)
                    c[key]=result
        elif isinstance(a,list) and isinstance(b,list):
            if self.order==1:
                c=[]
                if len(b)>len(a):
                    a.extend(None for _ in range(len(b)-len(a)))
                elif len(a)>len(b):
                    b.extend(None for _ in range(len(a)-len(b)))
                else:
                    pass
                for i,j in zip(a,b):
                    if i!=j:
                        c.append(self.diff(i,j))
            else:
                try:
                    c={}
                    c["online"]=list(set(a)-set(b))
                    c["test"]=list(set(b)-set(a))
                except TypeError:
                    print("you can only diff by order when {} in the []")
        else:
            if a!=b:
                c={}
                c["online"]=a
                c["test"]=b
            else:
                c=None
        return c

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
            rootlist+=results
        elif results and isinstance(results,dict):
            rootlist+=results

    def diff_by_keys(self,a,b,tagsr,*tagsv):
        tagsv = map(lambda tagv:tagv if isinstance(tagv,tuple) else (tagv,) ,tagsv)
        if not isinstance(tagsr,tuple):
            tagsr=(tagsr,)
        tagsa=list(tagsr)
        tagsb=list(tagsr)
        rootlista=[]
        rootlistb=[]
        self.j_root(a,tagsa,rootlista)
        self.j_root(b,tagsb,rootlistb)
        mylist=self.ld(rootlista,rootlistb,tagsv)
        return mylist

    def ld(self,a,b,tagsv):
        if len(b)>len(a):
            a.extend(None for _ in range(len(b)-len(a)))
        elif len(a)>len(b):
            b.extend(None for _ in range(len(a)-len(b)))
        else:
            pass
        mylist=[]
        for resulta,resultb in zip(a,b):
            mdict={}
            for tagv in tagsv:
                print tagv
                resa=self.leaf(resulta,tagv)
                resb=self.leaf(resultb,tagv)
                if resa!=resb:
                    mydict={}
                    mydict={}
                    mydict["online"]=resa
                    mydict["test"]=resb
                    mdict[tagv[-1]]=mydict
            mylist.append(mdict)
        return mylist

online={"a":1,"A":[{"c":2,"d":3},{"c":6,"d":9}]}
test=  {"a":1,"A":[{"c":5,"d":4},{"c":8,"d":0}]}
DIFF=Diff()
c=DIFF.diff_by_keys(online,test,"A","c","d")
final_dict={}
final_dict["online_url"]=None
final_dict["test_url"]=None
final_dict["diff"]=c
final_list=[]
final_list.append(final_dict)
with open('data.json', 'w') as f:
    json.dump(final_list, f)
