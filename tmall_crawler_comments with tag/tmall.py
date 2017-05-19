import requests
import json
import re
import csv


tagcloudurl = 'https://rate.tmall.com/listTagClouds.htm?callback=jsonp_review_tags&itemId='
commenturl = 'https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId={}&order=3&append=0&content=0&currentPage=1&pageSize=10&tagId=&callback=jsonp457'
class tmall_comment(object):

    def __init__(self,id,seller_id,tagid='',pagenum=2):
        self.tagcloudurl = 'https://rate.tmall.com/listTagClouds.htm?callback=jsonp_review_tags&itemId='
        self.commenturl = 'https://rate.tmall.com/list_detail_rate.htm?order=3&append=0&content=0&pageSize=10&callback=jsonp457'
        self.id = str(id)
        self.seller_id = str(seller_id)
        self.tagid = str(tagid)
        self.all_name = self.id+'_'+self.seller_id
        self.tag_name = self.id+'_'+self.seller_id+'_tag'
        self.pagenum =pagenum

    def get_tag(self):
        r = requests.get(tagcloudurl+self.id)
        info = r.text.split('(')[1].split(')')[0]
        json_info =json.loads(info)
        all =[]
        for i in json_info['tags']['tagClouds']:
            data =[]
            data.append(i['id'])
            data.append(i['tag'])
            all.append(data)
        self.write_csv('tag',all)


    def crawl_comment(self,i):
        header ={'method':'GET',
                  'scheme':'https',
                  'accept':'*/*',
                  'user-agent':'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
                  'cookie': ''}

        params = {
                'currentPage':str(i),
                  'itemId': self.id,
                  'sellerId': self.seller_id,
                  'tagId':''}
        r = requests.get(self.commenturl,headers =header,params=params)
        info = r.text.split('(')[1].split(')')[0]
        json_info = json.loads(info)

        commentlist = json_info['rateDetail']['rateList']
        data = []
        for i in commentlist:
            slist = []
            slist.append(i['id'])
            slist.append(i['position'])
            slist.append(i['rateContent'])
            slist.append(i['rateDate'])
            slist.append(i['tamllSweetLevel'])
            data.append(slist)
        return data


    def get_allcomment(self):
        self.create(self.all_name,['id','position','rateContent','rateDate','tamllSweetLevel'])
        for i in range(1,self.pagenum+1):
            self.write_csv(self.all_name,self.crawl_comment(i))


    def cra_tag_comment(self,i):
        header = {'method': 'GET',
                  'scheme': 'https',
                  'accept': '*/*',
                  'user-agent': 'Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9',
                  'cookie': ''}

        params = {
            'currentPage': str(i),
            'itemId': self.id,
            'sellerId': self.seller_id,
            'tagId': self.tagid}
        r = requests.get(self.commenturl, headers=header, params=params)
        info = r.text.split('(')[1].split(')')[0]
        json_info = json.loads(info)
        pagenum = json_info['rateDetail']['paginator']['lastPage']

        commentlist = json_info['rateDetail']['rateList']
        data = []
        for i in commentlist:
            slist = []
            slist.append(i['id'])
            slist.append(i['position'])
            slist.append(i['rateContent'])
            slist.append(i['rateDate'])
            slist.append(i['tamllSweetLevel'])
            data.append(slist)
        return data,pagenum

    def get_tagcomment(self):
        self.create(self.tag_name, ['id', 'position', 'rateContent', 'rateDate', 'tamllSweetLevel'])


        data,page_num =self.cra_tag_comment(1)
        for i in range(1,page_num+1):
            try:
                datalist,page_num = self.cra_tag_comment(i)
                self.write_csv(self.tag_name,datalist)
            except:
                pass




    def create(self,name,title):

        with open(name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(title)



    def write_csv(self,name,list):
        with open(name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(list)






#41124112598
#725677994


#改变底下输入的参数即可
#这一部分为爬tag标签 和 全部评论 例如 tmall_comment(41124112598,725677994,tagid='520',pagenum = 2) 第一项为商品id第二项为sellerid第三项为总页数
c = tmall_comment(41124112598,725677994,pagenum = 2)
c.get_tag()
c.get_allcomment()
with open('tag','r') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]
    for i in rows:
        print(i)
        #爬取带tag的评论 这里只用改变 第一项为商品id第二项为sellerid第三项不管
        a = tmall_comment(41124112598,725677994,tagid=i[0])
        a.get_tagcomment()

