#coding:utf-8
def test1():
    url = "http://10.85.93.232/lib/libac2.php?ip=10.85.93.232&port=61777&socialtime=1&cuid=2511255003&from=1045595010&source=2936099636&version=45&sid=t_wap_android&dup=1&engine_type=0&wm=5091_0008&isbctruncate=1&key=%E7%8C%AB%E7%B3%BB%E5%A5%B3%E5%8F%8B%E7%8E%8B%E4%B8%BD%E5%9D%A4&count=20&z=all&pagesize=20&xsort=social&us=1&token=Authorization%3A+TAuth2+token%3D%22OXPWQTNWWTQTXNXONYUU%253DONYUS%253DOUPYOTXORQPUVNTQTXNXNXpyOLOWaBfS%22%2Cparam%3D%22uid%253D2511255003%22%2Csign%3D%222pzblUe3uYqmdd42%252Blq3AcM1g1I%253D%22&cip=223.73.172.138&t=3&nettype=wifi&nofilter=0&page="
    J=Jseq(url,multi=0)
    result = J.j_dict(1,10,("subposdata"),"ID","digit_attr","hit_score","simhash_dup")
    print len(result)
def test2():
    url1="http://topic.search.weibo.com/topic/aggregate.php?sid=finder&uid=123467&count=10&type=1&web_degrade=0&seqid=1111&page="
    J=Jseq(url1)
    result=J.j_dict(1,3,"statuses",("attribute","text"),("attribute","category"),"mid","uid")
    print len(result)
def test3():
    urlonline="http://unify.search.weibo.com/mi/finder.php?wm=3333_2001&i=4e51dd2&b=1&from=1085393010&c=iphone&networktype=wifi&v_p=61&skin=default&v_f=1&lang=zh_CN&sflag=1&ua=iPhone6%2C2__weibo__8.5.3__iphone__os10.3.3&ft=0&scenes=0&extparam=search_biz%3A0&lon=116.2692666074009&luicode=10000001&containerid=231619_3&featurecode=10000001&uicode=10000772&fid=231583&need_head_cards=1&lat=40.04029177746782&feed_mypage_card_remould_enable=1&lfid=100012771122141&moduleID=pagecard&client=inf&infoType=cardlistInfo&ip=10.235.21.33&cip=10.235.21.33&uid=20738805&page="
    J = Jseq(urlonline)
    J.multi = 1
    mydict = J.j_dict(1,30,"cards",("card_group",1,"itemid"),("card_group",1,"title"),("card_group",0,"title"),("card_group",0,"tag_img"),("card_group",1,"pics"))
    mylist = J.j_list(1,10,("card_group",0,"title"),"cards")
test1()
