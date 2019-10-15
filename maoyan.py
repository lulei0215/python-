import requests
from multiprocessing import Pool
from requests.exceptions import RequestException
import  re
import json

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return response.status_code
    except RequestException:
        return 1

def parse_one_page(html):
    pattern = re.compile('<li>.*?<div .*?<em.*?>(\d+).*?<img.*?src="(.*?)".*?<span class.*?>(.*?)</span>.*?<div class.*?<p class.*?>(.*?)<br>(.*?)</p>.*?<span class="rating_num".*?>(.*?)</span>.*?</li>',re.S)
    # print(1)
    items = re.findall(pattern,html)
    # print(items)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'type':item[4].strip()[3:],
            'point':item[5],
        }

def write_to_file(content):
    with open('maoyan.txt','a',encoding='utf-8') as f:
            f.write(json.dumps(content,ensure_ascii=False) + '\n')
            f.close()

def main(offset):
    url = "https://movie.douban.com/top250?start="+ str(offset)
    html = get_one_page(url)
    #print(html)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    # for i in range(10):
    #     main(i*25)
    pool = Pool()
    pool.map(main,[i*25 for i in range(10)])