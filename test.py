import re
import requests
import threading
from pyecharts.charts import Bar

class spider:
    list = []
    link_set = set()
    pos=0
    def __init__(self,name,num):
        self.name=name
        self.num=num

    def get_links2(self,html):
        # 将正则表达式编译之后可以使用findall函数 #
        web_regex=re.compile(r"<span class=\"num\">[0-9]*</span>")
        return web_regex.findall(html)

    def get_num2(self,list):
        num_regex=re.compile(r"[0-9]+")
        s=""
        for i in list:
            s+=str(i)
        return num_regex.findall(s)

    def get_links(self,html):
        # 将正则表达式编译之后可以使用findall函数 #
        web_regex=re.compile(r"<a +href=[\'\"](.*?)[\'\"]")
        return web_regex.findall(html)

    def link_cwrael(self,start_url):
        html=requests.get(start_url).text
        link_regex = "https://blog.csdn.net/+"+self.name+"/article/details/"
        for list in self.get_links(html):
            if list and re.match(link_regex,list):
                self.link_set.add(list)

    def download(self, pos=None, num_retries=3,user_agent="wswp",proxies=None):
            headers={"User-Agent":user_agent}
            html=""
            for j in range(num_retries):
                try:
                    resp=requests.get(self.link_set[pos],headers=headers,proxies=proxies)
                    if resp.status_code==200:
                        html=resp.text

                    if 500<=resp.status_code<=600:
                        print(f"retry for {j+2} time")
                except Exception as e:
                    break
            list=[]
            try:
                title = self.get_title(html)
                good = self.get_good(html)
                dic = {"title": title, "read": good,}
                list.append(dic)
                print(dic["title"]+" "+dic["read"])
                with open(self.name+"_title.txt","a+",encoding="utf-8") as file:
                    file.write(dic["title"]+" "+dic["read"]+"\n")
            except Exception as e:
                print(e)

    def get_good(self,html):
        web_regex = re.compile(r"<span class=\"read-count\">阅读数 .*</span>")
        num=web_regex.findall(html)
        num=num[0]
        pos=num.find("阅读数")
        pos2=num.find("</span>")
        str=num[pos+3:pos2]
        return str

    def get_title2(self,i):
        web_regex = re.compile(r">.*<")
        title=web_regex.findall(i)
        str=title[0]
        str=str[1:-1]
        return str

    def get_title(self,html):
        web_regex = re.compile(r"<h1 class=\"title-article\">.*</h1>")
        title_list=web_regex.findall(html)
        title=title_list[0]
        return self.get_title2(title)

    def start(self):
        url = "https://blog.csdn.net/"
        url2= "/article/list/"
        for i in range(1, 8):
            self.link_cwrael(url +self.name+url2+ str(i) + "?")

        self.link_set=list(self.link_set)
        threads = []
        while self.pos<self.link_set.__len__():
            while len(threads) < 20 :
                thread = threading.Thread(target=self.download, args=[self.pos])
                thread.setDaemon(True)
                threads.append(thread)

                self.pos += 1
                thread.start()
            for thread in threads:
                thread.join()

            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
        self.table()

    def table(self):
        file = open(self.name + "_title.txt", "r", encoding="utf-8")
        title = []
        read = []
        list = file.readlines()
        for i in list:

            pos = None
            end = i.__len__() - 1
            while end >= 0:
                if (i[end] == " "):
                    pos = end
                    break
                end -= 1
            pos2 = None
            while end >= 0:
                if (i[end] != " "):
                    pos2 = end + 1
                    break
                end -= 1

            title_str = i[:pos2]
            j = title_str.__len__()
            j = int(j / 2)
            title_str = title_str[:j] + "\n" + title_str[j:]
            title.append(title_str)

            read_str = i[pos:]
            read_str = read_str.strip()
            read.append(int(read_str))

        read_data = []
        title_data = []
        j = 0
        for i in read:
            if i > self.num:
                read_data.append(i)
                title_data.append(title[j])
            j += 1

        bar = Bar()
        bar.add_xaxis(title_data)
        bar.add_yaxis("访问量大于" + str(self.num) + "的博客", read_data)
        bar.reversal_axis()
        bar.render(self.name + ".html")

sp=spider("Q_M_X_D_D_",300)
sp.start()